# Generated by Django 4.2.1 on 2023-06-27 13:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0043_alter_paper_arxiv_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paper",
            name="abstract",
            field=models.TextField(null=True),
        ),
    ]
