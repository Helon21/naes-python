from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Max
from django.utils import timezone
from datetime import datetime, timedelta
import json

from django.contrib.auth.models import User
from .models import (
    Equipe, Projeto, Tarefa, StatusTarefa, Etiqueta, 
    MembroEquipe, Atribuicao, Comentario, Anexo
)

# Views para Equipes
class EquipeListView(LoginRequiredMixin, ListView):
    model = Equipe
    template_name = 'projetos/equipe/lista.html'
    context_object_name = 'equipes'
    
    def get_queryset(self):
        # Mostra apenas equipes onde o usuário é membro
        return Equipe.objects.filter(
            membros__usuario=self.request.user,
            ativa=True
        ).distinct()

class EquipeDetailView(LoginRequiredMixin, DetailView):
    model = Equipe
    template_name = 'projetos/equipe/detalhe.html'
    context_object_name = 'equipe'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projetos'] = self.object.projetos.filter(ativo=True)
        context['membros'] = self.object.membros.all()
        return context

class EquipeCreateView(LoginRequiredMixin, CreateView):
    model = Equipe
    template_name = 'projetos/equipe/form.html'
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('projetos:lista-equipes')
    
    def form_valid(self, form):
        form.instance.criada_por = self.request.user
        response = super().form_valid(form)
        
        # Adiciona o criador como administrador da equipe
        MembroEquipe.objects.create(
            usuario=self.request.user,
            equipe=form.instance,
            papel='admin'
        )
        
        # Cria status padrão para a equipe
        status_padrao = [
            ('A Fazer', '#6c757d', 1),
            ('Em Andamento', '#007bff', 2),
            ('Em Revisão', '#ffc107', 3),
            ('Concluído', '#28a745', 4),
        ]
        
        for nome, cor, ordem in status_padrao:
            StatusTarefa.objects.create(
                nome=nome,
                cor=cor,
                ordem=ordem,
                equipe=form.instance
            )
        
        messages.success(self.request, 'Equipe criada com sucesso!')
        return response

class EquipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipe
    template_name = 'projetos/equipe/confirmar_exclusao.html'
    success_url = reverse_lazy('projetos:dashboard')
    
    def delete(self, request, *args, **kwargs):
        equipe = self.get_object()
        
        # Verifica se o usuário é administrador da equipe
        if not equipe.membros.filter(usuario=request.user, papel='admin').exists():
            messages.error(request, 'Você não tem permissão para excluir esta equipe!')
            return redirect('projetos:detalhe-equipe', pk=equipe.pk)
        
        # Verifica se há projetos ativos na equipe
        if equipe.projetos.filter(ativo=True).exists():
            messages.error(request, 'Não é possível excluir uma equipe com projetos ativos!')
            return redirect('projetos:detalhe-equipe', pk=equipe.pk)
        
        # Marca a equipe como inativa em vez de excluir fisicamente
        equipe.ativa = False
        equipe.save()
        
        messages.success(request, f'Equipe "{equipe.nome}" foi desativada com sucesso!')
        return redirect(self.get_success_url())

# Views para Projetos
class ProjetoListView(LoginRequiredMixin, ListView):
    model = Projeto
    template_name = 'projetos/projeto/lista.html'
    context_object_name = 'projetos'
    
    def get_queryset(self):
        equipe_id = self.kwargs.get('equipe_id')
        if equipe_id:
            return Projeto.objects.filter(
                equipe_id=equipe_id,
                ativo=True,
                equipe__membros__usuario=self.request.user
            )
        return Projeto.objects.filter(
            equipe__membros__usuario=self.request.user,
            ativo=True
        )

class ProjetoDetailView(LoginRequiredMixin, DetailView):
    model = Projeto
    template_name = 'projetos/projeto/detalhe.html'
    context_object_name = 'projeto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarefas'] = self.object.tarefas.all()
        context['status_list'] = self.object.equipe.status_tarefas.all()
        
        # Calcular estatísticas por status
        context['status_stats'] = {}
        for status in context['status_list']:
            count = self.object.tarefas.filter(status=status).count()
            context['status_stats'][status.nome] = count
        return context

