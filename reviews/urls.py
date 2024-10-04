from django.urls import path
from .views import homepage_recensioni, crea_recensione, review_success, ReviewListView, RecensioneUpdateView, \
    RecensioneDeleteView

app_name = 'reviews'

urlpatterns = [
    path('', homepage_recensioni, name='homepage_recensioni'),
    path('crea/', crea_recensione, name='crea_recensione'),
    path('succes/', review_success, name='review_success'),
    path('lista/', ReviewListView.as_view(), name='lista_recensioni'),
    path('<int:pk>/modifica/', RecensioneUpdateView.as_view(), name='recensione_update'),
    path('<int:pk>/delete/', RecensioneDeleteView.as_view(), name='recensione_delete'),
]