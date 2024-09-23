from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import RegistratoUtente
from trainers.models import PersonalTrainer


# Create your models here.
class Prenotazione(models.Model):
    registrato_utente = models.ForeignKey(RegistratoUtente, on_delete=models.CASCADE)
    personal_trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE)

    # Campo per richieste specifiche
    richieste_specifiche = models.TextField(max_length=500, blank=True, null=True)

    # Orario di inizio (le fasce orarie sono di un'ora)
    ORARI_FASCIA = [
        (8, '8:00 - 9:00'),
        (9, '9:00 - 10:00'),
        (10, '10:00 - 11:00'),
        (11, '11:00 - 12:00'),
        (12, '12:00 - 13:00'),
        (13, '13:00 - 14:00'),
        (14, '14:00 - 15:00'),
        (15, '15:00 - 16:00'),
        (16, '16:00 - 17:00'),
        (17, '17:00 - 18:00'),
        (18, '18:00 - 19:00'),
    ]

    fascia_oraria = models.IntegerField(choices=ORARI_FASCIA)
    data_prenotazione = models.DateField()

    class Meta:
        unique_together = ('personal_trainer', 'fascia_oraria', 'data_prenotazione')

    def clean(self):
        # Controllo se c'è già una prenotazione per il personal trainer nella stessa fascia oraria
        if Prenotazione.objects.filter(
                personal_trainer=self.personal_trainer,
                fascia_oraria=self.fascia_oraria,
                data_prenotazione=self.data_prenotazione
        ).exists():
            raise ValidationError("Il personal trainer ha già una prenotazione per questa fascia oraria.")

    def __str__(self):
        return f"Prenotazione di {self.registrato_utente.user.username} con {self.personal_trainer.nome} alle {self.get_fascia_oraria_display()} del {self.data_prenotazione}"

    class Meta:
        verbose_name_plural = "Prenotazioni"