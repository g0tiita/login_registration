from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)

def login(request):
    return render(request,'login.html')

def registro(request):
    if request.method == "POST":
        print(request.POST)

        errors = User.objects.basic_validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                #print("Desde el for: ", key, value)

        return redirect("/registro")
    else:
        return render(request,'registro.html')
