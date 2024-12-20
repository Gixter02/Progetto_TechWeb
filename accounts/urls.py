from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('', home_accounts, name='home_accounts'),
    path('creautente/', CreaUtenteView.as_view() , name='creautente'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
    path('inserimentodatiutente/', RegistratoUtenteCreateView.as_view(), name='inserimento_dati_utente'),
    path('allenamenti/', allenamenti_utente, name='allenamenti_utente'),
    path('profilo/<pk>/', RegistratoUtenteDetailview.as_view(), name='profilo'),
    path('modifica/<pk>/', RegistraoUtenteUpdateView.as_view(), name='modifica'),
]