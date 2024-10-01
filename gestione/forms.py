from django import forms
from .models import RichiestaPersonalTrainer

class RichiestaPersonalTrainerForm(forms.ModelForm):
    class Meta:
        model = RichiestaPersonalTrainer
        exclude = ['user', 'data_richiesta', 'approvato']
