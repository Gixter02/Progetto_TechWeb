from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard_amministratore, approva_personal_trainer, elimina_personal_trainer, \
    richiesta_personal_trainer, rifiuta_personal_trainer, RichiestaDetailView, SuccessPageView

app_name = 'gestione'

urlpatterns = [
    path('', dashboard_amministratore, name='dashboard_amministratore'),
    path('richiesta/<int:pk>', RichiestaDetailView.as_view(), name='richiesta_detail'),
    path('richiesta/approva/<int:pk>/', approva_personal_trainer, name='approva_personal_trainer'),
    path('richiesta/rifiuta/<int:pk>', rifiuta_personal_trainer, name='rifiuta_personal_trainer'),
    path('elimina_personal_trainer/<int:pk>/', elimina_personal_trainer, name='elimina_personal_trainer'),
    path('crearichiesta/', richiesta_personal_trainer, name='richiesta_personal_trainer'),
    path('success/', SuccessPageView.as_view(), name='success'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)