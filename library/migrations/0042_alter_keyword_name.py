# Generated by Django 4.2.1 on 2023-06-25 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0041_alter_keyword_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="keyword",
            name="name",
            field=models.CharField(max_length=1000),
        ),
    ]
