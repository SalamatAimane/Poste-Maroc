from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


#URLconf
urlpatterns=[
    path('', views.LoginPage),
    path('login/', views.LoginPage,name='login'),
    path('compte/', views.Compte,name='compte'),
    path('logout/',views.LogoutPage,name='logout'),
    path('sidebar/', views.sidebar),
]
urlpatterns += staticfiles_urlpatterns()