# Generated by Django 3.1.1 on 2020-11-08 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0028_auto_20201108_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='preview',
            field=models.FileField(blank=True, null=True, upload_to='previews'),
        ),
    ]
