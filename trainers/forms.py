from django import forms

from .models import PersonalTrainer

class PersonalTrainerForm(forms.ModelForm):

    class Meta:
        model = PersonalTrainer
        exclude = ['user']