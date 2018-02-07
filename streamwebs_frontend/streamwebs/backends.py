from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        userField = UserModel.USERNAME_FIELD

        if username is None:
            username = kwargs.get(userField)

        # Login with email address
        if '@' in username:
            userField = UserModel.EMAIL_FIELD

        try:
            case_insensitive_username = '{}__iexact'.format(userField)

            user = UserModel._default_manager.get(
                **{case_insensitive_username: username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            # This can stop potential attacks by taking the same time to login
            # for an existing user as for a non existing user
            UserModel().set_password(password)
        else:
            if user.check_password(password) and\
               self.user_can_authenticate(user):
                return user
