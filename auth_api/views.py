from django.contrib.auth.hashers import make_password, check_password

from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import (RegistrationSerializer, LoginSerializer, 
                          UpdateUserSerializer, ChangePasswordSerializer, 
                          AdminUpdateUserSerializer)
from .models import User
from .jwt_utils import generate_jwt


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed("User not found")
        
        if not user.is_active:
            raise AuthenticationFailed("User is deactivated")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Incorrect password")

        token = generate_jwt(user)

        return Response({"token": token})


class UpdateAccountView(UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        return Response({"message": "Account deactivated"})
    

class AdminUpdateUserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=user.id)