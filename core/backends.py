# core/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class IdentityBackend(ModelBackend):

    def authenticate(self, request, identity=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(identity=identity)
        except UserModel.DoesNotExist:
            return None

        print(f"User: {user.username}, Is Teacher: {user.is_teacher}")

        # Verificar la contraseña
        if user.check_password(password):
            print("Password is correct")

            # Comprobar si el usuario es profesor
            if user.is_teacher:
                print("Teacher authentication successful")
                return user
            else:
                print("Student authentication successful")
                return user

        print("Authentication failed")
        return None
