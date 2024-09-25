# Generated by Django 5.1.1 on 2024-09-25 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_regitratoutente_registratoutente'),
        ('reviews', '0002_alter_recensione_unique_together'),
        ('trainers', '0004_remove_personaltrainer_certificati_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recensione',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='recensione',
            constraint=models.UniqueConstraint(fields=('registrato_utente', 'personal_trainer'), name='unique_recensione_per_trainer'),
        ),
    ]