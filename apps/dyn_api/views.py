# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from pyexpat.errors import messages
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
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
# views.py (top imports)
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Property, Detector
from .serializers import PropertySerializer, DetectorSerializer

def calculate_property_counts(prop):
    """
    Calculate all relevant counts for a property including utilities, 
    rooms, room components, and detectors.
    
    Returns a dictionary with all counts needed for the report template.
    """
    counts = {}
    
    # ===== TENANT, KEY, DOCUMENT COUNTS =====
    counts['tenant_count'] = prop.tenants.count() if hasattr(prop, 'tenants') else 0
    counts['key_count'] = prop.keys.count() if hasattr(prop, 'keys') else 0
    counts['document_count'] = prop.documents.count() if hasattr(prop, 'documents') else 0
    
    # ===== EXTERNAL SURFACES, FEATURES, BOUNDARIES =====
    counts['external_surfaces_count'] = prop.external_surfaces.count() if hasattr(prop, 'external_surfaces') else 0
    counts['external_features_count'] = prop.external_features.count() if hasattr(prop, 'external_features') else 0
    counts['boundaries_count'] = prop.boundaries.count() if hasattr(prop, 'boundaries') else 0
    
    # ===== ROOM COUNTS =====
    counts['total_rooms'] = prop.rooms.count() if hasattr(prop, 'rooms') else 0
    
    # Count room components (doors, windows, ceilings, floors, walls, fixtures, furnishings, cupboards, appliances)
    if hasattr(prop, 'rooms') and prop.rooms.exists():
        doors_count = sum(room.doors.count() for room in prop.rooms.all())
        windows_count = sum(room.windows.count() for room in prop.rooms.all())
        ceilings_count = sum(room.ceilings.count() for room in prop.rooms.all())
        floors_count = sum(room.floors.count() for room in prop.rooms.all())
        walls_count = sum(room.walls.count() for room in prop.rooms.all())
        fixtures_count = sum(room.fixtures_fittings.count() for room in prop.rooms.all())
        furnishings_count = sum(room.furnishings.count() for room in prop.rooms.all())
        cupboards_count = sum(room.cupboards.count() for room in prop.rooms.all())
        appliances_count = sum(room.kitchen_appliances.count() for room in prop.rooms.all())
        
        counts['doors_count'] = doors_count
        counts['windows_count'] = windows_count
        counts['ceilings_count'] = ceilings_count
        counts['floors_count'] = floors_count
        counts['walls_count'] = walls_count
        counts['fixtures_count'] = fixtures_count
        counts['furnishings_count'] = furnishings_count
        counts['cupboards_count'] = cupboards_count
        counts['appliances_count'] = appliances_count
    else:
        counts['doors_count'] = 0
        counts['windows_count'] = 0
        counts['ceilings_count'] = 0
        counts['floors_count'] = 0
        counts['walls_count'] = 0
        counts['fixtures_count'] = 0
        counts['furnishings_count'] = 0
        counts['cupboards_count'] = 0
        counts['appliances_count'] = 0
    
    # ===== UTILITY METER COUNTS =====
    # Count meters: Gas, Electricity, Water, Heat, Other, Stopcock, Fusebox
    utility = getattr(prop, 'utility', None)
    meters_count = 0
    
    if utility:
        # Gas Meter (always present if utility exists)
        meters_count += 1
        # Electricity Meter (always present if utility exists)
        meters_count += 1
        # Water Meter (only if has data)
        if utility.waterMeterReading or utility.waterMeterSerialNumber or getattr(utility, 'waterMeterPhoto', None):
            meters_count += 1
        # Heat Meter (only if has data)
        if utility.heatMeterReading or utility.heatMeterSerialNumber or getattr(utility, 'heatMeterPhoto', None):
            meters_count += 1
        # Other Meter (only if has data)
        if getattr(utility, 'otherMeterType', None) or utility.otherMeterReading or utility.otherMeterSerialNumber or getattr(utility, 'otherMeterPhoto', None):
            meters_count += 1
        # Stopcock
        meters_count += 1
        # Fusebox
        meters_count += 1
    
    counts['meters_count'] = meters_count
    counts['utility'] = utility
    
    # ===== DETECTOR COUNTS =====
    # Smoke, CO, Heat detectors
    smoke_detectors = getattr(prop, 'smoke_detectors', [])
    co_detectors = getattr(prop, 'co_detectors', [])
    all_detectors = getattr(prop, 'all_detectors', [])
    
    counts['smoke_detector_count'] = len(smoke_detectors)
    counts['co_detector_count'] = len(co_detectors)
    counts['detector_count'] = len(all_detectors) or (counts['smoke_detector_count'] + counts['co_detector_count'])
    
    return counts


