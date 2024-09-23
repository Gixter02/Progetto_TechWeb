from django.urls import path
from . import views
from .views import homepage_recensioni, crea_recensione

app_name = 'reviews'

urlpatterns = [
    path('', homepage_recensioni, name='homepage_recensioni'),
    path('crea/', crea_recensione, name='crea_recensione'),
]