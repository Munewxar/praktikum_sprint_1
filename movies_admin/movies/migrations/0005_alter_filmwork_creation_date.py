# Generated by Django 4.2.5 on 2023-09-13 13:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_rename_created_filmwork_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filmwork",
            name="creation_date",
            field=models.DateField(blank=True, verbose_name="Creation date"),
        ),
    ]