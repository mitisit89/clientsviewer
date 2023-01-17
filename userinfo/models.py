import uuid
from typing import Optional

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken



class UserModelManager(BaseUserManager):
    def create_user(
        self,
        name: str,
        email: str,
        birthday,
        user_photo,
        password: Optional[str] = None,
    ) -> "UserModel":
        if name is None:
            raise TypeError("Users must have a username.")
        if email is None:
            raise TypeError("Users must have an email address")
        user = self.model(
            name=name, email=self.normalize_email(email), birthday=birthday,user_photo=user_photo
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name: str, email: str, password: str) -> "UserModel":
        if password is None:
            raise TypeError("Superusers must have a password.")
        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField()



class UserModel(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=150, db_index=True)
    surname = models.CharField(max_length=150, db_index=True)
    sex = models.CharField(max_length=10, db_index=True)
    birthday = models.DateField()
    user_photo = models.ForeignKey(UserPhoto, on_delete=models.CASCADE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserModelManager()
    
    @property
    def tokens(self) -> dict[str, str]:
        refresh_token = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
        }
