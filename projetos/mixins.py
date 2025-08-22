from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário é administrador"""
    
    def test_func(self):
        if hasattr(self.request.user, 'perfil'):
            return self.request.user.perfil.tipo_usuario == 'admin'
        return False
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar esta funcionalidade!')
        return redirect('projetos:dashboard')

class MembroRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário é membro ou admin"""
    
    def test_func(self):
        if hasattr(self.request.user, 'perfil'):
            return self.request.user.perfil.tipo_usuario in ['admin', 'membro']
        return False
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar esta funcionalidade!')
        return redirect('projetos:dashboard')

class VisualizadorRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário tem pelo menos permissão de visualização"""
    
    def test_func(self):
        if hasattr(self.request.user, 'perfil'):
            return self.request.user.perfil.tipo_usuario in ['admin', 'membro', 'visualizador']
        return False
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para acessar esta funcionalidade!')
        return redirect('projetos:dashboard')
