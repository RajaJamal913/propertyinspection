from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
import tempfile

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html', {'segment': 'dashboard'})


def property_manual_pdf(request):
    """
    Render the `reports/property_manual.html` template to a PDF and return it.

    Attempt order:
      1. WeasyPrint (preferred)
      2. pdfkit (wkhtmltopdf) as a fallback

    Notes for deployment:
      - WeasyPrint requires system libraries (cairo, pango, gdk-pixbuf). Install via your OS package manager.
      - If using wkhtmltopdf/pdfkit, ensure wkhtmltopdf binary is installed and accessible.
    """

    context = {}
    # Render template to HTML string
    html_string = render_to_string('reports/property_manual.html', context, request=request)

    # Base URL for resolving static files
    base_url = request.build_absolute_uri('/')

    # Decide disposition: attachment if ?download=1 or settings.PDF_FORCE_DOWNLOAD
    force_download = request.GET.get('download') == '1' or getattr(settings, 'PDF_FORCE_DOWNLOAD', False)
    disposition_type = 'attachment' if force_download else 'inline'

    # Try WeasyPrint first
    try:
        from weasyprint import HTML, CSS

        html = HTML(string=html_string, base_url=base_url)
        # Small page style; caller can override if needed
        pdf = html.write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition_type}; filename="property_manual.pdf"'
        return response

    except Exception as we_err:
        # Fallback to pdfkit (wkhtmltopdf)
        try:
            import pdfkit

            options = {
                'enable-local-file-access': None,
            }
            # If user has provided a WKHTMLTOPDF path in settings, use it
            wk_cmd = getattr(settings, 'WKHTMLTOPDF_CMD', None)
            if wk_cmd:
                config = pdfkit.configuration(wkhtmltopdf=wk_cmd)
                pdf = pdfkit.from_string(html_string, False, options=options, configuration=config)
            else:
                pdf = pdfkit.from_string(html_string, False, options=options)

            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'{disposition_type}; filename="property_manual.pdf"'
            return response

        except Exception as pk_err:
            # Both methods failed — return a helpful error message
            msg = (
                "PDF generation is not available on this server.\n"
                "Install WeasyPrint (and system dependencies) or wkhtmltopdf and pdfkit.\n"
                "WeasyPrint error: %s\npdfkit error: %s" % (we_err, pk_err)
            )
            return HttpResponse(msg, content_type='text/plain', status=500)

