from django.db import models

# Create your models here.

class Utente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    data_nascita = models.DateField()
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

    def __str__(self):
        return self.nome + self.cognome + " nato il " + str(self.data_nascita) + "\nPreferenze: " + self.preferenze + "\nBIO: " + self.bio

    class Meta:
        verbose_name_plural = "Utenti"