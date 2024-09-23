from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, ListView

from bookings.models import Prenotazione
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

# View per visualizzare i dettagli del Personal Trainer
class PersonalTrainerDetailView(LoginRequiredMixin, DetailView):
    model = PersonalTrainer
    template_name = 'trainers/personal_trainer_detail.html'

    def get_queryset(self):
        # Mostra solo i dettagli del personal trainer autenticato
        return PersonalTrainer.objects.filter(user=self.request.user)

class PersonalTrainerHomeView(TemplateView):
    template_name = 'trainers/personal_trainer_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            personal_trainer = PersonalTrainer.objects.get(user=self.request.user)
            context['personal_trainer'] = personal_trainer
        except PersonalTrainer.DoesNotExist:
            context['personal_trainer'] = None
        return context

class PersonalTrainerListView(ListView):
    model = PersonalTrainer
    template_name = 'trainers/personal_trainer_list.html'

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