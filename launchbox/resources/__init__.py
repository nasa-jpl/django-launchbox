import os

from django.core.exceptions import ImproperlyConfigured

import requests


class LBResources:
    def __init__(self):
        bridge_endpoint = os.environ.get("LB_BRIDGE_API")
        site_id = os.environ.get("LB_SITE_ID")
        self.resources = requests.get(f"{bridge_endpoint}/{site_id}/resources").json()

    def settings(self, resource_id):
        """Given a `resource_id`, return an appropriate Django settings dict.

        `resource_id` corresponds to the name of a resource in your launch.yaml file.
        For example, given this config in launch.yaml:

        resources:
          mydatabase:
            type: postgres

        'mydatabase' is the name of the resource to be passed to this method.
        """
        if resource_id in self.resources:
            if resource_type := self.resources[resource_id].get("type"):
                fname = f"build_{resource_type}_settings"
                if hasattr(self, fname) and callable(func := getattr(self, fname)):
                    return func(self.resources[resource_id]["values"])
                else:
                    raise ImproperlyConfigured(
                        f"Resource '{resource_id}' has invalid type: '{resource_type}'"
                    )
            else:
                raise ImproperlyConfigured(
                    f"Resource '{resource_id}' missing required 'type' property"
                )
        else:
            raise ImproperlyConfigured(f"Resource '{resource_id}' not found")

    def build_postgres_settings(self, resource):
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": resource["name"],
            "USER": resource["username"],
            "PASSWORD": resource["password"],
            "HOST": resource["hostname"],
            "PORT": resource["port"],
        }

    def build_redis_settings(self, resource):
        return {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": resource["url"],
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
                "SOCKET_CONNECT_TIMEOUT": 3,  # in seconds
                "SOCKET_TIMEOUT": 3,  # in seconds
            },
            "KEY_PREFIX": resource["prefix"],
        }

    def build_s3_settings(self, resource):
        return resource["folder"]
