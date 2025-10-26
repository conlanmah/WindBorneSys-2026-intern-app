import os
import json
import logging
import requests
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.conf import settings

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
    Expected response: JSON array of [lat, lon, alt].
    They mentioned this data sometimes is corrupted, I wonder
    if that will be an issue
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

########################
# N2YO plotting ########
########################


@require_GET
def satellite_positions(request):
    """
    Fetch current positions for a defined set of satellites from N2YO.
    Returns: [
      {"id": 25544, "name": "ISS (ZARYA)", "lat": ..., "lon": ..., "alt_km": ..., "timestamp": ...},
      ...
    ]
    """
    if not settings.N2YO_API_KEY:
        return HttpResponseServerError("N2YO_API_KEY is not configured.")

    base = "https://api.n2yo.com/rest/v1/satellite/positions"
    obs = settings.N2YO_OBSERVER
    seconds = getattr(settings, "N2YO_SECONDS", 1)

    results = []
    for sat in getattr(settings, "SATELLITES", []):
        satid = sat["id"]
        name = sat.get("name", str(satid))
        url = f"{base}/{satid}/{obs['lat']}/{obs['lon']}/{obs['alt_km']}/{seconds}?apiKey={settings.N2YO_API_KEY}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            # N2YO returns {"positions":[{"satlatitude":..., "satlongitude":..., "sataltitude":..., "timestamp":...}, ...], ...}
            positions = data.get("positions") or []
            if not positions:
                continue
            last = positions[-1]
            lat = last.get("satlatitude")
            lon = last.get("satlongitude")
            alt = last.get("sataltitude")
            ts  = last.get("timestamp")
            # Basic sanity
            if lat is None or lon is None:
                continue
            results.append({
                "id": satid,
                "name": name,
                "lat": float(lat),
                "lon": float(lon),
                "alt_km": float(alt) if alt is not None else None,
                "timestamp": ts,
            })
        except requests.RequestException as e:
            logger.exception("N2YO fetch failed for %s: %s", satid, e)
        except (ValueError, TypeError) as e:
            logger.exception("Bad JSON from N2YO for %s: %s", satid, e)

    return JsonResponse(results, safe=False)
