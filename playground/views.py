from django.http import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import Ville
from .models import Agence
from . import models
from .models import Colis
from .models import Courrier
from .models import BoitePostale
from .models import Reexpedition
from .models import Activite
from .models import Expediteur
from .models import Panier
from .models import PrixBoiteReexpedition
from .models import PrixColisCourrier
from .models import Recu


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        agent=models.Agent.objects.filter(matricule=username,password=password).first()
        if agent is not None:
            return redirect('compte')
        else:
            error_message = "Matricule ou Mot de passe incorrect!!!"
            return render(request, 'login.html', {'error_message': error_message})

def LogoutPage(request):
    return redirect('login')

def sidebar(request):
    context = {
        'image_url': '../static/images/Poste_Maroc_logo.png',
    }
    return render(request, 'sideBar.html')

def loginPage(req) :
    return render(req, 'login.html')

def compte(request):
    return render(request,'compte.html')
