from django import forms

from trainers.models import PersonalTrainer
from .models import Recensione

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = [ 'recensione_testuale', 'voto']
        widgets = {
            'recensione_testuale': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Scrivi la tua recensione...'}),
            'voto': forms.RadioSelect(choices=[(i, f'{i} Stelle') for i in range(1, 6)]),  # Radio button per il voto a stelle
        }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Impostazione per personalizzare il campo 'personal_trainer'
        self.fields['personal_trainer'].queryset = PersonalTrainer.objects.all()
    '''