# Generated by Django 3.1.1 on 2020-10-12 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_auto_20201009_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='paper',
            name='doctype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.doctype'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.publication'),
        ),
    ]