def property_report(request, pk):
    qs = Property.objects.select_related(
        'utility', 'detector_compliance', 'cleaning_standard'
    ).prefetch_related(
        'tenants',
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
        # Prefetch detectors separately into attrs for type-specific lists:
        Prefetch('detectors', queryset=Detector.objects.filter(detector_type='smoke'), to_attr='smoke_detectors'),
        Prefetch('detectors', queryset=Detector.objects.filter(detector_type='co'), to_attr='co_detectors'),
        # also keep the full detectors list if you want:
        Prefetch('detectors', queryset=Detector.objects.all(), to_attr='all_detectors'),
    )

    prop = get_object_or_404(qs, pk=pk)

    # Calculate all counts using helper function
    counts = calculate_property_counts(prop)
    
    # Get detector data
    smoke_detectors = getattr(prop, 'smoke_detectors', [])
    co_detectors = getattr(prop, 'co_detectors', [])
    smoke_detector_list = DetectorSerializer(smoke_detectors, many=True).data
    co_detector_list = DetectorSerializer(co_detectors, many=True).data

    cleaning_standard = getattr(prop, 'cleaning_standard', None)
    detector_compliance = getattr(prop, 'detector_compliance', None)

    # photos -> ensure lists
    front_photos = getattr(prop, 'front_elevation_photos', []) or []
    other_views = getattr(prop, 'other_views', []) or []

    # Ensure lists if JSONField stored single string accidentally
    import json
    if isinstance(front_photos, str):
        try:
            front_photos = json.loads(front_photos)
        except Exception:
            front_photos = [front_photos]
    if isinstance(other_views, str):
        try:
            other_views = json.loads(other_views)
        except Exception:
            other_views = [other_views]

    serialized_property = PropertySerializer(prop).data
    inspected_by = serialized_property.get('inspectedBy') or getattr(prop, 'inspectedBy', None)

    context = {
        "property": serialized_property,
        "property_obj": prop,
        "now": timezone.localtime(timezone.now()),
        "inspected_by": inspected_by,
        # Unpack all counts from helper function
        **counts,
        "smoke_detectors": smoke_detector_list,
        "co_detectors": co_detector_list,
        "cleaning_standard": cleaning_standard,
        "detector_compliance": detector_compliance,
        "front_photos": front_photos,
        "other_views": other_views,
    }

    return render(request, "reports/property.html", context)

from django.core.paginator import Paginator
from django.db.models import Q

def property_list(request):
    """
    List all properties (with optional search q=) and paginate results.
    Renders templates/reports/property_list.html
    """
    qs = Property.objects.all().select_related(
        'utility', 'detector_compliance', 'cleaning_standard'
    ).prefetch_related(
        'tenants', 'rooms'
    ).order_by('-id')

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(address__icontains=q) | Q(postcode__icontains=q))

    paginator = Paginator(qs, 25)  # 25 per page
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)

    return render(request, "reports/property_list.html", {
        'properties': properties
    })

@require_POST
@login_required
def property_delete(request, pk):
    """
    Delete a single Property (POST only).
    Uses 'next' hidden field or HTTP_REFERER to redirect back.
    Only logged-in users may perform the delete.
    Local import of django.contrib.messages avoids module name collisions.
    """
    # Local import ensures we get the real messages API even if the module-level
    # name 'messages' has been re-bound to something else.
    from django.contrib import messages as django_messages

    prop = get_object_or_404(Property, pk=pk)

    # OPTIONAL: strict permission check - uncomment and replace 'yourapp' with your app label
    # if not request.user.has_perm('yourapp.delete_property'):
    #     django_messages.error(request, "You don't have permission to delete properties.")
    #     return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('property_list'))

    address = getattr(prop, 'address', '')[:80]
    try:
        prop.delete()
        django_messages.success(request, f"Property '{address}' (ID {pk}) deleted.")
    except Exception as e:
        django_messages.error(request, f"Error deleting property ID {pk}: {str(e)}")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('property_list')
    return redirect(next_url)

# Add these imports near the top of your views.py (if not already present)
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import tempfile
import os
import io
import traceback
import json
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.text import slugify
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import base64
import multiprocessing

# 1x1 transparent PNG data URI (used as a placeholder when an image cannot be fetched)
TRANSPARENT_PNG_DATAURI = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAE0lEQVR42mP8/5+BFzA1wMDA"
    "gAEAAf8C4qv2xQAAAABJRU5ErkJggg=="
)

