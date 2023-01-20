from abc import ABC

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User, UserPhoto
from .utils import email_is_valid


class UserListSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField()
    surname = serializers.CharField()
    sex = serializers.CharField
    birthday = serializers.DateField()
    photo = serializers.CharField()
    read_only_fields = ["id"]



class RegistrationUserSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    photo = serializers.ImageField(write_only=True, use_url=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "surname", "sex", "birthday", "photo"]

    def validate_email(self, value: str) -> str:
        valid, error_txt = email_is_valid(value)
        if not valid:
            raise serializers.ValidationError(error_txt)
        try:
            email_name, domain_part = value.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            value = "@".join([email_name, domain_part.lower()])
        return value

    def create(self, validated_data) -> "User":
        user = User.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
            birthday=validated_data["birthday"],
            surname=validated_data.get("surname", ""),
            sex=validated_data.get("sex", ""),
        )
        photo = UserPhoto.objects.create(
            user=user, photo=validated_data.get("photo", "")
        )
        return user


class LoginSerializer(serializers.ModelSerializer[User]):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj) -> dict[str, str]:
        user = User.objects.get(email=obj.email)
        return {"refresh": user.tokens["refresh"], "access": user.tokens["access"]}

    class Meta:
        model = User
        fields = ["email", "name", "password", "tokens"]

    def validate(self, data: dict[str, str]):
        email = data.get("email", None)
        password = data.get("password", None)
        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")
        if password is None:
            raise serializers.ValidationError("A password is required to log in")
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("A user with this email and password was not found")
        if not user.is_active:
            raise serializers.ValidationError("This user is not currently activated.")
        return user


class UserSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    photo=serializers.ImageField(write_only=True,use_url=True)
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "password",
            "tokens",
            "surname",
            "sex",
            "birthday",
            "photo",
            "is_staff",
        ]
        read_only_fields = ("tokens", "if_staff")

    def update(self, instanse: User, validated_data):
        password = validated_data.pop("password", None)
        print(validated_data)
        photo=validated_data.pop('photo',None)
        print(photo)
        for (key, value) in validated_data.items():
            setattr(instanse, key, value)

        if password is not None:
            instanse.set_password(password)
        if photo is not None:
            UserPhoto.objects.filter(user=instanse).update(photo=photo)
        instanse.save()
        return instanse


class DeleteSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = "_all_"


class LogoutSerializer(serializers.Serializer[User]):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            raise AuthenticationFailed(e)
