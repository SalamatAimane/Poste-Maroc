from django.http import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')

def Compte(request):
    return render (request,'compte.html')

def LoginPage(request):
    context = {
        'image_url': '../static/images/Poste_Maroc_logo.png',
     }
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('compte')
        else:
            return HttpResponse ("<b style='font-family:Poppins;  position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);font-size:30px;color:#001272;'>Matricule ou Mot de passe incorrect!!!</b>")
    return render (request,'login.html')



def LogoutPage(request):
    logout(request)
    return redirect('login')

def sidebar(request):
    context = {
        'image_url': '../static/images/Poste_Maroc_logo.png',
    }
    return render(request, 'sideBar.html')
