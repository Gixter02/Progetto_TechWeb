from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from trainers.models import PersonalTrainer
from accounts.models import RegistratoUtente
from bookings.models import Prenotazione
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

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


class PersonalTrainerModelTest(TestCase):
    def setUp(self):
        # Creiamo un utente di base per associare al PersonalTrainer
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Creiamo un oggetto PersonalTrainer per i test
        self.personal_trainer = PersonalTrainer.objects.create(
            user=self.user,
            nome="Mario",
            cognome="Rossi",
            bio="Esperto in fitness e body building",
            competenze="BodyBuilding, PowerLifting",
            preferenze="BB",
            data_di_nascita=timezone.now().date(),
        )

    def test_personal_trainer_creation(self):
        # Verifichiamo che il PersonalTrainer sia stato creato correttamente
        personal_trainer = PersonalTrainer.objects.get(user=self.user)
        self.assertEqual(personal_trainer.nome, 'Mario')
        self.assertEqual(personal_trainer.cognome, 'Rossi')
        self.assertEqual(personal_trainer.bio, 'Esperto in fitness e body building')
        self.assertEqual(personal_trainer.competenze, 'BodyBuilding, PowerLifting')
        self.assertEqual(personal_trainer.preferenze, 'BB')

    def test_update_personal_trainer(self):
        # Modifichiamo l'oggetto PersonalTrainer
        self.personal_trainer.nome = 'Luca'
        self.personal_trainer.cognome = 'Bianchi'
        self.personal_trainer.bio = 'Esperto in yoga'
        self.personal_trainer.save()

        # Verifichiamo che le modifiche siano salvate correttamente
        updated_personal_trainer = PersonalTrainer.objects.get(user=self.user)
        self.assertEqual(updated_personal_trainer.nome, 'Luca')
        self.assertEqual(updated_personal_trainer.cognome, 'Bianchi')
        self.assertEqual(updated_personal_trainer.bio, 'Esperto in yoga')

    def test_delete_personal_trainer(self):
        # Verifichiamo che l'oggetto PersonalTrainer sia eliminabile
        self.personal_trainer.delete()

        # Verifichiamo che l'oggetto sia stato eliminato
        personal_trainer_exists = PersonalTrainer.objects.filter(user=self.user).exists()
        self.assertFalse(personal_trainer_exists)

    def test_personal_trainer_str_representation(self):
        # Verifichiamo che la rappresentazione `__str__` restituisca il nome e cognome corretti
        self.assertEqual(str(self.personal_trainer), f'{self.personal_trainer.nome} {self.personal_trainer.cognome} - Preferenza: {self.personal_trainer.get_preferenze_display()}')


class PersonalTrainerModelFailureTest(TestCase):
    def setUp(self):
        # Creiamo un utente di base
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_creation_without_nome(self):
        with self.assertRaises(ValidationError):
            pt = PersonalTrainer(
                user=self.user,
                cognome="Rossi",
                bio="Esperto in fitness",
                competenze="BodyBuilding",
                preferenze="BB",
                data_di_nascita=timezone.now().date(),
            )
            pt.full_clean()  # Solleva un ValidationError a causa del campo mancante 'nome'
            pt.save()  # Non dovrebbe mai arrivare a questa linea

    def test_creation_without_cognome(self):
        # Proviamo a creare un PersonalTrainer senza cognome (campo obbligatorio)
        with self.assertRaises(ValidationError):
            pt = PersonalTrainer.objects.create(
                user=self.user,
                nome="Mario",
                bio="Esperto in fitness",
                competenze="BodyBuilding",
                preferenze="BB",
                data_di_nascita=timezone.now().date(),
            )
            pt.full_clean()  # Solleva un ValidationError a causa del campo mancante 'cognome'
            pt.save()  # Non dovrebbe mai arrivare a questa linea

    def test_creation_without_bio(self):
        # Verifichiamo che un PersonalTrainer possa essere creato con una bio vuota
        # Se il campo `bio` è obbligatorio, questo test fallirà. Se è facoltativo, sarà creato con bio vuota.
        personal_trainer = PersonalTrainer.objects.create(
            user=self.user,
            nome="Mario",
            cognome="Rossi",
            bio="",
            competenze="BodyBuilding",
            preferenze="BB",
            data_di_nascita=timezone.now().date(),
        )
        self.assertEqual(personal_trainer.bio, "")

    def test_creation_with_invalid_preferenze(self):
        # Proviamo a creare un PersonalTrainer con un valore non valido nel campo 'preferenze'
        with self.assertRaises(ValidationError):
            pt = PersonalTrainer.objects.create(
                user=self.user,
                nome="Mario",
                cognome="Rossi",
                bio="Esperto in fitness",
                competenze="BodyBuilding",
                preferenze="XX",  # Valore non valido
                data_di_nascita=timezone.now().date(),
            )
            pt.full_clean()  # Solleva un ValidationError a causa del campo errato 'preferenze'
            pt.save()  # Non dovrebbe mai arrivare a questa linea

    def test_update_with_invalid_data(self):
        # Creiamo un oggetto PersonalTrainer valido
        personal_trainer = PersonalTrainer.objects.create(
            user=self.user,
            nome="Mario",
            cognome="Rossi",
            bio="Esperto in fitness",
            competenze="BodyBuilding",
            preferenze="BB",
            data_di_nascita=timezone.now().date(),
        )

        # Proviamo a modificarlo con un cognome vuoto (campo obbligatorio)
        personal_trainer.cognome = ""
        with self.assertRaises(ValidationError):
            personal_trainer.full_clean()
            personal_trainer.save()

    def test_creation_without_user(self):
        # Proviamo a creare un PersonalTrainer senza un utente associato (campo obbligatorio)
        with self.assertRaises(IntegrityError):
            PersonalTrainer.objects.create(
                nome="Mario",
                cognome="Rossi",
                bio="Esperto in fitness",
                competenze="BodyBuilding",
                preferenze="BB",
                data_di_nascita=timezone.now().date(),
            )
