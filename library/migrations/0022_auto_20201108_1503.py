# Generated by Django 3.1.1 on 2020-11-08 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0021_author_pretty_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(editable=False, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='paper',
            name='tags',
            field=models.ManyToManyField(related_name='papers', to='library.Tag'),
        ),
    ]
