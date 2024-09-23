# Generated by Django 5.1.1 on 2024-09-23 09:28

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
            name='Prenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('richieste_specifiche', models.TextField(blank=True, max_length=500, null=True)),
                ('fascia_oraria', models.IntegerField(choices=[(8, '8:00 - 9:00'), (9, '9:00 - 10:00'), (10, '10:00 - 11:00'), (11, '11:00 - 12:00'), (12, '12:00 - 13:00'), (13, '13:00 - 14:00'), (14, '14:00 - 15:00'), (15, '15:00 - 16:00'), (16, '16:00 - 17:00'), (17, '17:00 - 18:00'), (18, '18:00 - 19:00')])),
                ('data_prenotazione', models.DateField()),
                ('personal_trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainers.personaltrainer')),
                ('registrato_utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.registratoutente')),
            ],
            options={
                'unique_together': {('personal_trainer', 'fascia_oraria', 'data_prenotazione')},
            },
        ),
    ]
