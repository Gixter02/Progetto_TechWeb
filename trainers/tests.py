from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from trainers.models import PersonalTrainer
from accounts.models import RegistratoUtente
from bookings.models import Prenotazione
from django.utils import timezone

class PersonalTrainerUpdateViewTest(TestCase):

    def setUp(self):
        # Crea un utente di test e un personal trainer
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.personal_trainer = PersonalTrainer.objects.create(user=self.user, nome='Mario', cognome='Rossi', preferenze='BB', data_di_nascita='1990-01-01')

    def test_update_view_access(self):
        # Verifica se l'utente autenticato può accedere alla vista di modifica
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('trainers:personal_trainer_update', args=[self.personal_trainer.pk]))
        self.assertEqual(response.status_code, 200)

    def test_update_view_non_authenticated(self):
        # Verifica se un utente non autenticato non può accedere alla vista di modifica
        response = self.client.get(reverse('trainers:personal_trainer_update', args=[self.personal_trainer.pk]))
        self.assertRedirects(response, '/accounts/login/?next=/trainers/1/edit/')



class PersonalTrainerHomeViewTest(TestCase):

    def setUp(self):
        # Crea un utente e un personal trainer
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.personal_trainer = PersonalTrainer.objects.create(user=self.user, nome='Mario', cognome='Rossi', preferenze='BB', data_di_nascita='1990-01-01')

    def test_personal_trainer_home_view(self):
        # Verifica che l'utente possa accedere alla pagina home del personal trainer
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('trainers:personal_trainer_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mario Rossi')

class AllenamentiProgrammatiViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.personal_trainer = PersonalTrainer.objects.create(user=self.user, nome='Mario', cognome='Rossi', preferenze='BB', data_di_nascita='1990-01-01')
        self.registrato_utente = RegistratoUtente.objects.create(user=self.user, nome='Luigi', cognome='Verdi', preferenze='PL', data_nascita='2000-01-01')
        self.prenotazione = Prenotazione.objects.create(registrato_utente=self.registrato_utente, personal_trainer=self.personal_trainer, fascia_oraria=9, data_prenotazione=timezone.now().date())

    def test_view_allenamenti(self):
        # Verifica se l'allenamento programmato è visibile per il personal trainer
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('trainers:allenamenti_programmati'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '9:00 - 10:00')


class DisponibilitaPersonalTrainerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.personal_trainer = PersonalTrainer.objects.create(user=self.user, nome='Mario', cognome='Rossi', preferenze='BB', data_di_nascita='1990-01-01')

    def test_disponibilita_view(self):
        # Verifica se l'utente può accedere alla vista disponibilità personal trainer
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('trainers:disponibilita_personal_trainer', args=[self.personal_trainer.pk]))
        self.assertEqual(response.status_code, 200)


class ElencoPersonalTrainersTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='testuser1', password='testpass1')
        self.personal_trainer1 = PersonalTrainer.objects.create(user=self.user1, nome='Mario', cognome='Rossi', preferenze='BB', data_di_nascita='1990-01-01')
        self.user2 = get_user_model().objects.create_user(username='testuser2', password='testpass2')
        self.personal_trainer2 = PersonalTrainer.objects.create(user=self.user2, nome='Luigi', cognome='Verdi', preferenze='PL', data_di_nascita='1992-01-01')

    def test_elenco_personal_trainers_ordinato(self):
        # Testa la visualizzazione dei personal trainer ordinati per media voto
        response = self.client.get(reverse('trainers:elenco_personal_trainers_ordinato'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mario Rossi')
