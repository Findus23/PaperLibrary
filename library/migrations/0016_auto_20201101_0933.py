# Generated by Django 3.1.1 on 2020-11-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_note_custom_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='notes_html',
            field=models.TextField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='note',
            name='notes_md',
            field=models.TextField(blank=True),
        ),
    ]
