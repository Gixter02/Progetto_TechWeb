from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import RegistratoUtente
from trainers.models import PersonalTrainer
from reviews.models import Recensione
from datetime import date
from django.core.exceptions import ValidationError


class TestRecensioniViews(TestCase):

    def setUp(self):
        # Crea utente di test
        self.user = User.objects.create_user(username='testuser', password='password')
        self.registrato_utente = RegistratoUtente.objects.create(
            user=self.user,
            nome="Mario",
            cognome="Rossi",
            data_nascita=date(1990, 1, 1),
            bio="Appassionato di fitness",
            preferenze="BB"
        )
        self.user1 = User.objects.create_user(username='testuser1', password='password1')
        # Crea un personal trainer
        self.personal_trainer = PersonalTrainer.objects.create(
            user=self.user1,
            nome='Luca',
            cognome='Bianchi',
            preferenze='BB',
            data_di_nascita='1990-01-01'
        )

        # Crea una recensione
        self.recensione = Recensione.objects.create(
            registrato_utente=self.registrato_utente,
            personal_trainer=self.personal_trainer,
            recensione_testuale="Ottimo allenatore",
            voto=5,
            data_recensione=date(2024, 10, 5)
        )
        self.user2 = User.objects.create_user(username='testuser2', password='password2')
        # Crea un personal trainer
        self.personal_trainer1 = PersonalTrainer.objects.create(
            user=self.user2,
            nome='Bella',
            cognome='Raga',
            preferenze='YG',
            data_di_nascita='1990-01-01'
        )

    def test_homepage_recensioni(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Fai una richiesta alla homepage delle recensioni
        response = self.client.get(reverse('reviews:homepage_recensioni'))

        # Verifica se lo stato è 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/home_recensioni.html')

    def test_crea_recensione_success(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Crea una recensione per il personal trainer
        response = self.client.post(
            reverse('reviews:crea_recensione') + f'?personal_trainer={self.personal_trainer1.id}', {
                'recensione_testuale': 'Molto bravo',
                'voto': 5,
            })

        # Verifica che la recensione sia stata creata e si viene rediretti alla pagina di successo
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('reviews:review_success'))

        # Verifica che la recensione sia stata creata nel database
        nuova_recensione = Recensione.objects.filter(registrato_utente=self.registrato_utente,
                                                     personal_trainer=self.personal_trainer1)
        self.assertEqual(nuova_recensione.count(), 1)
        self.assertEqual(nuova_recensione.first().voto, 5)

    def test_crea_recensione_duplicate(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Tenta di creare una recensione per lo stesso personal trainer (dovrebbe fallire)
        response = self.client.post(
            reverse('reviews:crea_recensione') + f'?personal_trainer={self.personal_trainer.id}', {
                'recensione_testuale': 'Recensione duplicata',
                'voto': 5,
            })

        # Verifica che il messaggio di errore venga mostrato
        self.assertEqual(response.status_code, 200)  # Rimane sulla pagina di recensione

    def test_review_list_view(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Fai una richiesta alla lista delle recensioni dell'utente
        response = self.client.get(reverse('reviews:lista_recensioni'))

        # Verifica che la risposta sia 200 e che la recensione dell'utente appaia
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ottimo allenatore")

    def test_recensione_update_view(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Modifica la recensione
        response = self.client.post(reverse('reviews:recensione_update', args=[self.recensione.id]), {
            'recensione_testuale': 'Ancora meglio!',
            'voto': 5,
        })

        # Verifica che l'update sia stato fatto correttamente
        self.assertEqual(response.status_code, 302)
        self.recensione.refresh_from_db()
        self.assertEqual(self.recensione.recensione_testuale, 'Ancora meglio!')

    def test_recensione_delete_view(self):
        # Login utente
        self.client.login(username='testuser', password='password')

        # Elimina la recensione
        response = self.client.post(reverse('reviews:recensione_delete', args=[self.recensione.id]))

        # Verifica che la recensione sia stata cancellata
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Recensione.objects.filter(id=self.recensione.id).count(), 0)

class RecensioneModelTest(TestCase):

    def setUp(self):
        # Crea due utenti di base e personal trainer per i test
        self.user1 = User.objects.create_user(username='utente1', password='testpass')
        self.user2 = User.objects.create_user(username='utente2', password='testpass')

        self.registrato_utente1 = RegistratoUtente.objects.create(
            user=self.user1,
            nome="Mario",
            cognome="Rossi",
            data_nascita="1990-01-01",
            bio="Appassionato di fitness"
        )

        self.personal_trainer1 = PersonalTrainer.objects.create(
            user=self.user2,
            nome="Luigi",
            cognome="Verdi",
            data_di_nascita="1985-01-01",
            bio="Esperto in powerlifting",
            preferenze="PL"
        )

    def test_crea_recensione_success(self):
        # Crea una recensione valida
        recensione = Recensione.objects.create(
            registrato_utente=self.registrato_utente1,
            personal_trainer=self.personal_trainer1,
            recensione_testuale="Ottimo allenatore, molto preparato.",
            voto=5
        )

        # Verifica che la recensione sia stata creata correttamente
        self.assertEqual(recensione.registrato_utente, self.registrato_utente1)
        self.assertEqual(recensione.personal_trainer, self.personal_trainer1)
        self.assertEqual(recensione.recensione_testuale, "Ottimo allenatore, molto preparato.")
        self.assertEqual(recensione.voto, 5)
        self.assertIsNotNone(recensione.data_recensione)

    def test_recensione_fail_manca_testo(self):
        # Prova a creare una recensione senza il campo testo
        with self.assertRaises(ValidationError):
            recensione = Recensione(
                registrato_utente=self.registrato_utente1,
                personal_trainer=self.personal_trainer1,
                voto=4
            )
            recensione.full_clean()  # Deve sollevare ValidationError

    def test_recensione_fail_manca_voto(self):
        # Prova a creare una recensione senza il campo voto
        with self.assertRaises(ValidationError):
            recensione = Recensione(
                registrato_utente=self.registrato_utente1,
                personal_trainer=self.personal_trainer1,
                recensione_testuale="Molto bravo."
            )
            recensione.full_clean()  # Deve sollevare ValidationError

    def test_recensione_fail_voto_fuori_intervallo(self):
        # Prova a creare una recensione con un voto fuori dal range 1-5
        with self.assertRaises(ValidationError):
            recensione = Recensione(
                registrato_utente=self.registrato_utente1,
                personal_trainer=self.personal_trainer1,
                recensione_testuale="Molto bravo.",
                voto=6  # Fuori dall'intervallo 1-5
            )
            recensione.full_clean()  # Deve sollevare ValidationError

    def test_unique_recensione_per_trainer(self):
        # Crea una recensione valida
        Recensione.objects.create(
            registrato_utente=self.registrato_utente1,
            personal_trainer=self.personal_trainer1,
            recensione_testuale="Molto bravo.",
            voto=5
        )

        # Prova a creare un'altra recensione per lo stesso personal trainer dallo stesso utente
        with self.assertRaises(ValidationError):
            recensione_duplicata = Recensione(
                registrato_utente=self.registrato_utente1,
                personal_trainer=self.personal_trainer1,
                recensione_testuale="Ancora meglio la seconda volta.",
                voto=4
            )
            recensione_duplicata.full_clean()  # Deve sollevare ValidationError per il vincolo di unicità

    def test_str_representation(self):
        # Verifica la rappresentazione in stringa del modello Recensione
        recensione = Recensione.objects.create(
            registrato_utente=self.registrato_utente1,
            personal_trainer=self.personal_trainer1,
            recensione_testuale="Ottimo allenatore, molto preparato.",
            voto=5
        )
        self.assertEqual(
            str(recensione),
            f"Recensione di {self.registrato_utente1} per {self.personal_trainer1} - 5 stelle"
        )
