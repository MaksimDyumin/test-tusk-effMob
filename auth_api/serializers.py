from rest_framework.serializers import ModelSerializer, CharField, ValidationError, EmailField, Serializer
from django.contrib.auth.hashers import make_password, check_password

from .models import User


class RegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        raw_password = validated_data.pop("password")
        validated_data["password"] = make_password(raw_password)

        return User.objects.create(**validated_data)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError('password do not match confirm_password')
        return attrs
        

class LoginSerializer(ModelSerializer):
    email = EmailField()
    password = CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password']


class UpdateUserSerializer(ModelSerializer):
    password = CharField(write_only=True, required=False)
    email = EmailField(required=False)
    username = CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        if "password" in attrs:
            raise ValidationError({"password": "Password cannot be changed here. Use /auth/change-password/ endpoint."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance
    

class ChangePasswordSerializer(Serializer):
    old_password = CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_new_password = CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        user = self.context['request'].user

        if not check_password(attrs['old_password'], user.password):
            raise ValidationError({"old_password": "Incorrect old password."})

        if attrs['new_password'] != attrs['confirm_new_password']:
            raise ValidationError({"new_password": "New passwords do not match."})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.password = make_password(self.validated_data['new_password'])
        user.save()
        return user
    

class AdminUpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_admin", "is_active"]