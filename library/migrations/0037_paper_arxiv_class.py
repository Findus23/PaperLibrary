# Generated by Django 4.2.1 on 2023-05-11 15:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0036_paper_ads_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="paper",
            name="arxiv_class",
            field=models.CharField(null=True),
        ),
    ]