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
    MembroEquipe, Atribuicao, Comentario, Anexo, PerfilUsuario
)
from .mixins import AdminRequiredMixin, MembroRequiredMixin

class EquipeListView(LoginRequiredMixin, ListView):
    model = Equipe
    template_name = 'projetos/equipe/lista.html'
    context_object_name = 'equipes'
    
    def get_queryset(self):
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

class EquipeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Equipe
    template_name = 'projetos/equipe/form.html'
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('projetos:lista-equipes')
    
    def form_valid(self, form):
        form.instance.criada_por = self.request.user
        response = super().form_valid(form)
        
        MembroEquipe.objects.create(
            usuario=self.request.user,
            equipe=form.instance,
            papel='admin'
        )
        

        
        messages.success(self.request, 'Equipe criada com sucesso!')
        return response

class EquipeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Equipe
    template_name = 'projetos/equipe/confirmar_exclusao.html'
    success_url = reverse_lazy('projetos:dashboard')
    
    def delete(self, request, *args, **kwargs):
        equipe = self.get_object()
        
        if not equipe.membros.filter(usuario=request.user, papel='admin').exists():
            messages.error(request, 'Você não tem permissão para inativar esta equipe!')
            return redirect('projetos:detalhe-equipe', pk=equipe.pk)
        
        # Verificar se há projetos ativos
        projetos_ativos = equipe.projetos.filter(ativo=True)
        if projetos_ativos.exists():
            # Permitir inativação, mas com aviso
            messages.warning(request, f'Equipe "{equipe.nome}" foi inativada, mas possui {projetos_ativos.count()} projeto(s) ativo(s). Os projetos continuarão funcionando.')
        else:
            messages.success(request, f'Equipe "{equipe.nome}" foi inativada com sucesso!')
        
        # Inativar a equipe
        equipe.ativa = False
        equipe.save()
        
        return redirect(self.get_success_url())

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
        context['status_list'] = StatusTarefa.objects.all()
        
        context['status_stats'] = {}
        for status in context['status_list']:
            count = self.object.tarefas.filter(status=status).count()
            context['status_stats'][status.nome] = count
        return context

class ProjetoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
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
        equipe_id = self.kwargs.get('equipe_id')
        context['equipe_id'] = equipe_id
        
        if equipe_id:
            try:
                equipe = Equipe.objects.get(id=equipe_id)
                context['equipe'] = equipe
            except Equipe.DoesNotExist:
                pass
        
        return context

class ProjetoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Projeto
    template_name = 'projetos/projeto/confirmar_exclusao.html'
    
    def get_success_url(self):
        return reverse('projetos:detalhe-equipe', kwargs={'pk': self.object.equipe.pk})
    
    def delete(self, request, *args, **kwargs):
        projeto = self.get_object()
        
        if not projeto.equipe.membros.filter(usuario=request.user, papel='admin').exists():
            messages.error(request, 'Você não tem permissão para excluir este projeto!')
            return redirect('projetos:detalhe-projeto', pk=projeto.pk)
        
        projeto.ativo = False
        projeto.save()
        
        messages.success(request, f'Projeto "{projeto.titulo}" foi desativado com sucesso!')
        return redirect(self.get_success_url())

