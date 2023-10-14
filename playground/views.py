from django.shortcuts import render,redirect
import datetime
from . import models 
from .models import Colis, Courrier, Panier
from .models import PrixColisCourrier, Panier

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
        profile = request.session.get('profile')
        nom_agence = request.session.get('nom_agence')
        
        # Récupérer tous les objets Panier depuis la base de données
        panier_list = Panier.objects.all()
        
        context = {
            'matricule': matricule,
            'profile': profile,
            'nom_agence': nom_agence,
            'panier_list': panier_list,  # Ajoutez la liste des objets Panier au contexte
        }
        return render(request, 'sidebar.html', context)
    else:
        return redirect('logout')

    
    
    
    
    
    
    
    
    
    
    






def Ajouter_Colis(request):
    
    return render (request, 'Ajouter_Colis.html')

def P_colis(request):
    
    return render (request, 'P_colis.html')


def ajouter_courrier(request):
    # Votre logique de traitement ici, si nécessaire
    return render(request, 'Ajouter.html')  # Remplacez 'nom_de_votre_template.html' par le nom de votre template pour la page d'ajout de courrier


def P_C(request):   
    # Récupérer tous les objets Colis depuis la base de données
    courrier_list = Courrier.objects.all()
    # Passer la liste des objets Colis au modèle contextuel
    context = {'courrier_list': courrier_list} 
    return render(request, 'P_C.html',context)


def courrier_save(request):
    
    return render(request, 'P_C.html')

def courrier(request):
    matricule = request.session.get('matricule')
    profile= request.session.get('profile')
    nom_agence=request.session.get('nom_agence')
    expediteurs=models.Expediteur.objects.all()
    villes=models.Ville.objects.all()
    context = {
        'matricule': matricule,
        'profile': profile,
        'nom_agence': nom_agence,
        'expediteurs':expediteurs,
        'villes': villes,
    }
    return render(request, 'Ajouter.html',context)

def colis(request):
    matricule = request.session.get('matricule')
    profile= request.session.get('profile')
    nom_agence=request.session.get('nom_agence')
    expediteurs=models.Expediteur.objects.all()
    villes=models.Ville.objects.all()
    context = {
        'matricule': matricule,
        'profile': profile,
        'nom_agence': nom_agence,
        'expediteurs':expediteurs,
        'villes': villes,
    }
    return render(request, 'Ajouter_colis.html',context)




def P_colis(request):
    # Récupérer tous les objets Colis depuis la base de données
    colis_list = Colis.objects.all()
    # Passer la liste des objets Colis au modèle contextuel
    context = {'colis_list': colis_list}
    return render(request, 'P_colis.html',context)





def ajouter_colis(request):
  
    return render(request, 'Ajouter_Colis.html') 
    
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





def ajouter_courrier(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire soumis
        nom_article = "Courrier"  # Vous pouvez définir le nom de l'article ici
        quantite = int(request.POST.get('quantite', 1))  # Récupérer la quantité, par défaut 1 si non spécifiée
        prix_unitaire = float(request.POST.get('prix_unitaire', 0.0))  # Récupérer le prix unitaire, par défaut 0.0 si non spécifié
        prix_total = quantite * prix_unitaire  # Calculer le prix total

        # Afficher les détails du courrier avec les boutons "Valider le panier" et "Annuler"
        return render(request, 'Panier.html', {
            'nom_article': nom_article,
            'quantite': quantite,
            'prix_unitaire': prix_unitaire,
            'prix_total': prix_total
        })

    return render(request, 'Ajouter.html')  # Renvoyer la page Ajouter.html pour que l'utilisateur puisse remplir le formulaire




def valider_panier(request):
    if request.method == 'POST':
        # Récupérer les détails du formulaire
        nom_article = request.POST.get('nom_article')
        quantite = int(request.POST.get('quantite', 1))
        prix_unitaire = float(request.POST.get('prix_unitaire', 0.0))
        prix_total = float(request.POST.get('prix_total', 0.0))

        # Sauvegarder les détails du courrier dans la base de données en utilisant le modèle Cart
        new_item = Panier(
            nom_article=nom_article,
            quantite=quantite,
            prix_unitaire=prix_unitaire,
            prix_total=prix_total
            # Ajoutez d'autres champs pertinents ici selon les besoins
        )
        new_item.save()

        # Rediriger vers la page du panier ou une autre page de confirmation si nécessaire
        return redirect('panier')

def annuler(request):
    # Vous pouvez simplement rediriger l'utilisateur vers une autre page en cas d'annulation
    return redirect('')  # Remplacez 'page_d_accueil' par l'URL de la page que vous souhaitez afficher






def ajouter_au_panier(request):
    if request.method == 'POST':
        type_expediteur = request.POST.get('type_expediteur')
        poids = float(request.POST.get('Poids'))
        prix_unitaire = calculate_price(poids)  # Calculate the unit price based on the weight
        
        panier_item = Panier(type_expediteur=type_expediteur, poids=poids, prix_unitaire=prix_unitaire)
        panier_item.save()
        
        return redirect('panier')
    else:
        # Provide the list of expediteurs to the template if needed
        expediteurs = PrixColisCourrier.objects.all()
        return render(request, 'ajouter.html', {'expediteurs': expediteurs})

def calculate_price(weight):
    # Write your logic to calculate the price based on the weight
    # You can use the same logic as the one in your JavaScript code, or implement it differently here.
    # For this example, let's assume a simple calculation:
    if weight >= 0.001 and weight <= 0.5:
        return 10
    elif weight > 0.5 and weight <= 1000:
        return 12

def afficher_panier(request):
    articles = Panier.objects.all()
    
    # Vous pouvez calculer le prix total ici
    prix_total = 0
    for article in articles:
        prix_total += article.prix_ht + article.prix_ttc
    
    return render(request, 'Panier.html', {'articles': articles, 'prix_total': prix_total})







   