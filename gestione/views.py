from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from trainers.models import PersonalTrainer
from .forms import RichiestaPersonalTrainerForm
from .models import RichiestaPersonalTrainer

from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
# views.py



@login_required
def richiesta_personal_trainer(request):
    if request.method == 'POST':
        form = RichiestaPersonalTrainerForm(request.POST)
        if form.is_valid():
            richiesta = form.save(commit=False)
            richiesta.user = request.user
            richiesta.save()
            return redirect('gestione:dashboard_amministratore')
    else:
        form = RichiestaPersonalTrainerForm()

    return render(request, 'gestione/richiesta_personal_trainer.html', {'form': form})



@staff_member_required
def approva_personal_trainer(request, pk):
    richiesta = get_object_or_404(RichiestaPersonalTrainer, pk=pk)
    personal_trainer = PersonalTrainer.objects.create(
        user=richiesta.user,
        nome=richiesta.nome,
        cognome=richiesta.cognome,
        bio=richiesta.bio,
        competenze=richiesta.competenze,
        preferenze=richiesta.preferenze,
        data_di_nascita=richiesta.data_di_nascita,
        immagine_profilo=richiesta.immagine_profilo,
    )
    richiesta.delete()
    return redirect('gestione:dashboard_amministratore') #ridireziona a success page

@staff_member_required
def elimina_personal_trainer(request, pk):
    personal_trainer = get_object_or_404(PersonalTrainer, pk=pk)
    personal_trainer.delete()
    return redirect('gestione:dashboard_amministratore') #ridireziona a success page

@staff_member_required
def dashboard_amministratore(request):
    richieste = RichiestaPersonalTrainer.objects.filter(approvato=False)
    personal_trainers = PersonalTrainer.objects.all()
    return render(request, 'gestione/dashboard_amministratore.html', {
        'richieste': richieste,
        'personal_trainers': personal_trainers
    })

