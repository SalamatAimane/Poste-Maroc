from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


#URLconf
urlpatterns=[
    path('', views.Login,name='Login'),
    path('login/', views.LoginPage,name='LoginPage'),
    path('compte/', views.compte,name='compte'), 
    path('logout/',views.LogoutPage,name='logout'),
    path('/save',views.save,name='save'),
]
urlpatterns += staticfiles_urlpatterns()