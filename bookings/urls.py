from django.urls import path

from . import views
from .views import crea_prenotazione, SuccessPageView

app_name='bookings'

urlpatterns = [
    path('', views.bookings_homepage, name='home_page'),
    path('prenota/', crea_prenotazione, name='crea_prenotazione'),
    path('success/', SuccessPageView.as_view(), name='success_page'),
]