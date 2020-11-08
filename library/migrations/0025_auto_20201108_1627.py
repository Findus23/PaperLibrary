# Generated by Django 3.1.1 on 2020-11-08 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0024_auto_20201108_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='citation_key',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='notes', to='library.Tag'),
        ),
    ]
