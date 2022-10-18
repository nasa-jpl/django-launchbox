# Launchbox Helper for Django

A plugin for your Django app to assist in integrating with [Launchbox](https://github.com/nasa-jpl/launchbox).


---

## Features

The plugin currently offers the following features:

- A helper class for easier configuration of settings for resources provided by Launchbox,
  like databases, caches, and storage buckets
- A class for querying an identity service provided by a Launchbox plugin
- An API for Launchbox to get information from your application so that
  it can display, or even change, that info within the Launchbox Management Dashboard

### Planned features

- Integrations with other Launchbox plugin types – authentication and SSL certificate management


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


## Working with Launchbox plugins

### Identity providers

Use the `LBIdendity` class to query an identity service provided by a Launchbox plugin.
For all examples given below, be sure you have imported the class with:

```python
from launchbox import LBIdentity
```

You will need to know a plugin's `plugin_id` (an identifier internal to Launchbox) to work with it.

#### Get a specific user

To get a user's details when you know their exact user ID within the identity database, use the `user.get()` method:

```python
user_details = LBIdentity("plugin_id").user.get("user_id")
```

#### Search for a user with partial matching

To search for a user when you aren't certain of their user ID, use the `user.search()` method:

```python
user_details = LBIdentity("plugin_id").user.search("user_id")
```

#### Get the groups a user belongs to

For identity providers that can place users into groups,
you can get a list of a user's groups with the `user.groups()` method:

```python
user_groups = LBIdentity("plugin_id").user.groups("user_id")
```

#### Get group details

To get the details of a group, use the `group.get()` method:

```python
group_details = LBIdentity("plugin_id").group.get("group_id")
```
