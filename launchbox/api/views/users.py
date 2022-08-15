from django.conf import settings
from django.contrib.auth import get_user_model

# TODO: Change from mocked LBMgmtAPI to the real thing when available.
from ..utils import LBMgmtAPI, LBServiceAPI

USER_MODEL = get_user_model()


class Users:
    if hasattr(settings, "LB_USER_ATTRIBUTES"):
        attributes = settings.LB_USER_ATTRIBUTES
    else:
        attributes = ["first_name", "last_name", "email"]

    @staticmethod
    def parse(user):
        return {attr: getattr(user, attr) for attr in Users.attributes}

    @staticmethod
    def create(request):
        data = LBServiceAPI.request.json(request)
        if username := data.get("username"):
            # If using SSO, validate username
            if LBMgmtAPI.dir and not LBMgmtAPI.dir.user.get(username):
                return LBServiceAPI.response.error("invalid username")
            # Verify user does not exist
            if USER_MODEL.objects.filter(username=username).exists():
                return LBServiceAPI.response.error("user already exists")

            # Create user
            user = USER_MODEL.user(username)
            # Result
            result = {username: Users.parse(user)}
            return LBServiceAPI.response.json(result)
        return LBServiceAPI.response.invalid()

    @staticmethod
    def delete(request):
        data = LBServiceAPI.request.json(request)
        if username := data.get("username"):
            # Get user object and delete
            result = USER_MODEL.objects.filter(username=username).delete()
            # Check number of objects deleted
            if result[0] > 0:
                # Result
                return LBServiceAPI.response.json({username: "deleted"})
            else:
                # Error
                return LBServiceAPI.response.error("user does not exist")
        return LBServiceAPI.response.invalid()

    @staticmethod
    def read(request):
        params = LBServiceAPI.request.params(request)
        if username := params.get("username"):
            # Specific user
            users = USER_MODEL.objects.filter(username=username)
        else:
            # All users
            users = USER_MODEL.objects.all()
        # Result
        results = {user.username: Users.parse(user) for user in users}
        return LBServiceAPI.response.json(results)

    @staticmethod
    def update(request):
        # Format: dict (key: username, value: dict (user attr: value))
        # Example: {"jsmith": {"is_editor": true}}
        data = LBServiceAPI.request.json(request)
        if users := data.get("users"):
            # Verify type
            if type(users) is dict:
                # Prepare
                results = {}
                # Update
                for username, delta in users.items():
                    try:
                        # Get user
                        user = USER_MODEL.objects.get(username=username)
                        # Prepare
                        results[username] = {}
                        # Attributes
                        for attr, value in delta.items():
                            # Validate that the given attribute can be updated
                            if attr in Users.attributes and hasattr(user, attr):
                                # Update value
                                setattr(user, attr, value)
                                results[username][attr] = "updated"
                            else:
                                # Invalid attribute
                                results[username][attr] = "invalid"
                        # Save user
                        user.save()
                    except USER_MODEL.DoesNotExist:
                        results[username] = "not found"
                    except Exception:
                        results[username] = "error"
                # Result
                return LBServiceAPI.response.json(results)
        return LBServiceAPI.response.invalid()
