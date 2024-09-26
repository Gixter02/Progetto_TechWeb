from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, ListView

from bookings.models import Prenotazione
from reviews.models import Recensione
from .models import PersonalTrainer
from .forms import PersonalTrainerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# View per creare un Personal Trainer
class PersonalTrainerCreateView(LoginRequiredMixin, CreateView):
    model = PersonalTrainer
    form_class = PersonalTrainerForm
    template_name = 'trainers/personal_trainer_form.html'
    success_url = reverse_lazy('trainers:personal_trainer_home')  # Reindirizzamento dopo la creazione

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associa l'utente autenticato
        return super().form_valid(form)

# View per modificare i dati del Personal Trainer
class PersonalTrainerUpdateView(LoginRequiredMixin, UpdateView):
    model = PersonalTrainer
    form_class = PersonalTrainerForm
    template_name = 'trainers/personal_trainer_form.html'
    success_url = reverse_lazy('trainers:personal_trainer_home')  # Reindirizzamento dopo la modifica

    def get_queryset(self):
        # Permette solo al personal trainer autenticato di aggiornare i propri dati
        return PersonalTrainer.objects.filter(user=self.request.user)

    def form_valid(self, form):
        # Assicura che il personal trainer rimanga associato all'utente autenticato
        form.instance.user = self.request.user
        return super().form_valid(form)


class PersonalTrainerHomeView(TemplateView):
    template_name = 'trainers/personal_trainer_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            personal_trainer = PersonalTrainer.objects.get(user=self.request.user)
            context['personal_trainer'] = personal_trainer
        except PersonalTrainer.DoesNotExist:
            context['personal_trainer'] = None
        except TypeError:
            context['personal_trainer'] = None
        return context


@login_required
def allenamenti_programmati(request):
    # Verifica se l'utente è un personal trainer
    try:
        personal_trainer = PersonalTrainer.objects.get(user=request.user)
    except PersonalTrainer.DoesNotExist:
        # Se l'utente non è un personal trainer, redireziona ad una pagina con un messaggio di errore
        messages.error(request, "Devi essere un personal trainer per visualizzare i tuoi allenamenti.")
        return redirect('personal_trainer_home')

    # Ottieni tutte le prenotazioni future per questo personal trainer
    allenamenti = Prenotazione.objects.filter(personal_trainer=personal_trainer).order_by('data_prenotazione', 'fascia_oraria')

    return render(request, 'trainers/allenamenti_programmati.html', {'allenamenti': allenamenti})

class PersonalTrainerReviewDetailView(DetailView):
    model = PersonalTrainer
    template_name = 'trainers/personal_trainer_review_detail.html'
    context_object_name = 'personal_trainer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calcolare la media delle recensioni
        context['media_voti'] = Recensione.objects.filter(personal_trainer=self.object).aggregate(Avg('voto'))['voto__avg']
        # Recuperare tutte le recensioni dell'allenatore
        context['recensioni'] = Recensione.objects.filter(personal_trainer=self.object)
        return context

def elenco_personal_trainer(request):
    # Ottieni tutti i personal trainer e la loro media voti
    personal_trainer_list = PersonalTrainer.objects.annotate(media_voti=Avg('recensione__voto'))

    context = {
        'personal_trainer_list': personal_trainer_list,
    }
    return render(request, 'trainers/personal_trainer_elenco.html', context)