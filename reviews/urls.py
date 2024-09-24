from django.urls import path
from . import views
from .views import homepage_recensioni, crea_recensione, review_success

app_name = 'reviews'

urlpatterns = [
    path('', homepage_recensioni, name='homepage_recensioni'),
    path('crea/', crea_recensione, name='crea_recensione'),
    path('succes/', review_success, name='review_success'),
]