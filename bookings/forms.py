from django import forms

from trainers.models import PersonalTrainer
from .models import Prenotazione

class PrenotazioneForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ['personal_trainer', 'fascia_oraria', 'data_prenotazione', 'richieste_specifiche']
        widgets = {
            'data_prenotazione': forms.SelectDateWidget(),  # Widget per selezionare la data
            'richieste_specifiche': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Richieste specifiche (opzionale)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Impostazione per personalizzare il campo 'personal_trainer'
        self.fields['personal_trainer'].queryset = PersonalTrainer.objects.all()

class PrenotazioneUpdateForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ['richieste_specifiche']  # Solo questo campo può essere modificato