# Generated by Django 4.0.2 on 2022-02-23 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="staff",
            new_name="is_staff",
        ),
    ]
