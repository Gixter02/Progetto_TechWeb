from django import forms

from trainers.models import PersonalTrainer
from .models import Recensione

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = [ 'recensione_testuale', 'voto']
        widgets = {
            'recensione_testuale': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Scrivi la tua recensione...'}),
            'voto': forms.RadioSelect(attrs={'class': 'form-check-input'}, choices=[(i, f'{i} Stelle') for i in range(1, 6)]),
        }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Impostazione per personalizzare il campo 'personal_trainer'
        self.fields['personal_trainer'].queryset = PersonalTrainer.objects.all()
    '''