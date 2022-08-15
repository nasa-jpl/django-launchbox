# Launchbox Helper for Django

A plugin for your Django app to assist in integrating with [Launchbox](https://github.com/nasa-jpl/launchbox).


---

## Installation

1. Add `django-launchbox` to your project's requirements and install it.
2. Add `"launchbox"` to your `INSTALLED_APPS` setting like this:
   ```python
   INSTALLED_APPS = [
       "launchbox",
       ...
   ]
   ```
3. Optionally add the `LB_USER_ATTRIBUTES` setting to specify which
   user model fields and properties you want to log and validate:
   ```python
   LB_USER_ATTRIBUTES = [
       "first_name",
       "last_name",
       "middle_initial",
       "display_name",
       "email",
       "admin_access",
       "is_active",
       "is_editor",
       "is_moderator",
       "is_owner",
       "is_superuser",
   ]
   ```
4. Add the Launchbox URLs to the `urlpatterns` in your project's `urls.py`:
   ```python
   # LaunchBox Service Bridge API
   path("bridge/", include("launchbox.api.urls")),
   ```
