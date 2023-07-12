from django.http import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import Ville
from .models import Agence
from .models import Agent
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
        username = request.POST['username']
        password = request.POST['password']
        agent=Agent.objects.filter(matricule=username,password=password)
        if agent is not None:
            login(request,agent)
            return redirect('compte')
        else:
            error_message = "<b style='font-family:Poppins;  position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);font-size:20px;color:#001272;'>Matricule ou Mot de passe incorrect!!!</b>"
            return render(request, 'login.html', {'error_message': error_message})

def LogoutPage(request):
    logout(request)
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
