from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bookings.models import RegistratoUtente, Prenotazione
from datetime import date, datetime

from trainers.models import PersonalTrainer


class TestPrenotazioni(TestCase):

    def setUp(self):
        # Crea un utente di test
        user = User.objects.create_user(username="testuser", password="password")
        self.registrato_utente= RegistratoUtente.objects.create(
            user=user,
            nome="Mario",
            cognome="Rossi",
            data_nascita=date(1990, 1, 1),
            bio="Appassionato di fitness.",
            preferenze="BB"
        )
        self.user = get_user_model().objects.create_user(username='testpt', password='testpass')
        self.personal_trainer = PersonalTrainer.objects.create(user=self.user, nome='Mario', cognome='Verde',
                                                               preferenze='BB', data_di_nascita='1990-01-01')

    def test_crea_prenotazione_success(self):
        # Login utente
        self.client.login(username="testuser", password="password")

        # Simula la creazione di una prenotazione
        response = self.client.post(reverse('bookings:crea_prenotazione'), {
            'personal_trainer': 1,  # ID del PT (deve essere creato precedentemente)
            'data_prenotazione': '2024-10-10',
            'fascia_oraria': 9,  # Aggiungi una fascia oraria valida
        })

        # Verifica se la prenotazione è stata creata e reindirizzata alla pagina di successo
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('bookings:success_page'))

        # Controlla se la prenotazione è stata salvata nel database
        prenotazione = Prenotazione.objects.first()
        self.assertEqual(prenotazione.registrato_utente.user.username, "testuser")

    def test_crea_prenotazione_failure(self):
        # Login utente
        self.client.login(username="testuser", password="password")

        # Simula un errore nella prenotazione (es. mancanza di una fascia oraria valida)
        response = self.client.post(reverse('bookings:crea_prenotazione'), {
            'personal_trainer': 1,  # ID del PT (deve essere creato precedentemente)
            'data_prenotazione': '2024-10-10',
            'fascia_oraria': 0,  # Fascia oraria non valida
        })

        # Verifica che la prenotazione non sia stata creata e la pagina non sia stata redirezionata
        self.assertEqual(response.status_code, 200)  # Ritorna alla pagina del form

    def test_bookings_homepage(self):
        # Login utente
        self.client.login(username="testuser", password="password")

        # Simula la creazione di una prenotazione
        response = self.client.post(reverse('bookings:crea_prenotazione'), {
            'personal_trainer': 1,  # ID del PT (deve essere creato precedentemente)
            'data_prenotazione': '2024-10-10',
            'fascia_oraria': 8,  # Aggiungi una fascia oraria valida
        })

        # Verifica la visualizzazione delle prenotazioni
        response = self.client.get(reverse('bookings:home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '10/10/2024')
        self.assertContains(response, '8:00 - 9:00')

    def test_prenotazione_delete(self):
        # Login utente
        self.client.login(username="testuser", password="password")

        # Simula la creazione di una prenotazione
        response = self.client.post(reverse('bookings:crea_prenotazione'), {
            'personal_trainer': 1,  # ID del PT (deve essere creato precedentemente)
            'data_prenotazione': '2024-10-10',
            'fascia_oraria': 8,  # Aggiungi una fascia oraria valida
        })
        prenotazione = Prenotazione.objects.first()
        # Verifica la cancellazione di una prenotazione
        response = self.client.post(reverse('bookings:prenotazione_delete', args=[prenotazione.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect a success_page
        self.assertFalse(Prenotazione.objects.filter(pk=prenotazione.pk).exists())

    def test_success_page(self):
        response = self.client.get(reverse('bookings:success_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/success.html')

    def test_crea_prenotazione_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse('bookings:crea_prenotazione'))
        self.assertRedirects(response, '/accounts/login/?next=/bookings/prenota/')

    def test_prenotazione_delete_anonymous_user(self):
        # Login utente
        self.client.login(username="testuser", password="password")

        # Simula la creazione di una prenotazione
        response = self.client.post(reverse('bookings:crea_prenotazione'), {
            'personal_trainer': 1,  # ID del PT (deve essere creato precedentemente)
            'data_prenotazione': '2024-10-10',
            'fascia_oraria': 8,  # Aggiungi una fascia oraria valida
        })
        self.client.logout()
        prenotazione = Prenotazione.objects.first()
        response = self.client.post(reverse('bookings:prenotazione_delete', args=[prenotazione.pk]))
        self.assertRedirects(response, '/accounts/login/?next=/bookings/1/delete/')