class KanbanView(LoginRequiredMixin, DetailView):
    model = Projeto
    template_name = 'projetos/kanban/quadro.html'
    context_object_name = 'projeto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = StatusTarefa.objects.all()
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
            
            if not tarefa.projeto.equipe.membros.filter(usuario=request.user).exists():
                return JsonResponse({'success': False, 'error': 'Sem permissão'})
            

            if hasattr(request.user, 'perfil') and not request.user.perfil.pode_editar_tarefa():
                return JsonResponse({'success': False, 'error': 'Sem permissão para editar tarefas'})
            
            tarefa.status = novo_status
            tarefa.ordem = nova_ordem
            tarefa.save()
            
            return JsonResponse({'success': True})
        except (Tarefa.DoesNotExist, StatusTarefa.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Tarefa ou status não encontrado'})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

class TarefaCreateView(LoginRequiredMixin, MembroRequiredMixin, CreateView):
    model = Tarefa
    template_name = 'projetos/tarefa/form.html'
    fields = ['titulo', 'descricao', 'status', 'prioridade', 'data_limite', 'etiquetas']
    
    def get_success_url(self):
        return reverse('projetos:kanban-projeto', kwargs={'pk': self.kwargs['projeto_id']})
    
    def form_valid(self, form):
        form.instance.projeto_id = self.kwargs['projeto_id']
        form.instance.criada_por = self.request.user
        
        ultima_ordem = Tarefa.objects.filter(
            status=form.instance.status
        ).aggregate(ultima=Max('ordem'))['ultima'] or 0
        form.instance.ordem = ultima_ordem + 1
        
        messages.success(self.request, 'Tarefa criada com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projeto_id'] = self.kwargs['projeto_id']
        
        projeto = get_object_or_404(Projeto, id=self.kwargs['projeto_id'])
        context['projeto'] = projeto
        
        context['status_list'] = StatusTarefa.objects.all()

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
            
            if not tarefa.projeto.equipe.membros.filter(usuario=usuario).exists():
                messages.error(request, 'Usuário não é membro da equipe!')
                return redirect('projetos:detalhe-tarefa', pk=tarefa_id)
            
            Atribuicao.objects.filter(tarefa=tarefa).delete()
            
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
        
        Atribuicao.objects.filter(tarefa=tarefa).delete()
        
        messages.success(request, f'Atribuições removidas da tarefa "{tarefa.titulo}"!')
    
    return redirect('projetos:detalhe-tarefa', pk=tarefa_id)

# Dashboard
@login_required
def dashboard(request):
    equipes = Equipe.objects.filter(
        membros__usuario=request.user,
        ativa=True
    )
    
    projetos_ativos = Projeto.objects.filter(
        equipe__membros__usuario=request.user,
        ativo=True
    )
    
    tarefas_atribuidas = Tarefa.objects.filter(
        atribuicoes__usuario=request.user
    ).select_related('projeto', 'status')
    
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

# Views Administrativas
@login_required
def admin_dashboard(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
        return redirect('projetos:dashboard')
    
    total_usuarios = User.objects.count()
    total_equipes = Equipe.objects.count()
    total_projetos = Projeto.objects.count()
    total_tarefas = Tarefa.objects.count()
    
    usuarios_por_tipo = {}
    for choice in [('admin', 'Administrador'), ('membro', 'Membro')]:
        usuarios_por_tipo[choice[1]] = PerfilUsuario.objects.filter(tipo_usuario=choice[0]).count()
    
    equipes_ativas = Equipe.objects.filter(ativa=True)
    
    context = {
        'total_usuarios': total_usuarios,
        'total_equipes': total_equipes,
        'total_projetos': total_projetos,
        'total_tarefas': total_tarefas,
        'usuarios_por_tipo': usuarios_por_tipo,
        'equipes_ativas': equipes_ativas,
    }
    
    return render(request, 'projetos/admin/dashboard.html', context)

@login_required
def admin_usuarios(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
        return redirect('projetos:dashboard')
    
    usuarios = User.objects.select_related('perfil').all().order_by('date_joined')
    
    context = {
        'usuarios': usuarios,
    }
    
    return render(request, 'projetos/admin/usuarios.html', context)

@login_required
def admin_criar_usuario(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
        return redirect('projetos:dashboard')
    
    if request.method == 'POST':
        from .forms import AdminUserCreationForm
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuário "{user.username}" criado com sucesso!')
            return redirect('projetos:admin-usuarios')
    else:
        from .forms import AdminUserCreationForm
        form = AdminUserCreationForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Novo Usuário'
    }
    
    return render(request, 'projetos/admin/criar_usuario.html', context)

@login_required
def admin_editar_usuario(request, user_id):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
        return redirect('projetos:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        from .forms import AdminUserEditForm
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário "{user.username}" atualizado com sucesso!')
            return redirect('projetos:admin-usuarios')
    else:
        from .forms import AdminUserEditForm
        form = AdminUserEditForm(instance=user)
    
    context = {
        'form': form,
        'usuario': user,
        'titulo': f'Editar Usuário: {user.username}'
    }
    
    return render(request, 'projetos/admin/editar_usuario.html', context)

@login_required
def admin_criar_equipe_admin(request):
    """Criar equipes (apenas para admins)"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
        return redirect('projetos:dashboard')
    
    if request.method == 'POST':
        from .forms import EquipeForm
        form = EquipeForm(request.POST)
        if form.is_valid():
            equipe = form.save(commit=False)
            equipe.criada_por = request.user
            equipe.save()
            
            MembroEquipe.objects.create(
                usuario=request.user,
                equipe=equipe,
                papel='admin'
            )
            

            
            messages.success(request, f'Equipe "{equipe.nome}" criada com sucesso!')
            return redirect('projetos:admin-equipes')
    else:
        from .forms import EquipeForm
        form = EquipeForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Nova Equipe'
    }
    
    return render(request, 'projetos/admin/criar_equipe.html', context)

@login_required
def admin_equipes(request):
    """Lista todas as equipes para administradores"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
        return redirect('projetos:dashboard')
    
    equipes = Equipe.objects.prefetch_related('membros__usuario').all().order_by('nome')
    
    context = {
        'equipes': equipes,
    }
    
    return render(request, 'projetos/admin/equipes.html', context)

@login_required
def admin_gerenciar_membros_equipe(request, equipe_id):
    """Gerenciar membros de uma equipe específica (apenas para admins)"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
        return redirect('projetos:dashboard')
    
    try:
        equipe = Equipe.objects.get(id=equipe_id)
    except Equipe.DoesNotExist:
        messages.error(request, 'Equipe não encontrada.')
        return redirect('projetos:admin-equipes')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'adicionar_membro':
            usuario_id = request.POST.get('usuario_id')
            papel = request.POST.get('papel', 'membro')
            
            try:
                usuario = User.objects.get(id=usuario_id)
                
                # Verifica se o usuário já é membro da equipe
                if MembroEquipe.objects.filter(usuario=usuario, equipe=equipe).exists():
                    messages.warning(request, f'Usuário {usuario.username} já é membro desta equipe.')
                else:
                    # Adiciona o usuário à equipe
                    MembroEquipe.objects.create(
                        usuario=usuario,
                        equipe=equipe,
                        papel=papel
                    )
                    messages.success(request, f'Usuário {usuario.username} adicionado à equipe com sucesso!')
                    
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                
        elif action == 'remover_membro':
            membro_id = request.POST.get('membro_id')
            
            try:
                membro = MembroEquipe.objects.get(id=membro_id, equipe=equipe)
                nome_usuario = membro.usuario.username
                membro.delete()
                messages.success(request, f'Usuário {nome_usuario} removido da equipe com sucesso!')
                
            except MembroEquipe.DoesNotExist:
                messages.error(request, 'Membro não encontrado.')
                
        elif action == 'alterar_papel':
            membro_id = request.POST.get('membro_id')
            novo_papel = request.POST.get('novo_papel')
            
            try:
                membro = MembroEquipe.objects.get(id=membro_id, equipe=equipe)
                membro.papel = novo_papel
                membro.save()
                messages.success(request, f'Papel do usuário {membro.usuario.username} alterado para {membro.get_papel_display()}.')
                
            except MembroEquipe.DoesNotExist:
                messages.error(request, 'Membro não encontrado.')
    
    # Busca usuários disponíveis para adicionar
    usuarios_disponiveis = User.objects.filter(is_active=True).exclude(
        id__in=equipe.membros.values_list('usuario_id', flat=True)
    )
    
    # Busca membros atuais da equipe
    membros_equipe = MembroEquipe.objects.filter(equipe=equipe).select_related('usuario')
    
    context = {
        'equipe': equipe,
        'usuarios_disponiveis': usuarios_disponiveis,
        'membros_equipe': membros_equipe,
        'papel_choices': MembroEquipe.PAPEIS_CHOICES,
        'titulo': f'Gerenciar Membros - {equipe.nome}'
    }
    
    return render(request, 'projetos/admin/gerenciar_membros.html', context)

@login_required
def admin_toggle_equipe_status(request, equipe_id):
    """Ativar/Desativar equipe via AJAX (apenas para admins)"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        return JsonResponse({'success': False, 'error': 'Acesso negado. Apenas administradores podem acessar esta área.'})
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'})
    
    try:
        equipe = Equipe.objects.get(id=equipe_id)
    except Equipe.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Equipe não encontrada'})
    
    # Alternar status
    equipe.ativa = not equipe.ativa
    equipe.save()
    
    novo_status = 'ativada' if equipe.ativa else 'desativada'
    
    return JsonResponse({
        'success': True,
        'message': f'Equipe "{equipe.nome}" foi {novo_status} com sucesso!',
        'nova_status': equipe.ativa
    })

@login_required
def admin_excluir_equipe(request, equipe_id):
    """Excluir equipe via AJAX (apenas para admins)"""
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'admin':
        return JsonResponse({'success': False, 'error': 'Acesso negado. Apenas administradores podem acessar esta área.'})
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'})
    
    try:
        equipe = Equipe.objects.get(id=equipe_id)
    except Equipe.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Equipe não encontrada'})
    
    # Verificar se há projetos ativos
    projetos_ativos = equipe.projetos.filter(ativo=True)
    if projetos_ativos.exists():
        return JsonResponse({
            'success': False, 
            'error': f'Não é possível excluir a equipe "{equipe.nome}" pois ela possui {projetos_ativos.count()} projeto(s) ativo(s). Inative a equipe primeiro.'
        })
    
    # Remover todos os membros da equipe antes de excluí-la
    membros_removidos = equipe.membros.count()
    equipe.membros.all().delete()
    
    nome_equipe = equipe.nome
    equipe.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'Equipe "{nome_equipe}" foi excluída permanentemente com sucesso! {membros_removidos} membro(s) foram removidos automaticamente.'
    })
