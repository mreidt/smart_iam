# Generated by Django 4.0.2 on 2022-03-15 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_customuser_groups_customuser_user_permissions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="admin",
        ),
        migrations.AddField(
            model_name="useraccount",
            name="admin",
            field=models.BooleanField(default=False),
        ),
    ]
