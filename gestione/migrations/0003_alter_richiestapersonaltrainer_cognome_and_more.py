# Generated by Django 5.1.1 on 2024-10-01 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0002_alter_richiestapersonaltrainer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richiestapersonaltrainer',
            name='cognome',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='richiestapersonaltrainer',
            name='data_di_nascita',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='richiestapersonaltrainer',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]
