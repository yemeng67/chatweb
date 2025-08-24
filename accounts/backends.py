from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        try:
            user = User.objects.get(email=email)  # 通过 email 查找用户
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None