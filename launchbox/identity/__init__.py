import logging
import os

import requests

logger = logging.getLogger(__name__)


class LBIdentity:
    def __init__(self, plugin_id):
        self.endpoint = f"{os.environ.get('LB_CONNECT_API')}/identity/{plugin_id}"
        self.user = LBIdentity.user(self.endpoint)
        self.group = LBIdentity.group(self.endpoint)

    class user:
        def __init__(self, endpoint):
            self.endpoint = endpoint

        def get(self, user_id):
            # Call
            response = requests.get(f"{self.endpoint}/user/{user_id}")
            # Check
            if response.status_code == 200:
                try:
                    payload = response.json()
                except Exception:
                    logger.error("LBIdentity.get: Unable to decode response JSON")
                    return False
                else:
                    return payload
            else:
                logger.error(
                    f"LBIdentity.get: Invalid response [code: {response.status_code}]",
                )
                return False

        def groups(self, user_id):
            # Call
            response = requests.get(f"{self.endpoint}/user/{user_id}/groups")
            # Check
            if response.status_code == 200:
                try:
                    payload = response.json()
                except Exception:
                    logger.error("LBIdentity.get: Unable to decode response JSON")
                    return False
                else:
                    return payload
            else:
                logger.error(
                    f"LBIdentity.get: Invalid response [code: {response.status_code}]",
                )
                return False

        def search(self, query):
            # Call
            response = requests.get(f"{self.endpoint}/search/{query}")
            # Check
            if response.status_code == 200:
                try:
                    payload = response.json()
                except Exception:
                    logger.error("LBIdentity.get: Unable to decode response JSON")
                    return False
                else:
                    return payload
            else:
                logger.error(
                    f"LBIdentity.get: Invalid response [code: {response.status_code}]",
                )
                return False

    class group:
        def __init__(self, endpoint):
            self.endpoint = endpoint

        def get(self, group_id):
            # Call
            response = requests.get(f"{self.endpoint}/group/{group_id}")
            # Check
            if response.status_code == 200:
                try:
                    payload = response.json()
                except Exception:
                    logger.error("LBIdentity.get: Unable to decode response JSON")
                    return False
                else:
                    return payload
            else:
                logger.error(
                    f"LBIdentity.get: Invalid response [code: {response.status_code}]",
                )
                return False
