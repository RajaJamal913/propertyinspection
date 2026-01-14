import logging
import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination

from .helpers import Utils
from .models import Property
from .serializers import PropertySerializer

logger = logging.getLogger(__name__)

DYNAMIC_API = {}
try:
    DYNAMIC_API = getattr(settings, "DYNAMIC_API")
except Exception:
    DYNAMIC_API = {}

# ---------- index ----------
def index(request):
    context = {"routes": settings.DYNAMIC_API.keys() if hasattr(settings, "DYNAMIC_API") else [], "segment": "dyn_api"}
    return render(request, "dyn_api/index.html", context)


# ---------- DynamicAPI ----------
class DynamicAPI(APIView):
    def get(self, request, **kwargs):
        model_id = kwargs.get("id", None)
        try:
            serializer_cls = Utils.get_serializer(DYNAMIC_API, kwargs.get("model_name"))
            manager = Utils.get_manager(DYNAMIC_API, kwargs.get("model_name"))

            if model_id is not None:
                # Validate integer id
                try:
                    model_id = int(model_id)
                    if model_id < 0:
                        raise ValueError("Expect positive int")
                except ValueError as e:
                    return Response(
                        {"message": "Input Error = " + str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
                    )

                thing = manager.get(id=model_id)
                output = serializer_cls(instance=thing).data
            else:
                all_things = manager.all()
                output = [serializer_cls(instance=thing).data for thing in all_things]

        except KeyError:
            return Response(
                {"message": "this model is not activated or not exist.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (Http404, Utils.get_class(DYNAMIC_API, kwargs.get("model_name")).DoesNotExist):
            return Response(
                {"message": "object with given id not found.", "success": False}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("Unexpected error in DynamicAPI.get for model %s: %s", kwargs.get("model_name"), e)
            return Response({"message": "Internal Server Error", "detail": str(e), "success": False}, status=500)

        return Response({"data": output, "success": True}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        try:
            serializer_cls = Utils.get_serializer(DYNAMIC_API, kwargs.get("model_name"))
            model_serializer = serializer_cls(data=request.data)

            if not model_serializer.is_valid():
                logger.error(
                    "DynamicAPI POST validation failed for model %s: %s\nReceived: %s",
                    kwargs.get("model_name"),
                    model_serializer.errors,
                    request.data,
                )
                return Response(
                    {"message": "Validation error", "errors": model_serializer.errors, "received": request.data, "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            instance = model_serializer.save()
            output = serializer_cls(instance=instance).data

        except KeyError:
            return Response(
                {"message": "this model is not activated or not exist.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.exception("Unexpected error in DynamicAPI.post for model %s: %s", kwargs.get("model_name"), e)
            return Response({"message": "Internal Server Error", "detail": str(e), "success": False}, status=500)

        return Response({"message": "Record Created.", "data": output, "success": True}, status=status.HTTP_201_CREATED)

    def put(self, request, **kwargs):
        try:
            serializer_cls = Utils.get_serializer(DYNAMIC_API, kwargs.get("model_name"))
            manager = Utils.get_manager(DYNAMIC_API, kwargs.get("model_name"))
            thing = manager.get(id=kwargs.get("id"))

            model_serializer = serializer_cls(instance=thing, data=request.data, partial=True)
            if not model_serializer.is_valid():
                logger.error(
                    "DynamicAPI PUT validation failed for model %s id=%s: %s\nReceived: %s",
                    kwargs.get("model_name"),
                    kwargs.get("id"),
                    model_serializer.errors,
                    request.data,
                )
                return Response(
                    {"message": "Validation error", "errors": model_serializer.errors, "received": request.data, "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            instance = model_serializer.save()
            output = serializer_cls(instance=instance).data

        except KeyError:
            return Response(
                {"message": "this model is not activated or not exist.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Utils.get_class(DYNAMIC_API, kwargs.get("model_name")).DoesNotExist:
            return Response(
                {"message": "object with given id not found.", "success": False}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("Unexpected error in DynamicAPI.put for model %s id=%s: %s", kwargs.get("model_name"), kwargs.get("id"), e)
            return Response({"message": "Internal Server Error", "detail": str(e), "success": False}, status=500)

        return Response({"message": "Record Updated.", "data": output, "success": True}, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        try:
            model_cls = Utils.get_class(DYNAMIC_API, kwargs.get("model_name"))
            model_manager = Utils.get_manager(DYNAMIC_API, kwargs.get("model_name"))
            to_delete_id = kwargs.get("id")

            # validate id
            try:
                if to_delete_id is None:
                    raise ValueError("id is required for delete")
                to_delete_id = int(to_delete_id)
            except (ValueError, TypeError) as e:
                return Response({"message": "Input Error = " + str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)

            obj = model_manager.get(id=to_delete_id)
            obj.delete()

        except KeyError:
            return Response(
                {"message": "this model is not activated or not exist.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except model_cls.DoesNotExist:
            return Response({"message": "object with given id not found.", "success": False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error in DynamicAPI.delete for model %s id=%s: %s", kwargs.get("model_name"), kwargs.get("id"), e)
            return Response({"message": "Internal Server Error", "detail": str(e), "success": False}, status=500)

        return Response({"message": "Record Deleted.", "success": True}, status=status.HTTP_200_OK)


# ---------- PropertyViewSet ----------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 10


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Property create validation error: %s\nReceived: %s", serializer.errors, request.data)
            return Response(
                {"message": "Validation error", "errors": serializer.errors, "received": request.data, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            property_obj = serializer.save()
            return Response(self.get_serializer(property_obj).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Unexpected error creating Property: %s", e)
            return Response({"message": "Internal Server Error", "detail": str(e), "success": False}, status=500)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            logger.error("Property update validation error for id=%s: %s\nReceived: %s", instance.pk, serializer.errors, request.data)
            return Response(
                {"message": "Validation error", "errors": serializer.errors, "received": request.data, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            property_obj = serializer.save()
            return Response(self.get_serializer(property_obj).data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Unexpected error updating Property id=%s: %s", instance.pk, e)
            return Response({"message": "Internal Server Error", "detail": str(e), "success": False}, status=500)


# ---------- Reports / Helpers ----------
def property_report(request, pk):
    prop = get_object_or_404(
        Property.objects.select_related("utility", "detector_compliance", "cleaning_standard").prefetch_related(
            "tenants",
            "smoke_detectors",
            "co_detectors",
            "keys",
            "documents",
            "external_surfaces",
            "external_features",
            "boundaries",
            Prefetch("rooms__doors"),
            Prefetch("rooms__windows"),
            Prefetch("rooms__ceilings"),
            Prefetch("rooms__floors"),
            Prefetch("rooms__walls"),
            Prefetch("rooms__fixtures_fittings"),
            Prefetch("rooms__furnishings"),
            Prefetch("rooms__cupboards"),
            Prefetch("rooms__kitchen_appliances"),
        ),
        pk=pk,
    )

    tenant_count = prop.tenants.count()
    total_rooms = prop.rooms.count()
    smoke_detector_count = prop.smoke_detectors.count()
    co_detector_count = prop.co_detectors.count()
    detector_count = smoke_detector_count + co_detector_count
    key_count = prop.keys.count()
    document_count = prop.documents.count()
    external_features_count = prop.external_features.count()
    boundaries_count = prop.boundaries.count()

    utility = getattr(prop, "utility", None)
    cleaning_standard = getattr(prop, "cleaning_standard", None)
    detector_compliance = getattr(prop, "detector_compliance", None)

    front_photos = prop.front_elevation_photos or []
    if isinstance(front_photos, str):
        try:
            front_photos = json.loads(front_photos)
        except (json.JSONDecodeError, TypeError):
            front_photos = [front_photos]

    other_views = prop.other_views or []
    if isinstance(other_views, str):
        try:
            other_views = json.loads(other_views)
        except (json.JSONDecodeError, TypeError):
            other_views = [other_views]

    if not isinstance(front_photos, list):
        front_photos = [front_photos]
    if not isinstance(other_views, list):
        other_views = [other_views]

    serialized_property = PropertySerializer(prop).data

    context = {
        "property": serialized_property,
        "property_obj": prop,
        "now": timezone.localtime(timezone.now()),
        "inspected_by": prop.inspectedBy,
        "tenant_count": tenant_count,
        "total_rooms": total_rooms,
        "detector_count": detector_count,
        "smoke_detector_count": smoke_detector_count,
        "co_detector_count": co_detector_count,
        "key_count": key_count,
        "document_count": document_count,
        "external_features_count": external_features_count,
        "boundaries_count": boundaries_count,
        "utility": utility,
        "cleaning_standard": cleaning_standard,
        "detector_compliance": detector_compliance,
        "front_photos": front_photos,
        "other_views": other_views,
    }

    return render(request, "reports/property.html", context)


def property_list(request):
    qs = (
        Property.objects.all()
        .select_related("utility", "detector_compliance", "cleaning_standard")
        .prefetch_related("tenants", "rooms")
        .order_by("-id")
    )

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(address__icontains=q) | Q(postcode__icontains=q))

    paginator = Paginator(qs, 25)
    page_number = request.GET.get("page")
    properties = paginator.get_page(page_number)

    return render(request, "reports/property_list.html", {"properties": properties})
