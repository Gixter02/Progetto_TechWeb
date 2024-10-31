from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import  CreateView, DetailView, UpdateView
from django.shortcuts import render, redirect

from bookings.models import Prenotazione
from .models import RegistratoUtente
from .froms import RegistratoUtenteForm


# Create your views here.
def home_accounts(request):
    return render(request, template_name= "accounts/home_page.html")

class CreaUtenteView(CreateView):
    model = RegistratoUtente
    form_class = UserCreationForm
    template_name = "accounts/creazione_utenti.html"
    success_url = reverse_lazy("accounts:login")

class RegistratoUtenteCreateView(LoginRequiredMixin, CreateView):
    model = RegistratoUtente
    form_class = RegistratoUtenteForm
    template_name = 'accounts/creazione_utenti.html'
    success_url = reverse_lazy('accounts:home_accounts')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associa l'utente autenticato
        return super().form_valid(form)

@login_required
def allenamenti_utente(request):
    # Ottieni l'utente registrato associato all'utente loggato
    try:
        registrato_utente = RegistratoUtente.objects.get(user=request.user)
    except RegistratoUtente.DoesNotExist:
        # Se l'utente non è un utente registrato, redireziona con un messaggio di errore
        #messages.error(request, "Devi essere un utente registrato per visualizzare i tuoi allenamenti.")
        return redirect('accounts:home_accounts')

    # Ottieni tutte le prenotazioni future dell'utente registrato
    allenamenti = Prenotazione.objects.filter(registrato_utente=registrato_utente).order_by('data_prenotazione', 'fascia_oraria')

    return render(request, 'accounts/allenamenti_utente.html', {'allenamenti': allenamenti})

class RegistratoUtenteDetailview(LoginRequiredMixin, DetailView):
    model = RegistratoUtente
    template_name = 'accounts/profilo.html'

class RegistraoUtenteUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistratoUtente
    form_class = RegistratoUtenteForm
    template_name = 'accounts/edit_registrato_utente.html'

    def get_queryset(self):
        # Permette solo al personal trainer autenticato di aggiornare i propri dati
        return RegistratoUtente.objects.filter(user=self.request.user)

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse('accounts:profilo', kwargs={'pk': pk})