import logging
import os

from django.core.exceptions import ImproperlyConfigured

import requests

logger = logging.getLogger(__name__)


class LBResources:
    bridge_endpoint = f"{os.environ.get('LB_CONNECT_API')}/resources"

    def get(self, resource_id=None):
        # Call
        if resource_id:
            response = requests.get(f"{self.bridge_endpoint}/{resource_id}")
        else:
            response = requests.get(self.bridge_endpoint)
        # Check
        if response.status_code == 200:
            try:
                payload = response.json()
            except Exception:
                logger.error("LBResources.get: Unable to decode response JSON")
                return False
            else:
                return payload
        else:
            logger.error(
                f"LBResources.get: Invalid response [code: {response.status_code}]",
            )
            return False

    def settings(self, resource_id):
        """Given a `resource_id`, return an appropriate Django settings dict.

        `resource_id` corresponds to the name of a resource in your launch.yaml file.
        For example, given this config in launch.yaml:

        resources:
          mydatabase:
            type: postgres

        'mydatabase' is the name of the resource to be passed to this method.
        """
        if resource := self.get(resource_id):
            if params := resource.get("params"):
                resource_type = params["type"]
                fname = f"build_{resource_type}_settings"
                if hasattr(self, fname) and callable(func := getattr(self, fname)):
                    return func(params)
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
        return resource["bucket"]
