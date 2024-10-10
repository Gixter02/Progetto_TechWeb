# Progetto TechWeb - Palestra Online
## Descrizione del Progetto

Il progetto Tecnologie Web consiste in  un sito web per una palestra online che offre la possibilità di prenotare allenamenti personalizzati con Personal Trainer. 
Non sono presenti corsi di gruppo, ma gli utenti registrati possono scegliere tra varie specialità di allenamento e prenotare sessioni individuali. 
Il sistema consente inoltre di lasciare recensioni ai Personal Trainer.
L'approvazione dei trainer da parte degli amministratori.

Funzionalità principali:

- **Registrazione utenti**: Gli utenti possono creare un profilo con informazioni personali e preferenze di allenamento.
- **Ricerca e prenotazione**: Gli utenti possono cercare Personal Trainer in base alle preferenze espresse e prenotare sessioni di allenamento.
- **Recensioni**: Gli utenti possono lasciare una recensione e valutare i Personal Trainer con un sistema a 5 stelle.
- **Gestione dei Personal Trainer**: Gli utenti possono fare richiesta per diventare Personal Trainer.
- **Dashboard amministrativa**: Gli amministratori possono approvare o rifiutare richieste per nuovi Personal Trainer.

## Struttura del Progetto

Il progetto è sviluppato con Django, un framework web Python, e suddiviso in diverse applicazioni:
- **accounts**: Gestione della registrazione e autenticazione degli utenti.
- **trainers**: Gestione dei Personal Trainer e delle relative informazioni.
- **reviews**: Funzionalità per la scrittura e la visualizzazione delle recensioni sui Personal Trainer.
- **bookings**: Prenotazione degli allenamenti tra gli utenti e i Personal Trainer. 
- **gestione**: Funzionalità di amministrazione per la gestione dei Personal Trainer.

## Requisiti

- Python 3.12
- Django 5.1.1
- virtual environment

## Installazione

Clonare il repository:

    git clone https://github.com/Gixter02/Progetto_TechWeb.git

    cd Progetto_TechWeb


Creare un ambiente virtuale Python e attivarlo:

    python3 -m venv venv
    source venv/bin/activate   # Su Windows usa venv\Scripts\activate

Installare le dipendenze:

    pip install -r requirements.txt

Eseguire le migrazioni del database:

    python manage.py migrate

Creare un superutente per accedere al pannello di amministrazione:

    python manage.py createsuperuser

Avviare il server di sviluppo:

    python manage.py runserver

    Accedere all'applicazione all'indirizzo http://localhost:8000.

## Testing

Per eseguire i test, utilizzare il seguente comando:

    python manage.py test

I test coprono le principali applicazioni: trainers, accounts, bookings, reviews, e gestione.

## Frameworks e Linguaggi utilizzati:

<p> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>