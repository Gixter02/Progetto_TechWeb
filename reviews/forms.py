from django import forms

from .models import Recensione

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = [ 'recensione_testuale', 'voto']
        widgets = {
            'recensione_testuale': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Scrivi la tua recensione...'}),
            'voto': forms.RadioSelect(attrs={'class': 'form-check-input'}, choices=[(i, f'{i} Stelle') for i in range(1, 6)]),
        }
