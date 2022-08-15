from django.urls import path
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .utils import decorate_urlpatterns, req_auth
from .views import API

urlpatterns = [
    path("users/", API.users.read, name="api_users_read"),
    path("users/create/", API.users.create, name="api_users_create"),
    path("users/delete/", API.users.delete, name="api_users_delete"),
    path("users/update/", API.users.update, name="api_users_update"),
]

# Decorate all paths in list with Django's csrf_exempt and never_cache decorators,
# along with our custom req_auth decorator to ensure a logged-in user is requesting.
urlpatterns = decorate_urlpatterns(urlpatterns, csrf_exempt)
urlpatterns = decorate_urlpatterns(urlpatterns, never_cache)
urlpatterns = decorate_urlpatterns(urlpatterns, req_auth)
