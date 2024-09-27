from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, ListView

from bookings.models import Prenotazione
from reviews.models import Recensione
from .models import PersonalTrainer
from .forms import PersonalTrainerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone

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
        #messages.error(request, "Devi essere un personal trainer per visualizzare i tuoi allenamenti.")
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


def disponibilita_personal_trainer(request, pk):
    personal_trainer = get_object_or_404(PersonalTrainer, pk=pk)

    if request.method == 'POST':
        data_input = request.POST.get('data')
        data = timezone.datetime.strptime(data_input, "%Y-%m-%d").date()

        # Ottieni tutte le fasce orarie già prenotate per quel personal trainer e quella data
        fasce_prenotate = Prenotazione.objects.filter(
            personal_trainer=personal_trainer,
            data_prenotazione=data
        ).values_list('fascia_oraria', flat=True)

        # Disponibilità delle fasce orarie
        fasce_disponibili = [fascia for fascia in Prenotazione.ORARI_FASCIA if fascia[0] not in fasce_prenotate]

        context = {
            'personal_trainer': personal_trainer,
            'data': data,
            'fasce_disponibili': fasce_disponibili,
        }
        return render(request, 'trainers/personal_trainer_disponibilita.html', context)

    return render(request, 'trainers/personal_trainer_disponibilita.html', {'personal_trainer': personal_trainer})


def disponibilita_personal_trainers(request):
    personal_trainer_list = PersonalTrainer.objects.all()
    fasce_disponibili = []
    selected_trainer = None
    selected_date = None

    if request.method == 'POST':
        trainer_id = request.POST.get('personal_trainer')
        selected_date_input = request.POST.get('data')
        selected_date = timezone.datetime.strptime(selected_date_input, "%Y-%m-%d").date()
        selected_trainer = get_object_or_404(PersonalTrainer, pk=trainer_id)

        # Ottieni tutte le fasce orarie già prenotate per il personal trainer selezionato e quella data
        fasce_prenotate = Prenotazione.objects.filter(
            personal_trainer=selected_trainer,
            data_prenotazione=selected_date
        ).values_list('fascia_oraria', flat=True)

        # Disponibilità delle fasce orarie
        fasce_disponibili = [fascia for fascia in Prenotazione.ORARI_FASCIA if fascia[0] not in fasce_prenotate]

    context = {
        'personal_trainer_list': personal_trainer_list,
        'fasce_disponibili': fasce_disponibili,
        'selected_trainer': selected_trainer,
        'selected_date': selected_date,
    }

    return render(request, 'trainers/personal_trainers_disponibilita.html', context)
