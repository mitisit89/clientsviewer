# Generated by Django 4.1.5 on 2023-01-21 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userinfo", "0002_alter_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="user",
            name="sex",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="user",
            name="surname",
            field=models.CharField(max_length=150),
        ),
    ]
