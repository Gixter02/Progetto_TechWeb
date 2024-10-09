from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from gestione.models import RichiestaPersonalTrainer
from trainers.models import PersonalTrainer
from django.utils import timezone

class GestioneViewsTestCase(TestCase):
    def setUp(self):
        # Creiamo un utente standard e uno staff
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.staff_user = User.objects.create_user(username='staffuser', password='12345', is_staff=True)

        # Creiamo una richiesta per personal trainer
        self.richiesta = RichiestaPersonalTrainer.objects.create(
            user=self.user,
            nome="Mario",
            cognome="Rossi",
            bio="Istruttore fitness",
            competenze="BodyBuilding, PowerLifting",
            preferenze="BB",
            data_di_nascita=timezone.now().date(),
        )

    def test_richiesta_personal_trainer_view(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        # Autenticazione come utente normale
        self.client.login(username='testuser1', password='12345')

        # Verifichiamo che la view di creazione della richiesta sia accessibile
        response = self.client.get(reverse('gestione:richiesta_personal_trainer'))
        self.assertEqual(response.status_code, 200)

        # Simuliamo la creazione di una richiesta
        response = self.client.post(reverse('gestione:richiesta_personal_trainer'), {
            'nome': 'Luca',
            'cognome': 'Bianchi',
            'bio': 'Esperto in yoga',
            'competenze': 'Yoga',
            'preferenze': 'YG',
            'data_di_nascita': '1990-01-01',
        })

        # Verifichiamo il redirect alla pagina di successo
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gestione:success'))

        # Verifichiamo che la richiesta sia stata creata
        self.assertTrue(RichiestaPersonalTrainer.objects.filter(user=self.user1).exists())

    def test_approva_personal_trainer_view(self):
        # Autenticazione come utente staff
        self.client.login(username='staffuser', password='12345')

        # Verifichiamo che la view di approvazione funzioni
        response = self.client.post(reverse('gestione:approva_personal_trainer', kwargs={'pk': self.richiesta.pk}))

        # Verifichiamo il redirect alla pagina di successo
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gestione:success'))

        # Verifichiamo che il PersonalTrainer sia stato creato
        personal_trainer = PersonalTrainer.objects.filter(user=self.user)
        self.assertEqual(personal_trainer.count(), 1)
        self.assertEqual(personal_trainer.first().nome, 'Mario')

        # Verifichiamo che la richiesta sia stata eliminata
        self.assertFalse(RichiestaPersonalTrainer.objects.filter(pk=self.richiesta.pk).exists())

    def test_rifiuta_personal_trainer_view(self):
        # Autenticazione come utente staff
        self.client.login(username='staffuser', password='12345')

        # Verifichiamo che la view di rifiuto funzioni
        response = self.client.post(reverse('gestione:rifiuta_personal_trainer', kwargs={'pk': self.richiesta.pk}))

        # Verifichiamo il redirect alla pagina di successo
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gestione:success'))

        # Verifichiamo che la richiesta sia stata eliminata
        self.assertFalse(RichiestaPersonalTrainer.objects.filter(pk=self.richiesta.pk).exists())

    def test_elimina_personal_trainer_view(self):
        # Creiamo un PersonalTrainer associato all'utente
        personal_trainer = PersonalTrainer.objects.create(
            user=self.user,
            nome='Mario',
            cognome='Rossi',
            bio='Esperto in PowerLifting',
            preferenze='PL',
            data_di_nascita=timezone.now().date(),
        )

        # Autenticazione come utente staff
        self.client.login(username='staffuser', password='12345')

        # Verifichiamo che la view di eliminazione funzioni
        response = self.client.post(reverse('gestione:elimina_personal_trainer', kwargs={'pk': personal_trainer.pk}))

        # Verifichiamo il redirect alla pagina di successo
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('gestione:success'))

        # Verifichiamo che il PersonalTrainer sia stato eliminato
        self.assertFalse(PersonalTrainer.objects.filter(pk=personal_trainer.pk).exists())

    def test_dashboard_amministratore_view(self):
        # Autenticazione come utente staff
        self.client.login(username='staffuser', password='12345')

        # Verifichiamo che la dashboard sia accessibile
        response = self.client.get(reverse('gestione:dashboard_amministratore'))
        self.assertEqual(response.status_code, 200)

        # Verifichiamo che la richiesta non approvata sia mostrata
        self.assertContains(response, self.richiesta.nome)

    def test_richiesta_detail_view(self):
        # Autenticazione come utente staff
        self.client.login(username='staffuser', password='12345')

        # Verifichiamo che la view dettaglio sia accessibile
        response = self.client.get(reverse('gestione:richiesta_detail', kwargs={'pk': self.richiesta.pk}))
        self.assertEqual(response.status_code, 200)

        # Verifichiamo che il nome della richiesta sia visualizzato
        self.assertContains(response, self.richiesta.nome)
