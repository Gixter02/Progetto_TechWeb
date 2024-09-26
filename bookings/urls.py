from django.urls import path

from . import views
from .views import crea_prenotazione

app_name='bookings'

urlpatterns = [
    path('', views.bookings_homepage, name='home_page'),
    path('prenota/', crea_prenotazione, name='crea_prenotazione'),

]