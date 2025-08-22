from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . import views

urlpatterns = [
    
    path("login/", LoginView.as_view(
        template_name = "usuario/login.html",
        extra_context={"titulo": "Autenticação"}), name="login"),
    
    path("logout/", LogoutView.as_view(), name="logout"),
    
    path("alterar-senha/", PasswordChangeView.as_view(
        template_name="usuario/password_change.html",
        extra_context={"titulo": "Alterar minha senha"}), name="alterar-senha"),
    
    path("registro/", views.RegistroView.as_view(), name="registro"),

]


