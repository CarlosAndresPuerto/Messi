# core/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from core.models import Teacher

class IdentityBackend(ModelBackend):

    def authenticate(self, request, identity=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(identity=identity)
        except UserModel.DoesNotExist:
            return None

        print(f"User: {user.username}, Is Teacher: {user.is_teacher if hasattr(user, 'is_teacher') else False}")

        # Comprobar si el usuario es profesor
        if hasattr(user, 'is_teacher') and user.is_teacher:
            try:
                teacher = user.teacher
                if teacher and teacher.approved_by_admin and user.check_password(password):
                    print("Teacher authentication successful")
                    return user
                else:
                    print("Teacher authentication failed")
                    return None
            except Teacher.DoesNotExist:
                print("Teacher authentication failed (no associated Teacher object)")
                return None
        elif not hasattr(user, 'is_teacher') and not user.is_teacher and user.check_password(password):
            print("Student authentication successful")
            return user
        else:
            print("Authentication failed")
            return None
