from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import (CharField, ImageField, ModelSerializer,
                                        Serializer, SerializerMethodField,
                                        ValidationError)
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import UserModel
from .utils import email_is_valid


class RegistrationUserModelSerializer(ModelSerializer[UserModel]):
    password = CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = UserModel
        fields = (
            "email",
            "name",
            "password",
            "surname",
            "sex",
            "birthday",
            "user_photo",
            )

    def validate_email(self, value: str) -> str:
        print(value)
        valid, error_txt = email_is_valid(value)
        if not valid:
            raise ValidationError(error_txt)
        try:
            email_name, domain_part = value.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            value = "@".join([email_name, domain_part.lower()])
        return value

    def create(self, validated_data) -> "UserModel":
        print(validated_data)
        user = UserModel.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.surname = validated_data.get("surname", "")
        user.sex = validated_data.get("sex", "")
        user.birthday = validated_data['birthday']
        # user.user_photo = validated_data.get("user_photo",'')
        return user


class LoginUserModelSerializer(ModelSerializer[UserModel]):
    email = CharField(max_length=255)
    name = CharField(max_length=255, read_only=True)
    password = CharField(max_length=128, write_only=True)
    tokens = SerializerMethodField()

    def get_tokens(self, obj) -> dict[str, str]:
        user = UserModel.objects.get(email=obj.email)
        return {"refresh": user.tokens["refresh"], "access": user.tokens["access"]}

    class Meta:
        model = UserModel
        fields = ["email", "name", "password", "tokens"]

    def validate(self, data: dict[str, str]):
        email = data.get("email", None)
        password = data.get("password", None)
        if email is None:
            raise ValidationError("An email address is required to log in.")
        user = authenticate(username=email, password=password)
        if user is None:
            raise ValidationError("A user with this email and password was not found")
        if not user.is_active:
            raise ValidationError("This user is not currently activated.")
        return user


class UserModelSerializer(ModelSerializer[UserModel]):
    password = CharField(max_length=128, min_length=8, write_only=True)
    user_photo = ImageField(source="user_photo.photo")

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "name",
            "password",
            "tokens",
            "surname",
            "sex",
            "birthday",
            "user_photo",
            "is_staff",
        )
        read_only_fields = ("tokens", "if_staff")

    def update(self, instanse: UserModel, validated_data):
        password = validated_data.pop("password", None)
        for (key, value) in validated_data.items():
            setattr(instanse, key, value)

        if password is not None:
            instanse.set_password(password)
        instanse.save()
        return instanse


class LogoutSerializer(Serializer[UserModel]):
    refresh = CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            raise AuthenticationFailed(e)
