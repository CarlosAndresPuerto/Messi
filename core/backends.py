from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class IdentityBackend(ModelBackend):

    def authenticate(self, request, identity=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(identity=identity)  # Buscar por identity
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None