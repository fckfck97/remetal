from django.urls import path
from .views import Home, PerfilView, HomeSinPrivilegios
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', Home.as_view(), name='home'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('account/login/', auth_views.LoginView.as_view(template_name='base/login.html'),
         name='login'),
    path('account/logout/',
         auth_views.LogoutView.as_view(template_name='base/login.html'),
         name='logout'),
    path('sin_privilegios/', HomeSinPrivilegios.as_view(), name='sin_privilegios'),

]
