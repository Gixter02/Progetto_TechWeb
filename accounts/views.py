from django.shortcuts import render

# Create your views here.
def home_accounts(request):
    render(request, template_name= "accounts/base.html", context={})