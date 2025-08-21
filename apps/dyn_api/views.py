# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from django.conf import settings

DYNAMIC_API = {}

try:
    DYNAMIC_API = getattr(settings, 'DYNAMIC_API') 
except:     
    pass 

from .helpers import Utils 

def index(request):
    
    context = {
        'routes' : settings.DYNAMIC_API.keys(),
        'segment': 'dyn_api'
    }

    return render(request, 'dyn_api/index.html', context)

class DynamicAPI(APIView):

    # READ : GET api/model/id or api/model
    def get(self, request, **kwargs):

        model_id = kwargs.get('id', None)
        try:
            if model_id is not None:

                # Validate for integer
                try:
                    model_id = int(model_id)

                    if model_id < 0:
                        raise ValueError('Expect positive int')

                except ValueError as e:
                    return Response(data={
                        'message': 'Input Error = ' + str(e),
                        'success': False
                    }, status=400)

                thing = get_object_or_404(Utils.get_manager(DYNAMIC_API, kwargs.get('model_name')), id=model_id)
                model_serializer = Utils.get_serializer(DYNAMIC_API, kwargs.get('model_name'))(instance=thing)
                output = model_serializer.data
            else:
                all_things = Utils.get_manager(DYNAMIC_API, kwargs.get('model_name')).all()
                thing_serializer = Utils.get_serializer(DYNAMIC_API, kwargs.get('model_name'))
                output = []
                for thing in all_things:
                    output.append(thing_serializer(instance=thing).data)
        except KeyError:
            return Response(data={
                'message': 'this model is not activated or not exist.',
                'success': False
            }, status=400)
        except Http404:
            return Response(data={
                'message': 'object with given id not found.',
                'success': False
            }, status=404)
        return Response(data={
            'data': output,
            'success': True
            }, status=200)

    # CREATE : POST api/model/
    #@check_permission
    def post(self, request, **kwargs):
        try:
            model_serializer = Utils.get_serializer(DYNAMIC_API, kwargs.get('model_name'))(data=request.data)
            if model_serializer.is_valid():
                model_serializer.save()
            else:
                return Response(data={
                    **model_serializer.errors,
                    'success': False
                }, status=400)
        except KeyError:
            return Response(data={
                'message': 'this model is not activated or not exist.',
                'success': False
            }, status=400)
        return Response(data={
            'message': 'Record Created.',
            'success': True
        }, status=200)

    # UPDATE : PUT api/model/id/
    #@check_permission
    def put(self, request, **kwargs):
        try:
            thing = get_object_or_404(Utils.get_manager(DYNAMIC_API, kwargs.get('model_name')), id=kwargs.get('id'))
            model_serializer = Utils.get_serializer(DYNAMIC_API, kwargs.get('model_name'))(instance=thing,
                                                                                           data=request.data,
                                                                                           partial=True)
            if model_serializer.is_valid():
                model_serializer.save()
            else:
                return Response(data={
                    **model_serializer.errors,
                    'success': False
                }, status=400)
        except KeyError:
            return Response(data={
                'message': 'this model is not activated or not exist.',
                'success': False
            }, status=400)
        except Http404:
            return Response(data={
                'message': 'object with given id not found.',
                'success': False
            }, status=404)
        return Response(data={
            'message': 'Record Updated.',
            'success': True
            }, status=200)

    # DELETE : DELETE api/model/id/
    #@check_permission
    def delete(self, request, **kwargs):
        try:
            model_manager = Utils.get_manager(DYNAMIC_API, kwargs.get('model_name'))
            to_delete_id = kwargs.get('id')
            model_manager.get(id=to_delete_id).delete()
        except KeyError:
            return Response(data={
                'message': 'this model is not activated or not exist.',
                'success': False
            }, status=400)
        except Utils.get_class(DYNAMIC_API, kwargs.get('model_name')).DoesNotExist as e:
            return Response(data={
                'message': 'object with given id not found.',
                'success': False
            }, status=404)
        return Response(data={
            'message': 'Record Deleted.',
            'success': True
        }, status=200)

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Property
from .serializers import PropertySerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1  # You can set this as desired
    page_size_query_param = 'page_size'
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
        serializer.is_valid(raise_exception=True)
        property_obj = serializer.save()
        return Response(self.get_serializer(property_obj).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        property_obj = serializer.save()
        return Response(self.get_serializer(property_obj).data, status=status.HTTP_200_OK)
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Prefetch

from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from django.utils import timezone
from .models import Property
from .serializers import PropertySerializer

def property_report(request, pk):
    prop = get_object_or_404(
        Property.objects.select_related(
            'utility', 'detector_compliance', 'cleaning_standard'
        ).prefetch_related(
            'tenants',
            'smoke_detectors',
            'co_detectors',
            'keys',
            'documents',
            'external_surfaces',
            'external_features',
            'boundaries',
            Prefetch('rooms__doors'),
            Prefetch('rooms__windows'),
            Prefetch('rooms__ceilings'),
            Prefetch('rooms__floors'),
            Prefetch('rooms__walls'),
            Prefetch('rooms__fixtures_fittings'),
            Prefetch('rooms__furnishings'),
            Prefetch('rooms__cupboards'),
            Prefetch('rooms__kitchen_appliances'),
        ),
        pk=pk
    )

    # Counts / summaries
    tenant_count = prop.tenants.count()
    total_rooms = prop.rooms.count()
    smoke_detector_count = prop.smoke_detectors.count()
    co_detector_count = prop.co_detectors.count()
    detector_count = smoke_detector_count + co_detector_count
    key_count = prop.keys.count()
    document_count = prop.documents.count()
    external_features_count = prop.external_features.count()
    boundaries_count = prop.boundaries.count()

    # OneToOne objects may be None if not created
    utility = getattr(prop, 'utility', None)
    cleaning_standard = getattr(prop, 'cleaning_standard', None)
    detector_compliance = getattr(prop, 'detector_compliance', None)

    # Handle JSON fields properly - ensure they are lists
    front_photos = prop.front_elevation_photos or []
    # If it's a string, try to parse it as JSON
    if isinstance(front_photos, str):
        try:
            import json
            front_photos = json.loads(front_photos)
        except (json.JSONDecodeError, TypeError):
            front_photos = [front_photos]  # Treat as single URL
    
    other_views = prop.other_views or []
    # If it's a string, try to parse it as JSON
    if isinstance(other_views, str):
        try:
            import json
            other_views = json.loads(other_views)
        except (json.JSONDecodeError, TypeError):
            other_views = [other_views]  # Treat as single URL

    # Ensure we're always working with lists
    if not isinstance(front_photos, list):
        front_photos = [front_photos]
    if not isinstance(other_views, list):
        other_views = [other_views]

    # Serialized version - this is what the template expects
    serialized_property = PropertySerializer(prop).data

    context = {
        # Use the serialized property data in the template
        "property": serialized_property,
        # Keep the original object for any direct model access needed
        "property_obj": prop,
        "now": timezone.localtime(timezone.now()),
        "inspected_by": prop.inspectedBy,
        # summaries
        "tenant_count": tenant_count,
        "total_rooms": total_rooms,
        "detector_count": detector_count,
        "smoke_detector_count": smoke_detector_count,
        "co_detector_count": co_detector_count,
        "key_count": key_count,
        "document_count": document_count,
        "external_features_count": external_features_count,
        "boundaries_count": boundaries_count,
        # optional objects
        "utility": utility,
        "cleaning_standard": cleaning_standard,
        "detector_compliance": detector_compliance,
        # photos
        "front_photos": front_photos,
        "other_views": other_views,
    }

    return render(request, "reports/property.html", context)