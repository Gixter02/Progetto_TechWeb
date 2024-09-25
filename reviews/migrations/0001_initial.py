# Generated by Django 5.1.1 on 2024-09-23 14:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_rename_regitratoutente_registratoutente'),
        ('trainers', '0004_remove_personaltrainer_certificati_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recensione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recensione_testuale', models.TextField(max_length=500)),
                ('voto', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('data_recensione', models.DateTimeField(auto_now_add=True)),
                ('personal_trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainers.personaltrainer')),
                ('registrato_utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.registratoutente')),
            ],
            options={
                'verbose_name_plural': 'Recensioni',
            },
        ),
    ]