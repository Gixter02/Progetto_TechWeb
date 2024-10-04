from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView

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
                return redirect('bookings:success_page')  # Redireziona a una pagina di conferma o dashboard
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

class SuccessPageView(TemplateView):
    template_name = 'bookings/success.html'

class PrenotazioneDeleteView(LoginRequiredMixin, DeleteView):
    model = Prenotazione
    template_name = 'bookings/confirm_delete.html'
    success_url = reverse_lazy('bookings:success_page')

    # Aggiungere il controllo per permettere solo al proprietario della prenotazione di cancellarla
    def get_queryset(self):
        # Limita le prenotazioni cancellabili solo a quelle dell'utente loggato
        queryset = super().get_queryset()
        return queryset.filter(registrato_utente__user=self.request.user)

@login_required
def elimina_prenotazioni(request):
    # Ottieni le prenotazioni fatte dall'utente loggato
    prenotazioni = Prenotazione.objects.filter(registrato_utente__user=request.user).order_by('data_prenotazione', 'fascia_oraria')

    return render(request, 'bookings/elimina_prenotazioni.html', {'prenotazioni': prenotazioni})