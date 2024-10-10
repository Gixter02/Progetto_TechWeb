from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import RegistratoUtente
from bookings.models import Prenotazione
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from trainers.models import PersonalTrainer


class TestAccountsViews(TestCase):

    def setUp(self):
        # Crea un utente di test
        self.user = User.objects.create_user(username='testuser', password='password')
        self.registrato_utente = RegistratoUtente.objects.create(
            user=self.user,
            nome="Mario",
            cognome="Rossi",
            data_nascita=date(1990, 1, 1),
            bio="Appassionato di fitness",
            preferenze="BB"
        )

    def test_home_accounts(self):
        # Fai una richiesta alla homepage degli account
        response = self.client.get(reverse('accounts:home_accounts'))

        # Verifica se lo stato è 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home_page.html')

    def test_lista_utenti_view(self):
        # Login utente come staff
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='password')

        # Fai una richiesta alla lista degli utenti
        response = self.client.get(reverse('accounts:lista_utenti'))

        # Verifica se lo stato è 200 e che l'utente venga visualizzato
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/listautenti.html')
        self.assertContains(response, "Mario Rossi")

    def test_crea_utente_view(self):
        # Verifica che il form sia visualizzato correttamente con una GET
        response = self.client.get(reverse('accounts:creautente'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/creazione_utenti.html')

        # Crea un nuovo utente tramite la view
        response = self.client.post(reverse('accounts:creautente'), {
            'username': 'newuser',
            'password1': 'Bella_raga02',
            'password2': 'Bella_raga02',
        })

        # Verifica che l'utente sia stato creato e si venga rediretti alla pagina di login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

        # Verifica che l'utente esista nel database
        new_user = User.objects.filter(username='newuser')
        self.assertEqual(new_user.count(), 1)

    def test_registrato_utente_create_view(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password1')
        # Login utente
        self.client.login(username='testuser1', password='password1')

        # Crea un RegistratoUtente associato a un nuovo utente
        response = self.client.post(reverse('accounts:inserimento_dati_utente'), {
            'nome': 'Luigi',
            'cognome': 'Verdi',
            'data_nascita': '1985-01-01',
            'bio': 'Nuovo utente di test',
            'preferenze': 'BB',
        })

        # Verifica che l'utente sia stato creato e si venga rediretti alla pagina home degli account
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:home_accounts'))

        # Verifica che il RegistratoUtente esista nel database
        new_registrato_utente = RegistratoUtente.objects.filter(user=self.user1)
        self.assertEqual(new_registrato_utente.count(), 1)
        self.assertEqual(new_registrato_utente.first().nome, 'Luigi')

    def test_allenamenti_utente_view(self):
        self.user = get_user_model().objects.create_user(username='testpt', password='testpasspt')
        self.personal_trainer = PersonalTrainer.objects.create(user=self.user, nome='Mario', cognome='Rossi',
                                                               preferenze='BB', data_di_nascita='1990-01-01')

        # Login utente
        self.client.login(username='testuser', password='password')

        # Crea una prenotazione per l'utente
        prenotazione = Prenotazione.objects.create(
            registrato_utente=self.registrato_utente,
            personal_trainer=self.personal_trainer,
            data_prenotazione=date(2024, 10, 10),
            fascia_oraria=10
        )

        # Fai una richiesta alla pagina degli allenamenti
        response = self.client.get(reverse('accounts:allenamenti_utente'))

        # Verifica che lo stato sia 200 e che la prenotazione venga visualizzata
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/allenamenti_utente.html')
        self.assertContains(response, "10:00 - 11:00")

    def test_registrato_utente_detail_view(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Fai una richiesta alla pagina del profilo dell'utente
        response = self.client.get(reverse('accounts:profilo', args=[self.registrato_utente.pk]))

        # Verifica se lo stato è 200 e che il profilo venga visualizzato
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profilo.html')
        self.assertContains(response, "Mario Rossi")

    def test_registrato_utente_update_view(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Modifica il profilo dell'utente
        response = self.client.post(reverse('accounts:modifica', args=[self.registrato_utente.pk]), {
            'nome': 'Mario',
            'cognome': 'Bianchi',
            'data_nascita': '1990-01-01',
            'bio': 'Aggiornato',
            'preferenze': 'BB',
        })

        # Verifica che l'update sia stato fatto correttamente
        self.assertEqual(response.status_code, 302)
        self.registrato_utente.refresh_from_db()
        self.assertEqual(self.registrato_utente.cognome, 'Bianchi')
        self.assertEqual(self.registrato_utente.bio, 'Aggiornato')


class RegistratoUtenteModelTest(TestCase):

    def setUp(self):
        # Crea un utente di base per i test
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_crea_registrato_utente_success(self):
        # Crea un RegistratoUtente con dati validi
        registrato_utente = RegistratoUtente.objects.create(
            user=self.user,
            nome='Mario',
            cognome='Rossi',
            data_nascita=timezone.now().date(),
            bio='Sono un appassionato di fitness',
            preferenze='BB'  # BodyBuilding
        )

        # Verifica che l'oggetto sia stato creato correttamente
        self.assertEqual(registrato_utente.nome, 'Mario')
        self.assertEqual(registrato_utente.cognome, 'Rossi')
        self.assertEqual(registrato_utente.bio, 'Sono un appassionato di fitness')
        self.assertEqual(registrato_utente.preferenze, 'BB')
        self.assertEqual(registrato_utente.user.username, 'testuser')

    def test_registrato_utente_creation_fails_without_nome(self):
        # Verifica che la creazione fallisca senza il campo 'nome'
        with self.assertRaises(ValidationError):
            registrato_utente = RegistratoUtente(
                user=self.user,
                cognome='Rossi',
                data_nascita=timezone.now().date(),
                bio='Sono un appassionato di fitness',
                preferenze='BB'
            )
            registrato_utente.full_clean()  # Questo deve sollevare un ValidationError
            registrato_utente.save()  # Non deve arrivare a questo punto

    def test_registrato_utente_creation_fails_without_cognome(self):
        # Verifica che la creazione fallisca senza il campo 'cognome'
        with self.assertRaises(ValidationError):
            registrato_utente = RegistratoUtente(
                user=self.user,
                nome='Mario',
                data_nascita=timezone.now().date(),
                bio='Sono un appassionato di fitness',
                preferenze='BB'
            )
            registrato_utente.full_clean()  # Questo deve sollevare un ValidationError
            registrato_utente.save()

    def test_registrato_utente_creation_fails_without_data_nascita(self):
        # Verifica che la creazione fallisca senza il campo 'data_nascita'
        with self.assertRaises(ValidationError):
            registrato_utente = RegistratoUtente(
                user=self.user,
                nome='Mario',
                cognome='Rossi',
                bio='Sono un appassionato di fitness',
                preferenze='BB'
            )
            registrato_utente.full_clean()  # Questo deve sollevare un ValidationError
            registrato_utente.save()

    def test_registrato_utente_creation_fails_without_bio(self):
        # Verifica che la creazione fallisca senza il campo 'bio'
        with self.assertRaises(ValidationError):
            registrato_utente = RegistratoUtente(
                user=self.user,
                nome='Mario',
                cognome='Rossi',
                data_nascita=timezone.now().date(),
                preferenze='BB'
            )
            registrato_utente.full_clean()  # Questo deve sollevare un ValidationError
            registrato_utente.save()

    def test_registrato_utente_creation_fails_without_preferenze(self):
        # Verifica che la creazione fallisca senza il campo 'preferenze'
        with self.assertRaises(ValidationError):
            registrato_utente = RegistratoUtente(
                user=self.user,
                nome='Mario',
                cognome='Rossi',
                data_nascita=timezone.now().date(),
                bio='Sono un appassionato di fitness',
            )
            registrato_utente.full_clean()  # Questo deve sollevare un ValidationError
            registrato_utente.save()

    def test_registrato_utente_str_representation(self):
        # Testa la rappresentazione in stringa del modello
        registrato_utente = RegistratoUtente.objects.create(
            user=self.user,
            nome='Mario',
            cognome='Rossi',
            data_nascita=timezone.now().date(),
            bio='Sono un appassionato di fitness',
            preferenze='BB'
        )
        self.assertEqual(str(registrato_utente),
                         f'Mario Rossi nato il {registrato_utente.data_nascita}\nPreferenze: BB\nBIO: Sono un appassionato di fitness')
