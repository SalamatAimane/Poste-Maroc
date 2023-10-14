from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


#URLconf
urlpatterns=[
    path('', views.Login,name='Login'),
    path('login/', views.LoginPage,name='LoginPage'),
    path('compte/', views.compte,name='compte'), 
    path('logout/',views.LogoutPage,name='logout'),
    path('save/',views.save,name='save'),
    path('reexpedition_save/',views.reexpedition_save,name='reexpedition_save'),
    path('reexpedition/',views.reexpedition,name='reexpedition'),
    path('welcome/',views.welcome,name='welcome'),
    path('Ajouter_Colis', views.Ajouter_Colis, name='Ajouter_Colis'),
    path('P_colis/', views.P_colis, name='P_colis'),
    path('ajouter_courrier/', views.ajouter_courrier, name='ajouter_courrier'),
    path('P_C/', views.P_C, name='P_C'),
    path('valider_panier/', views.valider_panier, name='valider_panier'),
    # Chemin pour annuler l'opération
    path('annuler/', views.annuler, name='annuler'),
    path('courrier_save/', views.courrier_save, name='courrier_save'),
    path('courrier/',views.courrier,name='courrier'),
    path('colis/',views.colis,name='colis'),
    path('P_colis/',views.P_colis,name='P_colis'),
    path(' ajouter_colis/',views.ajouter_colis,name=' ajouter_colis'),
    path('Panier/', views.afficher_panier, name='Panier'),
    
    
    
]
urlpatterns += staticfiles_urlpatterns()