from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from accounts.models import RegitratoUtente


# Create your views here.
def home_accounts(request):
    return render(request, template_name= "accounts/home.html")

class ListaUtentiView(ListView):
    model = RegitratoUtente
    template_name = "accounts/listautenti.html"

class CreaUtenteRegistratoView(CreateView):
    model = RegitratoUtente
    fields = "__all__"
    template_name = "accounts/creazione_utenti.html"
    success_url = reverse_lazy("accounts:lista_utenti")

class CreaUtenteView(CreateView):
    model = RegitratoUtente
    form_class = UserCreationForm
    template_name = "accounts/creazione_utenti.html"
    success_url = reverse_lazy("accounts:registrazione")