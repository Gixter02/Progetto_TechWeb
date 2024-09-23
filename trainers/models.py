from django.db import models
from django.contrib.auth.models import User

# Funzione per definire il percorso dinamico per l'immagine del profilo
def foto_profilo_upload_path(instance, filename):
    # Salva l'immagine nella directory 'trainer_foto_profilo/<user_id>/<filename>'
    return f'trainer_foto_profilo/{instance.user.id}/{filename}'

class PersonalTrainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    data_di_nascita = models.DateField()
    bio = models.TextField(max_length=500)

    SCELTA_PREFERENZE = [
        ("BB", "BodyBuilding"),
        ("PL", "PowerLifting"),
        ("CL", "Calisthenics"),
        ("ST", "StrongMen"),
        ("YG", "Yoga"),
        ("PS", "Pilates"),
        ("AR", "Aerobico")
    ]
    preferenze = models.CharField(max_length=2, choices=SCELTA_PREFERENZE)

    # Campo immagine del profilo con percorso dinamico
    immagine_profilo = models.ImageField(upload_to=foto_profilo_upload_path, blank=True, null=True)
    competenze = models.TextField(max_length=500, default='Nessuna competenza')

    def __str__(self):
        return f"{self.nome} {self.cognome} - Preferenza: {self.get_preferenze_display()}"

    class Meta:
        verbose_name = "Personal Trainer"
        verbose_name_plural = "Personal Trainers"