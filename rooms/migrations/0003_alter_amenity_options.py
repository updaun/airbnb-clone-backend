# Generated by Django 3.2 on 2022-11-24 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_auto_20221124_0347"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="amenity",
            options={"verbose_name_plural": "Amenities"},
        ),
    ]
