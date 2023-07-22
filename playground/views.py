from django.shortcuts import render,redirect
from . import models

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        agent=models.Agent.objects.filter(matricule=username,password=password).first()
        if agent is not None:
            agence=models.Agence.objects.filter(num_agence=agent.num_agence_id).first()
            request.session['matricule'] = agent.matricule 
            request.session['nom_complet'] = agent.nom_complet
            request.session['password'] = agent.password
            request.session['status'] = agent.status
            request.session['profile'] = agent.profile
            request.session['num_agence_id'] = agent.num_agence_id
            request.session['nom_agence']=agence.nom_agence
            return redirect('welcome')
        else:
            error_message = "Matricule ou Mot de passe incorrect!!!"
            return render(request, 'login.html', {'error_message': error_message})


def LogoutPage(request):
    return redirect('Login')

def Login(request) :
    return render(request, 'login.html')

def compte(request):
    matricule = request.session.get('matricule')
    nom_complet= request.session.get('nom_complet')
    password= request.session.get('password')
    status= request.session.get('status')
    profile= request.session.get('profile')
    nom_agence=request.session.get('nom_agence')
    context = {
        'matricule': matricule,
        'nom_complet': nom_complet,
        'password': password,
        'status': status,
        'profile': profile,
        'nom_agence': nom_agence
    }

    return render(request,'compte.html',context)


def save(request):
    ##update de la base de donnee 
    password= request.session.get('password')
    status= request.session.get('status')
    profile= request.session.get('profile')
    num_agence_id=request.session.get('num_agence_id')
    matricule= request.session.get('matricule')
    nom = request.POST.get('nom')
    my_save=models.Agent(matricule=matricule,password=password,nom_complet=nom,status=status,profile=profile,num_agence_id=num_agence_id)
    my_save.save()
    ##update de la session
    agent=models.Agent.objects.filter(matricule=matricule,password=password).first()
    agence=models.Agence.objects.filter(num_agence=agent.num_agence_id).first()
    request.session['matricule'] = agent.matricule 
    request.session['nom_complet'] = agent.nom_complet
    request.session['password'] = agent.password
    request.session['status'] = agent.status
    request.session['profile'] = agent.profile
    request.session['num_agence_id'] = agent.num_agence_id
    request.session['nom_agence']=agence.nom_agence
    ##actualisation de la page compte
    return redirect('compte')

def reexpedition(request):
    matricule = request.session.get('matricule')
    profile= request.session.get('profile')
    nom_agence=request.session.get('nom_agence')
    context = {
        'matricule': matricule,
        'profile': profile,
        'nom_agence': nom_agence,
    }
    return render(request, 'reexpedition.html',context)


def reexpedition_save(request):
    return redirect('reexpedition')
    










def welcome(request):
    matricule = request.session.get('matricule')
    profile= request.session.get('profile')
    nom_agence=request.session.get('nom_agence')
    context = {
        'matricule': matricule,
        'profile': profile,
        'nom_agence': nom_agence
    }
    return render(request,'sidebar.html',context)