from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.shortcuts import render, redirect

from accounts.models import RegistratoUtente
from reviews.forms import RecensioneForm
from trainers.models import PersonalTrainer



# Create your views here.

@login_required
def homepage_recensioni(request):
    # Ottieni la lista di tutti i personal trainer
    personal_trainers = PersonalTrainer.objects.all()

    return render(request, 'reviews/home_recensioni.html', {'personal_trainers': personal_trainers})

@login_required
def crea_recensione(request):
    # Recupera l'ID del personal trainer dal parametro GET
    personal_trainer_id = request.GET.get('personal_trainer')

    if not personal_trainer_id:
        # Se manca il parametro, invia un messaggio di errore
        messages.error(request, "Personal trainer non selezionato.")
        return redirect('reviews:homepage_recensioni')  # Reindirizza alla homepage delle recensioni o a una pagina d'errore

    # Recupera il personal trainer selezionato, gestendo l'eccezione nel caso in cui l'ID non sia valido
    try:
        personal_trainer = PersonalTrainer.objects.get(id=personal_trainer_id)
    except PersonalTrainer.DoesNotExist:
        messages.error(request, "Il personal trainer selezionato non esiste.")
        return redirect('reviews:homepage_recensioni')

    # Ottieni l'utente registrato associato all'utente loggato
    try:
        registrato_utente = RegistratoUtente.objects.get(user=request.user)
    except RegistratoUtente.DoesNotExist:
        messages.error(request, "Devi essere un utente registrato per effettuare una prenotazione.")
        return redirect('reviews:homepage_receptioni')

    if request.method == 'POST':
        form = RecensioneForm(request.POST)
        if form.is_valid():
            try:
                recensione = form.save(commit=False)
                recensione.registrato_utente = registrato_utente  # Assegna l'utente loggato
                recensione.personal_trainer = personal_trainer  # Assegna il personal trainer selezionato
                recensione.save()
                messages.success(request, 'Recensione registrata con successo')
                return redirect('reviews:review_success')  # Redireziona ad una pagina di successo
            except IntegrityError:
                messages.error(request, "Hai già lasciato una recensione per questo personal trainer.")
    else:
        form = RecensioneForm()

    return render(request, 'reviews/crea_recensione.html', {'form': form, 'personal_trainer': personal_trainer})

def review_success(request):
    return render(request, 'reviews/success.html')
