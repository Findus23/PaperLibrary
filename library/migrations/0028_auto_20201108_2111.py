# Generated by Django 3.1.1 on 2020-11-08 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0027_auto_20201108_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='arxiv_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
