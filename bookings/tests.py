from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from bookings.models import Prenotazione
from accounts.models import RegistratoUtente
from django.core.exceptions import ValidationError
from datetime import timedelta


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
            'data_prenotazione': timezone.now().date() + timedelta(days=1),
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
            'data_prenotazione': timezone.now().date() + timedelta(days=1),
            'fascia_oraria': 0,  # Fascia oraria non valida
        })

        # Verifica che la prenotazione non sia stata creata e la pagina non sia stata redirezionata
        self.assertEqual(response.status_code, 200)  # Ritorna alla pagina del form

    def test_bookings_homepage(self):
        # Login utente
        self.client.login(username="testuser", password="password")
        data_futura = timezone.now().date() + timedelta(days=1)
        # Simula la creazione di una prenotazione
        response = self.client.post(reverse('bookings:crea_prenotazione'), {
            'personal_trainer': 1,  # ID del PT (deve essere creato precedentemente)
            'data_prenotazione': data_futura,
            'fascia_oraria': 8,  # Aggiungi una fascia oraria valida
        })

        # Verifica la visualizzazione delle prenotazioni
        response = self.client.get(reverse('bookings:home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'{data_futura.day}/{data_futura.month}/{data_futura.year}')
        self.assertContains(response, '8:00 - 9:00')

    def test_prenotazione_delete(self):
        # Login utente
        self.client.login(username="testuser", password="password")

        # Simula la creazione di una prenotazione
        response = self.client.post(reverse('bookings:crea_prenotazione'), {
            'personal_trainer': 1,  # ID del PT (deve essere creato precedentemente)
            'data_prenotazione': timezone.now().date() + timedelta(days=1),
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
            'data_prenotazione': timezone.now().date() + timedelta(days=1),
            'fascia_oraria': 8,  # Aggiungi una fascia oraria valida
        })
        self.client.logout()
        prenotazione = Prenotazione.objects.first()
        response = self.client.post(reverse('bookings:prenotazione_delete', args=[prenotazione.pk]))
        self.assertRedirects(response, '/accounts/login/?next=/bookings/1/delete/')


class PrenotazioneModelTest(TestCase):

    def setUp(self):
        # Crea utenti e personal trainers di base per i test
        self.user1 = User.objects.create_user(username='utente1', password='testpass')
        self.user2 = User.objects.create_user(username='utente2', password='testpass')

        self.registrato_utente1 = RegistratoUtente.objects.create(
            user=self.user1,
            nome='Mario',
            cognome='Rossi',
            data_nascita=timezone.now().date() - timedelta(days=8000),
            bio='Sono un appassionato di fitness',
            preferenze='BB'
        )
        self.registrato_utente2 = RegistratoUtente.objects.create(
            user=self.user2,
            nome='Luigi',
            cognome='Verdi',
            data_nascita=timezone.now().date() - timedelta(days=9000),
            bio='Appassionato di yoga',
            preferenze='YG'
        )

        self.personal_trainer1 = PersonalTrainer.objects.create(
            user=self.user1,
            nome='Giovanni',
            cognome='Bianchi',
            data_di_nascita=timezone.now().date() - timedelta(days=12000),
            bio='Esperto in bodybuilding',
            competenze='BodyBuilding',
            preferenze='BB'
        )

    def test_crea_prenotazione_success(self):
        # Crea una prenotazione con dati validi
        futura_data = timezone.now().date() + timedelta(days=1)
        prenotazione = Prenotazione.objects.create(
            registrato_utente=self.registrato_utente1,
            personal_trainer=self.personal_trainer1,
            fascia_oraria=9,  # 9:00 - 10:00
            data_prenotazione=futura_data
        )

        # Verifica che la prenotazione sia stata creata correttamente
        self.assertEqual(prenotazione.registrato_utente, self.registrato_utente1)
        self.assertEqual(prenotazione.personal_trainer, self.personal_trainer1)
        self.assertEqual(prenotazione.fascia_oraria, 9)
        self.assertEqual(prenotazione.data_prenotazione, futura_data)

    def test_prenotazione_fail_data_passata(self):
        # Verifica che non sia possibile creare una prenotazione per una data passata
        data_passata = timezone.now().date() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            prenotazione = Prenotazione(
                registrato_utente=self.registrato_utente1,
                personal_trainer=self.personal_trainer1,
                fascia_oraria=9,
                data_prenotazione=data_passata
            )
            prenotazione.full_clean()  # Deve sollevare ValidationError

    def test_prenotazione_fail_data_odierna(self):
        # Verifica che non sia possibile creare una prenotazione per la data odierna
        data_odierna = timezone.now().date()
        with self.assertRaises(ValidationError):
            prenotazione = Prenotazione(
                registrato_utente=self.registrato_utente1,
                personal_trainer=self.personal_trainer1,
                fascia_oraria=10,
                data_prenotazione=data_odierna
            )
            prenotazione.full_clean()  # Deve sollevare ValidationError

    def test_prenotazione_fail_fascia_oraria_occupata(self):
        # Crea una prima prenotazione
        futura_data = timezone.now().date() + timedelta(days=2)
        Prenotazione.objects.create(
            registrato_utente=self.registrato_utente1,
            personal_trainer=self.personal_trainer1,
            fascia_oraria=9,
            data_prenotazione=futura_data
        )

        # Verifica che non sia possibile creare un'altra prenotazione nella stessa fascia oraria per lo stesso trainer
        with self.assertRaises(ValidationError):
            prenotazione = Prenotazione(
                registrato_utente=self.registrato_utente2,  # Utente diverso
                personal_trainer=self.personal_trainer1,
                fascia_oraria=9,
                data_prenotazione=futura_data
            )
            prenotazione.full_clean()  # Deve sollevare ValidationError

    def test_str_representation(self):
        # Verifica la rappresentazione in stringa del modello Prenotazione
        futura_data = timezone.now().date() + timedelta(days=3)
        prenotazione = Prenotazione.objects.create(
            registrato_utente=self.registrato_utente1,
            personal_trainer=self.personal_trainer1,
            fascia_oraria=10,
            data_prenotazione=futura_data
        )
        self.assertEqual(
            str(prenotazione),
            f"Prenotazione di {self.registrato_utente1.user.username} con {self.personal_trainer1.nome} alle 10:00 - 11:00 del {futura_data}"
        )
