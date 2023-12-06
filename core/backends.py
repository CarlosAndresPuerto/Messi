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

        # Comprobamos la contraseña dependiendo del tipo de usuario
        if user.is_teacher and user.check_password(user.teacher_password):
            print("Teacher authentication successful")
            return user
        elif not user.is_teacher and user.check_password(password):
            print("Student authentication successful")
            return user
        else:
            print("Authentication failed")
            return None
