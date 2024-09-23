from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PersonalTrainerCreateView, PersonalTrainerUpdateView, PersonalTrainerDetailView, \
    PersonalTrainerHomeView, PersonalTrainerListView, allenamenti_programmati

app_name = 'trainers'

urlpatterns = [
    path('', PersonalTrainerHomeView.as_view(), name='personal_trainer_home'),
    path('create/', PersonalTrainerCreateView.as_view(), name='personal_trainer_create'),
    path('<int:pk>/edit/', PersonalTrainerUpdateView.as_view(), name='personal_trainer_update'),
    path('<int:pk>/', PersonalTrainerDetailView.as_view(), name='personal_trainer_detail'),
    path('elencoallenatori/', PersonalTrainerListView.as_view(), name='personal_trainer_list'),
    path('allenamenti/', allenamenti_programmati, name='allenamenti_programmati'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
