# Generated by Django 3.1.1 on 2020-11-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='custom_title',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
