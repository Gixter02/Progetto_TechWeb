from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.shortcuts import render
from .models import RegistratoUtente
from .froms import RegistratoUtenteForm


# Create your views here.
def home_accounts(request):
    return render(request, template_name= "accounts/home_page.html")

class ListaUtentiView(ListView):
    model = RegistratoUtente
    template_name = "accounts/listautenti.html"

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