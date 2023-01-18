import uuid
from typing import Optional

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(
            self,
            name: str,
            email: str,
            sex:str,
            surname:str,
            birthday,

            password: Optional[str] = None,
    ) -> "User":
        if name is None:
            raise TypeError("Users must have a username.")
        if email is None:
            raise TypeError("Users must have an email address")
        user = self.model(
            name=name, email=self.normalize_email(email), birthday=birthday,sex=sex,surname=surname
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name: str, email: str, password: str) -> "User":
        if password is None:
            raise TypeError("Superusers must have a password.")
        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=150, db_index=True)
    surname = models.CharField(max_length=150, db_index=True)
    sex = models.CharField(max_length=10, db_index=True)
    birthday = models.DateField()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserManager()

    @property
    def tokens(self) -> dict[str, str]:
        refresh_token = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
        }


class UserPhoto(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    photo = models.ImageField()
