from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PersonalTrainerCreateView, PersonalTrainerUpdateView, \
    PersonalTrainerHomeView, allenamenti_programmati, PersonalTrainerReviewDetailView, \
    elenco_personal_trainer, disponibilita_personal_trainer

app_name = 'trainers'

urlpatterns = [
    path('', PersonalTrainerHomeView.as_view(), name='personal_trainer_home'),
    path('create/', PersonalTrainerCreateView.as_view(), name='personal_trainer_create'),
    path('<int:pk>/edit/', PersonalTrainerUpdateView.as_view(), name='personal_trainer_update'),
    path('allenamenti/', allenamenti_programmati, name='allenamenti_programmati'),
    path('detail/<pk>/', PersonalTrainerReviewDetailView.as_view(), name='personal_trainer_review'),
    path('elenco/', elenco_personal_trainer, name='elenco_personal_trainer'),
    path('disponibilita/<pk>/', disponibilita_personal_trainer, name='disponibilita_personal_trainer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
