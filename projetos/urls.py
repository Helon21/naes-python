from django.urls import path
from . import views

app_name = 'projetos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('equipes/', views.EquipeListView.as_view(), name='lista-equipes'),
    path('equipes/criar/', views.EquipeCreateView.as_view(), name='criar-equipe'),
    path('equipes/<int:pk>/', views.EquipeDetailView.as_view(), name='detalhe-equipe'),
    path('equipes/<int:pk>/excluir/', views.EquipeDeleteView.as_view(), name='excluir-equipe'),
    
    path('projetos/', views.ProjetoListView.as_view(), name='lista-projetos'),
    path('projetos/criar/', views.ProjetoCreateView.as_view(), name='criar-projeto'),
    path('projetos/<int:pk>/', views.ProjetoDetailView.as_view(), name='detalhe-projeto'),
    path('projetos/<int:pk>/excluir/', views.ProjetoDeleteView.as_view(), name='excluir-projeto'),

    
    path('projetos/<int:pk>/kanban/', views.KanbanView.as_view(), name='kanban-projeto'),
    path('projetos/<int:projeto_id>/tarefas/criar/', views.TarefaCreateView.as_view(), name='criar-tarefa'),
    path('tarefas/<int:pk>/', views.TarefaDetailView.as_view(), name='detalhe-tarefa'),
    
    path('mover-tarefa/', views.mover_tarefa, name='mover-tarefa'),
    
    path('tarefas/<int:tarefa_id>/comentarios/', views.adicionar_comentario, name='adicionar-comentario'),
    
    path('tarefas/<int:tarefa_id>/atribuir/', views.atribuir_tarefa, name='atribuir-tarefa'),
    path('tarefas/<int:tarefa_id>/remover-atribuicao/', views.remover_atribuicao, name='remover-atribuicao'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-usuarios/', views.admin_usuarios, name='admin-usuarios'),
    path('admin-usuarios/criar/', views.admin_criar_usuario, name='admin-criar-usuario'),
    path('admin-usuarios/<int:user_id>/editar/', views.admin_editar_usuario, name='admin-editar-usuario'),
    path('admin-equipes/', views.admin_equipes, name='admin-equipes'),
    path('admin-equipes/criar/', views.admin_criar_equipe_admin, name='admin-criar-equipe'),
    path('admin-equipes/<int:equipe_id>/membros/', views.admin_gerenciar_membros_equipe, name='admin-gerenciar-membros'),
    path('admin-equipes/<int:equipe_id>/toggle-status/', views.admin_toggle_equipe_status, name='admin-toggle-equipe-status'),
    path('admin-equipes/<int:equipe_id>/excluir/', views.admin_excluir_equipe, name='admin-excluir-equipe'),
]
