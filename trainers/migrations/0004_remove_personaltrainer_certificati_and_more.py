# Generated by Django 5.1.1 on 2024-09-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0003_alter_certificato_personal_trainer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaltrainer',
            name='certificati',
        ),
        migrations.AddField(
            model_name='personaltrainer',
            name='competenze',
            field=models.TextField(default='Nessuna competenza', max_length=500),
        ),
        migrations.DeleteModel(
            name='Certificato',
        ),
    ]