import json
import logging
from functools import update_wrapper

from django.http import HttpResponse, JsonResponse

# Remove these when the Launchbox management bridge API is available.
# They currently pull from the existing code in WCP to feed the mock LBMgmtAPI class.
from config.manage.bridge import WCPBridge
from config.manage.jpl import WCPLDAP

logger = logging.getLogger(__name__)


class LBMgmtAPI:
    """Temporarily mock Launchbox management bridge API endpoints."""

    dir = WCPLDAP
    port = WCPBridge.port


class LBServiceAPI:
    class request:
        @staticmethod
        def auth(request):
            # Limit requests to internal port only.
            return int(request.get_port()) == LBMgmtAPI.port

        @staticmethod
        def json(request):
            try:
                return json.loads(request.body)
            except Exception:
                logger.warning(
                    "LBServiceAPI.request: Unable to decode request body (invalid JSON)"
                )
            return False

        @staticmethod
        def params(request):
            return dict(request.GET.items())

    class response:
        @staticmethod
        def error(message):
            return LBServiceAPI.response.json({"error": message})

        @staticmethod
        def invalid():
            return LBServiceAPI.response.error("parameters")

        @staticmethod
        def json(data):
            return JsonResponse(data)

        @staticmethod
        def unauth():
            return HttpResponse("401 Unauthorized", status=401)


# Decorator: Require auth
def req_auth(func):
    def _req_auth(request, *args, **kwargs):
        if LBServiceAPI.request.auth(request):
            return func(request, *args, **kwargs)
        else:
            return LBServiceAPI.response.unauth()

    return _req_auth


def decorate_urlpatterns(urlpatterns, decorator):
    """Decorate all the views in the passed urlpatterns list with the given decorator.

    Hat tip:
    https://github.com/wagtail/wagtail/blob/d10f15e55806c6944827d801cd9c2d53f5da4186/wagtail/utils/urlpatterns.py
    """

    for pattern in urlpatterns:
        if hasattr(pattern, "url_patterns"):
            # This is an included RegexURLResolver;
            # recursively decorate the views contained in it.
            decorate_urlpatterns(pattern.url_patterns, decorator)

        if getattr(pattern, "callback", None):
            pattern.callback = update_wrapper(
                decorator(pattern.callback), pattern.callback
            )

    return urlpatterns
