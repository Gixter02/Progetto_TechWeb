from django import forms

from .models import RegistratoUtente

class RegistratoUtenteForm(forms.ModelForm):
    class Meta:
        model = RegistratoUtente
        exclude = ['user']