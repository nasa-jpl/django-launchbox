# Launchbox Helper for Django

A plugin for your Django app to assist in integrating with [Launchbox](https://github.com/nasa-jpl/launchbox).


---

## Features

The plugin currently offers the following features:

- A helper for easier configuration of settings for resources provided by Launchbox,
  like databases, caches, and storage buckets
- An API for Launchbox to get information from your application so that
  it can display, or even change, that info within the Launchbox Management Dashboard

### Planned features

- Integrations with Launchbox plugins for identity, authentication, and SSL certificate management


## Installation

These steps assume that you have already added a `launch.yaml` file to your application.
For more information on that, [visit the Launchbox docs](https://nasa-jpl.github.io/launchbox/features/services/).

1. Add `django-launchbox` to your project's requirements and install it.
2. Add `"launchbox"` to your `INSTALLED_APPS` setting like this:
   ```python
   INSTALLED_APPS = [
       "launchbox",
       ...
   ]
   ```
3. Update your Django settings to use the database provided by Launchbox:
   ```python
   from launchbox import LBResources
   
   DATABASES = {
       # "db" is the resource identifier specified in your launch.yaml file
       "default": LBResources().settings("db")
   }
   ```
   - If you configured a cache or storage bucket in your `launch.yaml` file,
     update those settings, too:
     ```python
     from launchbox import LBResources
     
     CACHES = {
         # "cache" is the resource identifier specified in your launch.yaml file
         "default": LBResources().settings("cache")
     }
     
     # AWS_STORAGE_BUCKET_NAME is a django-storages setting
     # "storage" is the resource identifier specified in your launch.yaml file
     AWS_STORAGE_BUCKET_NAME = LBResources().settings("storage") 
   ```
4. If you want to manage users in the Launchbox dashboard,
   add the `LB_USER_ATTRIBUTES` setting to specify which user model fields
   and properties you want to log and validate:
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
   And then add the Launchbox bridge API URLs to the `urlpatterns` in your project's `urls.py`:
   ```python
   # Launchbox Service Bridge API
   path("bridge/", include("launchbox.api.urls")),
   ```
