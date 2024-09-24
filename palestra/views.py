from django.shortcuts import render

def homepage_palestra(request):
    return render(request, 'home_page.html')