def make_requests_session(retries=2, backoff_factor=0.3, status_forcelist=(500,502,503,504)):
    s = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist,
                  raise_on_status=False)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s

def property_report_pdf(request, pk):
    """
    Robust PDF generator:
      - prefetch remote images with timeouts/retries
      - replace unreachable images with inline placeholder
      - write PDF to a temp file and stream to the client
      - on failure, write detailed log to /tmp/weasyprint_error_<pid>.log and return link
    """
    try:
        from weasyprint import HTML, CSS
    except ImportError:
        return HttpResponse("PDF generation library not installed. Please install weasyprint.", status=500)

    # Prepare containers for temp paths so we can cleanup
    tmp_image_paths = []
    tmp_pdf_path = None
    log_path = f"/tmp/weasyprint_error_{os.getpid()}.log"

    try:
        # --- your existing queryset + context construction (unchanged) ---
        qs = Property.objects.select_related(
            'utility', 'detector_compliance', 'cleaning_standard'
        ).prefetch_related(
            'tenants',
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
            Prefetch('detectors', queryset=Detector.objects.filter(detector_type='smoke'), to_attr='smoke_detectors'),
            Prefetch('detectors', queryset=Detector.objects.filter(detector_type='co'), to_attr='co_detectors'),
            Prefetch('detectors', queryset=Detector.objects.all(), to_attr='all_detectors'),
        )

        prop = get_object_or_404(qs, pk=pk)
        counts = calculate_property_counts(prop)

        smoke_detectors = getattr(prop, 'smoke_detectors', [])
        co_detectors = getattr(prop, 'co_detectors', [])
        smoke_detector_list = DetectorSerializer(smoke_detectors, many=True).data
        co_detector_list = DetectorSerializer(co_detectors, many=True).data

        cleaning_standard = getattr(prop, 'cleaning_standard', None)
        detector_compliance = getattr(prop, 'detector_compliance', None)

        front_photos = getattr(prop, 'front_elevation_photos', []) or []
        other_views = getattr(prop, 'other_views', []) or []

        # Ensure lists if JSONField stored single string accidentally
        if isinstance(front_photos, str):
            try:
                front_photos = json.loads(front_photos)
            except Exception:
                front_photos = [front_photos]
        if isinstance(other_views, str):
            try:
                other_views = json.loads(other_views)
            except Exception:
                other_views = [other_views]

        serialized_property = PropertySerializer(prop).data
        inspected_by = serialized_property.get('inspectedBy') or getattr(prop, 'inspectedBy', None)

        context = {
            "property": serialized_property,
            "property_obj": prop,
            "now": timezone.localtime(timezone.now()),
            "inspected_by": inspected_by,
            **counts,
            "smoke_detectors": smoke_detector_list,
            "co_detectors": co_detector_list,
            "cleaning_standard": cleaning_standard,
            "detector_compliance": detector_compliance,
            "front_photos": front_photos,
            "other_views": other_views,
            "is_pdf": True,  # Tell template to render for PDF
        }
        # --- end existing context build ---

        # Render HTML template
        html_string = render(request, "reports/property.html", context).content.decode('utf-8')

        # ---------------------
        # Prefetch remote images
        # ---------------------
        session = make_requests_session(retries=2)
        # conservative connect/read timeout tuple (connect, read) in seconds
        REQUEST_TIMEOUT = (5, 12)

        try:
            soup = BeautifulSoup(html_string, "html.parser")
            imgs = soup.find_all("img")
            for img in imgs:
                src = img.get("src") or ""
                src = src.strip()
                if not src:
                    continue

                # Resolve relative URLs to absolute URLs using request.base URL
                if src.startswith('/'):
                    src = urljoin(request.build_absolute_uri('/'), src)
                # If src is data: already inlined, leave it
                if src.startswith('data:'):
                    continue

                # If http(s) - try to fetch and save to temp file
                if src.startswith("http://") or src.startswith("https://"):
                    try:
                        # Perform HEAD first to quickly fail on big redirects / unreachable hosts
                        # Some servers block HEAD; so we use GET with stream=True
                        resp = session.get(src, stream=True, timeout=REQUEST_TIMEOUT, allow_redirects=True)
                        resp.raise_for_status()

                        # choose extension
                        path_ext = ""
                        parsed = urlparse(src)
                        if parsed.path:
                            _, ext = os.path.splitext(parsed.path)
                            if ext and len(ext) <= 5:
                                path_ext = ext.lower()
                        if not path_ext:
                            ctype = (resp.headers.get("Content-Type") or "").lower()
                            if "jpeg" in ctype or "jpg" in ctype:
                                path_ext = ".jpg"
                            elif "png" in ctype:
                                path_ext = ".png"
                            elif "webp" in ctype:
                                path_ext = ".webp"
                            else:
                                path_ext = ".img"

                        tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=path_ext)
                        # write in chunks
                        for chunk in resp.iter_content(8192):
                            if chunk:
                                tmpf.write(chunk)
                        tmpf.flush()
                        tmpf.close()
                        tmp_image_paths.append(tmpf.name)
                        # point to local file for WeasyPrint
                        img['src'] = 'file://' + tmpf.name

                    except Exception as e:
                        # If fetching fails for any reason, replace the <img> with a tiny inline placeholder
                        try:
                            img['src'] = TRANSPARENT_PNG_DATAURI
                        except Exception:
                            # as fallback, remove tag
                            img.decompose()
                        # Optionally record the failure in a small attribute for later debugging
                        img['data-fetch-error'] = str(e)
                        continue
                else:
                    # Not an http(s) URL (relative already handled) - leave as-is
                    continue

            html_string = str(soup)
        except Exception as e:
            # If anything goes wrong during prefetching, continue with original html_string
            # but log the incident in the debug log.
            with open(log_path, 'a') as fh:
                fh.write("Image prefetch failed:\n")
                fh.write(traceback.format_exc())
                fh.write("\n\n")

        # ---------------------
        # PDF CSS (keep your CSS if you have a long block; short example below)
        # ---------------------
        pdf_css = """
        @page {
            size: A4;
            margin: 0.75cm;
        }
        
        * {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        
        body {
            font-family: 'Segoe UI', Roboto, Arial, sans-serif;
            color: #333;
            font-size: 10pt;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background: white;
        }
        
        .no-print {
            display: none !important;
        }
        
        .report-container {
            max-width: 100%;
            margin: 0;
            background: white;
            padding: 0;
        }
        
        .report-header {
            background: #1e88e5;
            color: white;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            page-break-inside: avoid;
        }
        
        .report-header h1 {
            margin: 0 0 0.5rem 0;
            font-size: 1.5rem;
        }
        
        .report-header h2 {
            margin: 0.25rem 0;
            font-size: 1rem;
        }
        
        .report-header p {
            margin: 0.25rem 0;
            font-size: 0.9rem;
        }
        
        .section-card {
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 1.25rem;
            page-break-inside: avoid;
            background: white;
        }
        
        .section-header {
            background: #f5f5f5;
            border-bottom: 1px solid #ddd;
            padding: 0.85rem;
            font-weight: 600;
            color: #1e88e5;
            page-break-inside: avoid;
        }
        
        .section-body {
            padding: 1rem;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 0.75rem;
            margin: 1rem 0;
        }
        
        .summary-item {
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 0.75rem;
            text-align: center;
            page-break-inside: avoid;
        }
        
        .summary-count {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e88e5;
        }
        
        .summary-label {
            font-size: 0.8rem;
            color: #666;
            margin-top: 0.25rem;
        }
        
        .details-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
        }
        
        .detail-item {
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-left: 3px solid #1e88e5;
            border-radius: 3px;
            padding: 0.6rem;
            page-break-inside: avoid;
        }
        
        .detail-item-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #1e88e5;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }
        
        .detail-item-value {
            font-size: 0.9rem;
            color: #333;
            word-break: break-word;
        }
        
        .component-container {
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 1rem;
            page-break-inside: avoid;
            background: white;
        }
        
        .component-details {
            padding: 0.85rem;
            background: #fafafa;
        }
        
        .component-photos {
            padding: 0.85rem;
            background: #f5f5f5;
            border-top: 1px solid #ddd;
        }
        
        .component-title {
            font-weight: 700;
            color: #1e88e5;
            margin-bottom: 0.5rem;
        }
        
        .photo-gallery {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.5rem;
        }
        
        .photo-item {
            width: 100%;
            height: 100px;
            overflow: hidden;
            border-radius: 3px;
            border: 1px solid #ddd;
            background: #f9f9f9;
        }
        
        .photo-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        
        .signature-section {
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 2px dashed #ddd;
            page-break-inside: avoid;
        }
        
        .signature-header {
            font-weight: 700;
            color: #1e88e5;
            margin-bottom: 1rem;
        }
        
        .signature-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
        }
        
        .signature-box {
            page-break-inside: avoid;
        }
        
        .signature-print-label {
            font-weight: 600;
            color: #333;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        
        .signature-pad {
            width: 100%;
            height: 100px;
            border: 1px solid #000;
            background: white;
            display: block;
            margin-bottom: 0.5rem;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.75rem 0;
            font-size: 0.9rem;
        }
        
        .data-table th {
            background: #f5f5f5;
            padding: 0.6rem;
            text-align: left;
            font-weight: 600;
            color: #1e88e5;
            border: 1px solid #ddd;
        }
        
        .data-table td {
            padding: 0.6rem;
            border: 1px solid #ddd;
            vertical-align: top;
        }
        
        .sub-section {
            margin-bottom: 1.25rem;
            page-break-inside: avoid;
        }
        
        .sub-section-header {
            background: #f5f5f5;
            padding: 0.6rem 0.85rem;
            margin-bottom: 0.75rem;
            font-weight: 600;
            color: #1e88e5;
            border-bottom: 1px solid #ddd;
        }
        
        .room-card {
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 1.25rem;
            page-break-inside: avoid;
        }
        
        .room-header {
            background: #e6f0ff;
            padding: 0.75rem;
            border-bottom: 1px solid #ddd;
            font-weight: 600;
            color: #1e88e5;
        }
        
        .intro-section {
            background: #f0f8ff;
            border-left: 4px solid #1e88e5;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            page-break-inside: avoid;
        }
        
        .intro-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 0.85rem;
            margin-bottom: 0.75rem;
            page-break-inside: avoid;
        }
        
        .intro-card-header {
            background: #e6f0ff;
            border-bottom: 1px solid #ddd;
            padding: 0.6rem;
            font-weight: 600;
            color: #1e88e5;
            margin-bottom: 0.5rem;
        }
        
        .footer {
            text-align: center;
            padding: 1rem;
            border-top: 1px solid #ddd;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #666;
            page-break-inside: avoid;
        }
        """


        # Create WeasyPrint objects and write PDF to disk
        html_obj = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        css_obj = CSS(string=pdf_css)

        tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        tmp_pdf_path = tmp_pdf.name
        tmp_pdf.close()

        try:
            # This is the critical call that used to hang. We wrap in try/except and log any error.
            html_obj.write_pdf(target=tmp_pdf_path, stylesheets=[css_obj])
        except Exception as we:
            # Write a verbose debug file for immediate inspection
            with open(log_path, 'a') as fh:
                fh.write("WeasyPrint write_pdf failed:\n")
                fh.write(traceback.format_exc())
                fh.write("\n")
                fh.write("Temp images created:\n")
                for p in tmp_image_paths:
                    fh.write(f" - {p} (exists={os.path.exists(p)})\n")
                fh.write("\nHtml (truncated 10k chars):\n")
                fh.write(html_string[:10000])
                fh.write("\n\n")
            # Clean up temp images (we'll remove PDF later in finally)
            for p in tmp_image_paths:
                try:
                    os.remove(p)
                except Exception:
                    pass
            # Return an HTTP 500 with pointer to the debug log
            return HttpResponse(
                f"Error generating PDF. See server log for details: {log_path}",
                status=500
            )

        # If write_pdf succeeded, stream file back and clean up tmp files after streaming
        def stream_file(path, image_paths, chunk_size=8192):
            try:
                with open(path, 'rb') as fh:
                    while True:
                        chunk = fh.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
            finally:
                # cleanup pdf + tmp images
                try:
                    os.remove(path)
                except Exception:
                    pass
                for p in image_paths:
                    try:
                        os.remove(p)
                    except Exception:
                        pass

        safe_addr = slugify(getattr(prop, 'address', f'property_{pk}'))
        filename = f"Property_Report_{safe_addr or pk}.pdf"

        file_size = os.path.getsize(tmp_pdf_path)
        response = StreamingHttpResponse(stream_file(tmp_pdf_path, tmp_image_paths), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = str(file_size)
        return response

    except Exception as e:
        # catch-all: write a detailed log and return path
        with open(log_path, 'a') as fh:
            fh.write("Unhandled exception when generating PDF:\n")
            fh.write(traceback.format_exc())
            fh.write("\n")
        # try cleanup
        try:
            if tmp_pdf_path and os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)
        except Exception:
            pass
        for p in tmp_image_paths:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass
        return HttpResponse(f"Error generating PDF. See server log for details: {log_path}", status=500)

