# Generated by Django 4.0.2 on 2022-03-07 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("permissions", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="permissions",
            options={"verbose_name_plural": "Permissions"},
        ),
    ]
