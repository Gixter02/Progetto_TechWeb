from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', home_accounts, name='home_accounts'),
]