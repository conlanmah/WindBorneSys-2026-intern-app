import os
import json
import logging
import requests
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.views.decorators.http import require_GET
from django.shortcuts import render

logger = logging.getLogger(__name__)

# Set this in your env, e.g. POINTS_API_URL="https://example.com/api/points"
POINTS_API_URL = os.getenv("POINTS_API_URL", "")

def map_view(request):
    """
    Renders the Leaflet map page.
    Pass the API URL down in case you want the browser to hit it directly.
    If CORS blocks it, the JS will fall back to the /points/ proxy.
    """
    return render(request, "map.html", {"api_url": POINTS_API_URL})

@require_GET
def points_proxy(request):
    """
    Simple GET proxy to avoid CORS issues.
    Fetches from POINTS_API_URL and returns the data as-is.
    Expected response: JSON array of [lat, lon, value].
    """
    if not POINTS_API_URL:
        return HttpResponseServerError("POINTS_API_URL is not configured on the server.")
    try:
        r = requests.get(POINTS_API_URL, timeout=10)
        r.raise_for_status()
        # Validate it looks like a JSON list of lists
        data = r.json()
        if not isinstance(data, list):
            return HttpResponseServerError("Upstream API didn't return a JSON list.")
        return JsonResponse(data, safe=False)
    except requests.RequestException as e:
        logger.exception("Error fetching points: %s", e)
        return HttpResponseServerError("Failed to fetch points from upstream.")
    except json.JSONDecodeError:
        return HttpResponseServerError("Upstream API response was not valid JSON.")
