from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone


class Ville(models.Model):
    code_postale = models.IntegerField(primary_key=True)
    nom_ville = models.CharField(max_length=50)

class Agence(models.Model):
    num_agence = models.CharField(max_length=10, primary_key=True)
    nom_agence = models.CharField(max_length=50)
    code_postal = models.ForeignKey(Ville, on_delete=models.CASCADE)

    
class Agent(models.Model):
    matricule = models.CharField(max_length=10, primary_key=True)
    nom_complet = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    profile = models.CharField(max_length=100)
    num_agence = models.ForeignKey(Agence, on_delete=models.CASCADE)

class Activite(models.Model):
    num_activite = models.CharField(max_length=10) 
    type_activite = models.CharField(max_length=100, primary_key=True)
    compteur = models.IntegerField()

class Expediteur(models.Model):
    num_expediteur = models.CharField(max_length=10, primary_key=True)
    type_expediteur = models.CharField(max_length=100)

class Panier(models.Model):
    num_Panier = models.IntegerField( primary_key=True)
    num_agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    prix_ht = models.DecimalField(max_digits=8, decimal_places=2)
    prix_ttc = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=100)
    tva = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True) #date system

class Recu(models.Model):
    num_recu = models.IntegerField(primary_key=True)
    num_panier = models.ForeignKey(Panier, on_delete=models.CASCADE)

class PrixBoiteReexpedition(models.Model):
    type_activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    mois_abonnement = models.CharField(max_length=10)
    type_expediteur = models.ForeignKey(Expediteur, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['type_activite', 'mois_abonnement', 'type_expediteur'],
                name='prix_boite_reexpedition_unique_constraint'
            )
        ]

class Reexpedition(models.Model):
    num_reexp = models.CharField(max_length=10, primary_key=True)
    type_activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    adresse_nouvelle = models.CharField(max_length=100)
    adresse_actuelle = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()]) #control de l'email
    piece_identite = models.CharField(max_length=100)
    mois_abonnement = models.ForeignKey(PrixBoiteReexpedition, on_delete=models.CASCADE,  limit_choices_to=models.Q(), related_name='reexpedition_mois_abonnement')
    code_postale = models.IntegerField()
    nom_ville = models.CharField(max_length=20)
    num_tel_exp = models.CharField(max_length=20)
    type_expediteur = models.ForeignKey(PrixBoiteReexpedition, on_delete=models.CASCADE,  limit_choices_to=models.Q(), related_name='reexpedition_type_expediteur')
    date = models.DateTimeField(auto_now_add=True) #date system
    matricule = models.ForeignKey(Agent, on_delete=models.CASCADE)
    num_panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        ville = Ville.objects.get(nom_ville=self.nom_ville)
        self.code_postale = ville.code_postale
        super(Reexpedition, self).save(*args, **kwargs)



class BoitePostale(models.Model):
    num_boite = models.CharField(max_length=10, primary_key=True)
    type_activite = models.ForeignKey(PrixBoiteReexpedition, on_delete=models.CASCADE, limit_choices_to=models.Q(), related_name='boitepostale_type_activite')
    adresse_client = models.CharField(max_length=100)
    email_client = models.EmailField(validators=[EmailValidator()]) #control de l'email
    piece_identite = models.CharField(max_length=100)
    nom_client = models.CharField(max_length=100)
    code_postale = models.IntegerField()
    nom_ville = models.CharField(max_length=20)
    mois_abonnement = models.ForeignKey(PrixBoiteReexpedition, on_delete=models.CASCADE, limit_choices_to=models.Q(), related_name='boitepostale_mois_abonnement')
    num_tel_exp = models.CharField(max_length=20)
    type_expediteur = models.ForeignKey(PrixBoiteReexpedition, on_delete=models.CASCADE, limit_choices_to=models.Q(), related_name='boitepostale_type_expediteur')
    date = models.DateTimeField(auto_now_add=True) #date system
    matricule = models.ForeignKey(Agent, on_delete=models.CASCADE)
    num_panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        ville = Ville.objects.get(nom_ville=self.nom_ville)
        self.code_postale = ville.code_postale
        super(Reexpedition, self).save(*args, **kwargs)

class PrixColisCourrier(models.Model):
    poids_inf = models.DecimalField(max_digits=5, decimal_places=3)
    poids_sup = models.DecimalField(max_digits=5, decimal_places=3)
    type_activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['type_activite', 'poids_inf', 'poids_sup'],
                name='prix_colis_courrier_unique_constraint'
            )
        ]


class Colis(models.Model):
    num_colis = models.CharField(max_length=10, primary_key=True)
    type_activite = models.ForeignKey(Activite, on_delete=models.CASCADE, limit_choices_to=models.Q())
    adresse_destinataire = models.CharField(max_length=100)
    email_dest = models.EmailField(validators=[EmailValidator()]) #control de l'email
    email_exped = models.EmailField(validators=[EmailValidator()]) #control de l'email
    piece_identite = models.CharField(max_length=100)
    code_postale = models.IntegerField()
    nom_ville = models.CharField(max_length=20)
    poids_inf = models.DecimalField(max_digits=5, decimal_places=3)
    poids_sup = models.DecimalField(max_digits=5, decimal_places=3)
    num_tel_exp = models.CharField(max_length=20)
    type_expediteur = models.ForeignKey(PrixColisCourrier, on_delete=models.CASCADE, limit_choices_to=models.Q())
    date = models.DateTimeField(auto_now_add=True) #date system
    matricule = models.ForeignKey(Agent, on_delete=models.CASCADE)
    num_panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        ville = Ville.objects.get(nom_ville=self.nom_ville)
        self.code_postale = ville.code_postale
        super(Reexpedition, self).save(*args, **kwargs)

class Courrier(models.Model):
    num_courrier = models.CharField(max_length=10, primary_key=True)
    type_activite = models.ForeignKey(Activite, on_delete=models.CASCADE, limit_choices_to=models.Q())
    adresse_destinataire = models.CharField(max_length=100)
    email_dest = models.EmailField(validators=[EmailValidator()]) #control de l'email
    email_exped = models.EmailField(validators=[EmailValidator()]) #control de l'email
    piece_identite = models.CharField(max_length=100)
    code_postale = models.IntegerField()
    nom_ville = models.CharField(max_length=20)
    poids_inf = models.DecimalField(max_digits=5, decimal_places=3)
    poids_sup = models.DecimalField(max_digits=5, decimal_places=3)
    num_tel_exp = models.CharField(max_length=20)
    type_expediteur = models.ForeignKey(PrixColisCourrier, on_delete=models.CASCADE, limit_choices_to=models.Q())
    date = models.DateTimeField(auto_now_add=True) #date system
    matricule = models.ForeignKey(Agent, on_delete=models.CASCADE)
    num_panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        ville = Ville.objects.get(nom_ville=self.nom_ville)
        self.code_postale = ville.code_postale
        super(Reexpedition, self).save(*args, **kwargs)





