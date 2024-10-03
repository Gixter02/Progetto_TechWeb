from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PersonalTrainerUpdateView, \
    PersonalTrainerHomeView, allenamenti_programmati, PersonalTrainerReviewDetailView, \
    disponibilita_personal_trainer, disponibilita_personal_trainers, \
    elenco_personal_trainers_ordinato

app_name = 'trainers'

urlpatterns = [
    path('', PersonalTrainerHomeView.as_view(), name='personal_trainer_home'),
    path('<int:pk>/edit/', PersonalTrainerUpdateView.as_view(), name='personal_trainer_update'),
    path('allenamenti/', allenamenti_programmati, name='allenamenti_programmati'),
    path('detail/<pk>/', PersonalTrainerReviewDetailView.as_view(), name='personal_trainer_review'),
    path('elenco/', elenco_personal_trainers_ordinato, name='elenco_personal_trainers_ordinato'),
    path('disponibilita/<pk>/', disponibilita_personal_trainer, name='disponibilita_personal_trainer'),
    path('verificadisponibilita/', disponibilita_personal_trainers, name='disponibilita_personal_trainers'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
