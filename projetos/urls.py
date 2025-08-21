from django.urls import path
from . import views

app_name = 'projetos'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Equipes
    path('equipes/', views.EquipeListView.as_view(), name='lista-equipes'),
    path('equipes/criar/', views.EquipeCreateView.as_view(), name='criar-equipe'),
    path('equipes/<int:pk>/', views.EquipeDetailView.as_view(), name='detalhe-equipe'),
    path('equipes/<int:pk>/excluir/', views.EquipeDeleteView.as_view(), name='excluir-equipe'),
    
    # Projetos
    path('projetos/', views.ProjetoListView.as_view(), name='lista-projetos'),
    path('projetos/criar/', views.ProjetoCreateView.as_view(), name='criar-projeto'),
    path('projetos/<int:pk>/', views.ProjetoDetailView.as_view(), name='detalhe-projeto'),
    path('projetos/<int:pk>/excluir/', views.ProjetoDeleteView.as_view(), name='excluir-projeto'),
    path('equipes/<int:equipe_id>/projetos/criar/', views.ProjetoCreateView.as_view(), name='criar-projeto-equipe'),
    
    # Tarefas
    path('projetos/<int:pk>/kanban/', views.KanbanView.as_view(), name='kanban-projeto'),
    path('projetos/<int:projeto_id>/tarefas/criar/', views.TarefaCreateView.as_view(), name='criar-tarefa'),
    path('tarefas/<int:pk>/', views.TarefaDetailView.as_view(), name='detalhe-tarefa'),
    
    # Funcionalidades do Kanban
    path('mover-tarefa/', views.mover_tarefa, name='mover-tarefa'),
    
    # Comentários
    path('tarefas/<int:tarefa_id>/comentarios/', views.adicionar_comentario, name='adicionar-comentario'),
    
    # Atribuições
    path('tarefas/<int:tarefa_id>/atribuir/', views.atribuir_tarefa, name='atribuir-tarefa'),
    path('tarefas/<int:tarefa_id>/remover-atribuicao/', views.remover_atribuicao, name='remover-atribuicao'),
]
