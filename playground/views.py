from django.shortcuts import render,redirect
import datetime
from . import models 

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        agent=models.Agent.objects.filter(matricule=username,password=password).first()
        
        if agent is not None:
            agence=models.Agence.objects.filter(num_agence=agent.num_agence_id).first()
            Save=models.Panier(num_agent=agent,status='actif',prix_ht=0,prix_ttc=0,tva=0)
            Save.save()
            panier=models.Panier.objects.order_by('-num_Panier').first()
            request.session['matricule'] = agent.matricule 
            request.session['nom_complet'] = agent.nom_complet
            request.session['password'] = agent.password
            request.session['status'] = agent.status
            request.session['profile'] = agent.profile
            request.session['num_agence_id'] = agent.num_agence_id
            request.session['nom_agence']=agence.nom_agence
            request.session['num_Panier']=panier.num_Panier
            return redirect('welcome')
        else:
            error_message = "Matricule ou Mot de passe incorrect!!!"
            return render(request, 'login.html', {'error_message': error_message})

def LogoutPage(request):
    request.session.clear()
    return redirect('Login')

def Login(request) :
    return render(request, 'login.html')

def compte(request):
    if request.session.get('matricule') and request.session.get('password'):
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
    else :
        return redirect('logout')


def save(request):
    if request.session.get('matricule') and request.session.get('password'):
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
    else :
        return redirect('logout')

def reexpedition(request):
    if request.session.get('matricule') and request.session.get('password'):
        matricule = request.session.get('matricule')
        profile= request.session.get('profile')
        nom_agence=request.session.get('nom_agence')
        villes=models.Ville.objects.all()
        prixs=models.PrixBoiteReexpedition.objects.all()
        context = {
            'matricule': matricule,
            'profile': profile,
            'nom_agence': nom_agence,
            'villes': villes,
            'prixs':prixs,
        }
        return render(request, 'reexpedition.html',context)
    else :
        return redirect('logout')
        


def reexpedition_save(request):
    tva=0.20
    prix_ht=0
    prix_ttc=0
    if request.session.get('matricule') and request.session.get('password'):
        panier=models.Panier.objects.filter(num_Panier=request.session.get('num_Panier')).first()
        activite=models.Activite.objects.filter(num_activite="R").first()
        agent=models.Agent.objects.filter(matricule=request.session.get('matricule')).first()
        expediteur=models.Expediteur.objects.filter(type_expediteur=request.POST.get('type_expediteur')).first()
        PBR=models.PrixBoiteReexpedition.objects.filter(mois_abonnement=request.POST.get('mois_abonnement'),type_expediteur=expediteur).first()
        ville=models.Ville.objects.filter(code_postale=request.POST.get('code_postale')).first()
        
        save1=models.Reexpedition (num_reexp = activite.compteur,
        type_activite_id = activite,
        adresse_nouvelle = request.POST.get('adresse_nouvelle'),
        adresse_actuelle = request.POST.get('adresse_actuelle'),
        email = request.POST.get('email'),
        piece_identite = request.POST.get('piece_identite'),
        mois_abonnement= PBR,
        code_postale = request.POST.get('code_postale'),
        nom_ville =ville.nom_ville,
        num_tel_exp =request.POST.get('num_tel_exp'),
        type_expediteur = PBR,
        date = datetime.datetime.now(),
        matricule = agent,
        num_panier = panier,
        status = 'actif' )
        save1.save()
        
        save2=models.Activite(num_activite="R",type_activite=activite.type_activite)
        save2.save()
        
        prix=request.POST.get('prix')
        prix_ht =(float(prix)  + prix_ht) 
        prix_ttc = (prix_ht * tva)+prix_ht
        save3=models.Panier(num_Panier =request.session.get('num_Panier'),
            num_agent = agent,
            prix_ht = prix_ht,
            prix_ttc =prix_ttc,
            status = 'actif',
            tva = tva,
            date = datetime.datetime.now())
        save3.save()
        return redirect('reexpedition')
    else :
        return redirect('logout')
 



def welcome(request):
    if request.session.get('matricule') and request.session.get('password'):
        matricule = request.session.get('matricule')
        profile= request.session.get('profile')
        nom_agence=request.session.get('nom_agence')
        context = {
            'matricule': matricule,
            'profile': profile,
            'nom_agence': nom_agence
        }
        return render(request,'sidebar.html',context)
    else :
        return redirect('logout')