class ProjetoCreateView(LoginRequiredMixin, CreateView):
    model = Projeto
    template_name = 'projetos/projeto/form.html'
    fields = ['titulo', 'descricao', 'data_inicio', 'data_fim', 'prioridade']
    
    def get_success_url(self):
        return reverse('projetos:detalhe-projeto', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        equipe_id = self.kwargs.get('equipe_id')
        if equipe_id:
            form.instance.equipe_id = equipe_id
        else:
            # Se não há equipe_id, usar a primeira equipe do usuário
            primeira_equipe = Equipe.objects.filter(
                membros__usuario=self.request.user,
                ativa=True
            ).first()
            if primeira_equipe:
                form.instance.equipe = primeira_equipe
            else:
                messages.error(self.request, 'Você precisa participar de uma equipe para criar projetos.')
                return self.form_invalid(form)
        
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Projeto criado com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipe_id'] = self.kwargs.get('equipe_id')
        return context

class ProjetoDeleteView(LoginRequiredMixin, DeleteView):
    model = Projeto
    template_name = 'projetos/projeto/confirmar_exclusao.html'
    
    def get_success_url(self):
        return reverse('projetos:detalhe-equipe', kwargs={'pk': self.object.equipe.pk})
    
    def delete(self, request, *args, **kwargs):
        projeto = self.get_object()
        
        # Verifica se o usuário tem permissão para excluir o projeto
        if not projeto.equipe.membros.filter(usuario=request.user, papel='admin').exists():
            messages.error(request, 'Você não tem permissão para excluir este projeto!')
            return redirect('projetos:detalhe-projeto', pk=projeto.pk)
        
        # Marca o projeto como inativo em vez de excluir fisicamente
        projeto.ativo = False
        projeto.save()
        
        messages.success(request, f'Projeto "{projeto.titulo}" foi desativado com sucesso!')
        return redirect(self.get_success_url())

# Views para Tarefas (Kanban)
class KanbanView(LoginRequiredMixin, DetailView):
    model = Projeto
    template_name = 'projetos/kanban/quadro.html'
    context_object_name = 'projeto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = self.object.equipe.status_tarefas.all()
        context['etiquetas'] = self.object.equipe.etiquetas.all()
        return context

@login_required
def mover_tarefa(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tarefa_id = data.get('tarefa_id')
        novo_status_id = data.get('novo_status_id')
        nova_ordem = data.get('nova_ordem')
        
        try:
            tarefa = Tarefa.objects.get(id=tarefa_id)
            novo_status = StatusTarefa.objects.get(id=novo_status_id)
            
            # Verifica se o usuário tem permissão para mover a tarefa
            if not tarefa.projeto.equipe.membros.filter(usuario=request.user).exists():
                return JsonResponse({'success': False, 'error': 'Sem permissão'})
            
            tarefa.status = novo_status
            tarefa.ordem = nova_ordem
            tarefa.save()
            
            return JsonResponse({'success': True})
        except (Tarefa.DoesNotExist, StatusTarefa.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Tarefa ou status não encontrado'})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

class TarefaCreateView(LoginRequiredMixin, CreateView):
    model = Tarefa
    template_name = 'projetos/tarefa/form.html'
    fields = ['titulo', 'descricao', 'status', 'prioridade', 'data_limite', 'etiquetas']
    
    def get_success_url(self):
        return reverse('projetos:kanban-projeto', kwargs={'pk': self.kwargs['projeto_id']})
    
    def form_valid(self, form):
        form.instance.projeto_id = self.kwargs['projeto_id']
        form.instance.criada_por = self.request.user
        
        # Define a ordem como última na coluna
        ultima_ordem = Tarefa.objects.filter(
            status=form.instance.status
        ).aggregate(ultima=Max('ordem'))['ultima'] or 0
        form.instance.ordem = ultima_ordem + 1
        
        messages.success(self.request, 'Tarefa criada com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projeto_id'] = self.kwargs['projeto_id']
        
        # Buscar o projeto para acessar a equipe
        projeto = get_object_or_404(Projeto, id=self.kwargs['projeto_id'])
        context['projeto'] = projeto
        
        # Adicionar status da equipe
        context['status_list'] = projeto.equipe.status_tarefas.all()
        
        # Adicionar etiquetas da equipe
        context['etiquetas'] = projeto.equipe.etiquetas.all()
        
        return context

class TarefaDetailView(LoginRequiredMixin, DetailView):
    model = Tarefa
    template_name = 'projetos/tarefa/detalhe.html'
    context_object_name = 'tarefa'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = self.object.comentarios.all()
        context['anexos'] = self.object.anexos.all()
        context['atribuicoes'] = self.object.atribuicoes.all()
        return context

# Views para Comentários
@login_required
def adicionar_comentario(request, tarefa_id):
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo:
            tarefa = get_object_or_404(Tarefa, id=tarefa_id)
            Comentario.objects.create(
                tarefa=tarefa,
                usuario=request.user,
                conteudo=conteudo
            )
            messages.success(request, 'Comentário adicionado com sucesso!')
        else:
            messages.error(request, 'Conteúdo do comentário é obrigatório!')
    
    return redirect('projetos:detalhe-tarefa', pk=tarefa_id)

# Views para Atribuições
@login_required
def atribuir_tarefa(request, tarefa_id):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        if usuario_id:
            tarefa = get_object_or_404(Tarefa, id=tarefa_id)
            usuario = get_object_or_404(User, id=usuario_id)
            
            # Verifica se o usuário é membro da equipe
            if not tarefa.projeto.equipe.membros.filter(usuario=usuario).exists():
                messages.error(request, 'Usuário não é membro da equipe!')
                return redirect('projetos:detalhe-tarefa', pk=tarefa_id)
            
            # Remove atribuições existentes
            Atribuicao.objects.filter(tarefa=tarefa).delete()
            
            # Cria nova atribuição
            Atribuicao.objects.create(
                tarefa=tarefa,
                usuario=usuario,
                atribuida_por=request.user
            )
            
            messages.success(request, f'Tarefa "{tarefa.titulo}" atribuída a {usuario.get_full_name() or usuario.username}!')
        else:
            messages.error(request, 'Usuário é obrigatório!')
    
    return redirect('projetos:detalhe-tarefa', pk=tarefa_id)

@login_required
def remover_atribuicao(request, tarefa_id):
    if request.method == 'POST':
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        
        # Remove todas as atribuições da tarefa
        Atribuicao.objects.filter(tarefa=tarefa).delete()
        
        messages.success(request, f'Atribuições removidas da tarefa "{tarefa.titulo}"!')
    
    return redirect('projetos:detalhe-tarefa', pk=tarefa_id)

# Dashboard
@login_required
def dashboard(request):
    # Equipes do usuário
    equipes = Equipe.objects.filter(
        membros__usuario=request.user,
        ativa=True
    )
    
    # Projetos ativos
    projetos_ativos = Projeto.objects.filter(
        equipe__membros__usuario=request.user,
        ativo=True
    )
    
    # Tarefas atribuídas ao usuário
    tarefas_atribuidas = Tarefa.objects.filter(
        atribuicoes__usuario=request.user
    ).select_related('projeto', 'status')
    
    # Estatísticas
    total_projetos = projetos_ativos.count()
    total_tarefas = Tarefa.objects.filter(
        projeto__equipe__membros__usuario=request.user
    ).count()
    
    tarefas_concluidas = Tarefa.objects.filter(
        projeto__equipe__membros__usuario=request.user,
        status__nome='Concluído'
    ).count()
    
    percentual_conclusao = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
    
    context = {
        'equipes': equipes,
        'projetos_ativos': projetos_ativos,
        'tarefas_atribuidas': tarefas_atribuidas,
        'total_projetos': total_projetos,
        'total_tarefas': total_tarefas,
        'tarefas_concluidas': tarefas_concluidas,
        'percentual_conclusao': round(percentual_conclusao, 1),
    }
    
    return render(request, 'projetos/dashboard.html', context)
