from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistroUsuarioForm

class RegistroView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'usuario/registro.html'
    success_url = reverse_lazy('projetos:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, form.instance)
        messages.success(self.request, 'Conta criada com sucesso! Bem-vindo ao Sistema Kanban!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar conta. Verifique os dados informados.')
        return super().form_invalid(form)
