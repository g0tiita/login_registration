from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt

def logout(request):
    if 'usuario' in request.session: 
        del request.session['usuario']
    
    return redirect("/")

def index(request):
    #si el usuario no esta registrado que no pase del index
    if 'usuario' not in request.session:
        return redirect("/login")
        
    return render(request,'index.html')

def registro(request):
    if request.method == "POST":
        print(request.POST)
        errors = User.objects.basic_validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                #print("Desde el for: ", key, value)
                
            #Para mantener el dato una vez que aparecen los errores
            request.session['registro_firstname']=request.POST['firstname']
            request.session['registro_lastname']=request.POST['lastname']
            request.session['registro_email']=request.POST['email']
        else:
            #Vacia las variables de sesion
            request.session['registro_firstname']=""  
            request.session['registro_lastname']=""
            request.session['registro_email']=""

            
            password_encriptada=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

            User.objects.create(
                                firstname=request.POST['firstname'],
                                lastname=request.POST['lastname'],
                                email=request.POST['email'],
                                password=password_encriptada)
            
            messages.success(request, "User entered correctly")

        return render(request, 'success.html')
    
def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                
                usuario= {
                    "id": log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email
                }
                
                request.session['usuario']=usuario
                messages.success(request, "User entered correctly")
                return render(request, 'success.html')
            else:
                messages.error(request, "Pasword or email wrong")
        else:
            messages.error(request, "Email or password wrong")

        return redirect("/")
    else:
        return render(request,'index.html')




