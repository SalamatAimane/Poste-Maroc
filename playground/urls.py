from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


#URLconf
urlpatterns=[
    path('', views.loginPage),
    path('login/', views.LoginPage,name='LoginPage'),
    path('compte/', views.compte,name='compte'), 
    path('logout/',views.LogoutPage,name='logout'),
    path('sidebar/', views.sidebar),
]
urlpatterns += staticfiles_urlpatterns()