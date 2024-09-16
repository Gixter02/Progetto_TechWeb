from django.shortcuts import render
from django.views.generic import ListView

from accounts.models import Utente


# Create your views here.
def home_accounts(request):
    render(request, template_name= "accounts/base.html", context={})

class ListaUtentiView(ListView):
    model = Utente
    template_name = "accounts/listautenti.html"