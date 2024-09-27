from django.core.exceptions import ValidationError
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PrenotazioneForm
from .models import RegistratoUtente, Prenotazione


@login_required
def crea_prenotazione(request):
    # Ottieni l'utente registrato associato all'utente loggato
    try:
        registrato_utente = RegistratoUtente.objects.get(user=request.user)
    except RegistratoUtente.DoesNotExist:
        #messages.error(request, "Devi essere un utente registrato per effettuare una prenotazione.")
        return redirect('homepage_palestra')

    if request.method == 'POST':
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            # Associa l'utente loggato alla prenotazione
            prenotazione = form.save(commit=False)
            prenotazione.registrato_utente = registrato_utente

            # Verifica che non ci siano prenotazioni per la stessa fascia oraria e trainer
            try:
                prenotazione.clean()
                prenotazione.save()
                #messages.success(request, "Prenotazione effettuata con successo!")
                return redirect('bookings:home_page')  # Redireziona a una pagina di conferma o dashboard
            except ValidationError as e:
                form.add_error(None, e.message)

    else:
        form = PrenotazioneForm()

    return render(request, 'bookings/crea_prenotazione.html', {'form': form})

@login_required
def bookings_homepage(request):
    # Ottieni le prenotazioni fatte dall'utente loggato
    prenotazioni = Prenotazione.objects.filter(registrato_utente__user=request.user).order_by('data_prenotazione', 'fascia_oraria')

    return render(request, 'bookings/bookings_homepage.html', {'prenotazioni': prenotazioni})