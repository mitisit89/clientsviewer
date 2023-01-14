import uuid

from django.db import models

# Create your models here.


class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to="images/")


class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, db_index=True)
    surname = models.CharField(max_length=150, db_index=True)
    sex = models.CharField(max_length=10, db_index=True)
    birthday = models.DateTimeField()
    user_photo = models.ForeignKey(UserPhoto, on_delete=models.CASCADE)
