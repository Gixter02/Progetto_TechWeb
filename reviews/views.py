from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from reviews.forms import RecensioneForm
from trainers.models import PersonalTrainer



# Create your views here.

@login_required
def homepage_recensioni(request):
    # Ottieni la lista di tutti i personal trainer
    personal_trainers = PersonalTrainer.objects.all()

    return render(request, 'reviews/home_recensioni.html', {'personal_trainers': personal_trainers})

@login_required
def crea_recensione(request):
    for k in request.GET:
        personal_trainer = PersonalTrainer.objects.get(id=request.GET[k])

    if request.method == 'POST':
        form = RecensioneForm(request.POST)
        if form.is_valid():
            recensione = form.save(commit=False)
            recensione.registrato_utente = request.user.registratoutente  # Assegna l'utente loggato
            recensione.personal_trainer = personal_trainer  # Assegna il personal trainer selezionato
            recensione.save()
            return redirect('reviews:review_success')  # Redireziona ad una pagina di successo
    else:
        form = RecensioneForm()

    return render(request, 'reviews/crea_recensione.html', {'form': form, 'personal_trainer': personal_trainer})

def review_success(request):
    return render(request, 'reviews/success.html')
