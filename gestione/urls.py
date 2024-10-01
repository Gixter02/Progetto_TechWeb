from django.urls import path
from .views import dashboard_amministratore, approva_personal_trainer, elimina_personal_trainer, \
    richiesta_personal_trainer

app_name = 'gestione'

urlpatterns = [
    path('', dashboard_amministratore, name='dashboard_amministratore'),
    path('approva/<int:pk>/', approva_personal_trainer, name='approva_personal_trainer'),
    path('elimina_personal_trainer/<int:pk>/', elimina_personal_trainer, name='elimina_personal_trainer'),
    path('richiesta/', richiesta_personal_trainer, name='richiesta_personal_trainer'),

]