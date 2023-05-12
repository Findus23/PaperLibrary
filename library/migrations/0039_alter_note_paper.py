# Generated by Django 4.2.1 on 2023-05-12 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0038_note_remove_paper_notes_html_remove_paper_notes_md"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="paper",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="note",
                serialize=False,
                to="library.paper",
            ),
        ),
    ]
