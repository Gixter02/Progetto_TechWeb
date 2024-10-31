from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard_amministratore, approva_personal_trainer, elimina_personal_trainer, \
    richiesta_personal_trainer, rifiuta_personal_trainer, RichiestaDetailView, SuccessPageView, elimina_account, \
    richiesta_list_view, personal_trainer_list_view, search_registrato_utente

app_name = 'gestione'

urlpatterns = [
    path('', dashboard_amministratore, name='dashboard_amministratore'),
    path('richiesta/<int:pk>', RichiestaDetailView.as_view(), name='richiesta_detail'),
    path('richiesta/approva/<int:pk>/', approva_personal_trainer, name='approva_personal_trainer'),
    path('richiesta/rifiuta/<int:pk>', rifiuta_personal_trainer, name='rifiuta_personal_trainer'),
    path('elimina_personal_trainer/<int:pk>/', elimina_personal_trainer, name='elimina_personal_trainer'),
    path('crearichiesta/', richiesta_personal_trainer, name='richiesta_personal_trainer'),
    path('success/', SuccessPageView.as_view(), name='success'),
    path('elimina_account/<int:pk>/', elimina_account, name='elimina_account'),
    path('lista_richieste/', richiesta_list_view, name='lista_richieste'),
    path('lista_personal_trainer/', personal_trainer_list_view, name='lista_personal_trainer'),
    path('cerca/', search_registrato_utente, name='search_registrato_utente'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)