from django.db import models
from django.contrib.auth.models import User
from accounts.models import RegistratoUtente
from trainers.models import PersonalTrainer
# Create your models here.

class Recensione(models.Model):
    registrato_utente = models.ForeignKey(RegistratoUtente, on_delete=models.CASCADE)
    personal_trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE)
    recensione_testuale = models.TextField(max_length=500)

    # Campo per il voto a 5 stelle
    voto = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Voti da 1 a 5 stelle

    data_recensione = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Recensioni"
        constraints = [
            models.UniqueConstraint(fields=['registrato_utente', 'personal_trainer'], name='unique_recensione_per_trainer')
        ]

    def __str__(self):
        return f"Recensione di {self.registrato_utente} per {self.personal_trainer} - {self.voto} stelle"