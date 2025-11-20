import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import User

class CustomJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None
        
        try:
            prefix, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid token header")

        if prefix.lower() != "bearer":
            raise AuthenticationFailed("Authorization header must start with Bearer")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user = User.objects.filter(id=payload["user_id"]).first()
        
        if not user:
            raise AuthenticationFailed("User not found")
        
        if not user.is_active:
            raise AuthenticationFailed("User is deactivated")

        return (user, token)