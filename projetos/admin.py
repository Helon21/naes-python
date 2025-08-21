from django.contrib import admin
from .models import (
    PerfilUsuario, Equipe, MembroEquipe, StatusTarefa, 
    Etiqueta, Projeto, Tarefa, Atribuicao, Comentario, Anexo
)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefone', 'data_nascimento']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name']
    list_filter = ['data_nascimento']

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criada_por', 'criada_em', 'ativa']
    search_fields = ['nome', 'descricao']
    list_filter = ['ativa', 'criada_em']
    date_hierarchy = 'criada_em'

@admin.register(MembroEquipe)
class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'equipe', 'papel', 'data_entrada']
    list_filter = ['papel', 'equipe', 'data_entrada']
    search_fields = ['usuario__username', 'equipe__nome']

@admin.register(StatusTarefa)
class StatusTarefaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'equipe', 'ordem', 'cor']
    list_filter = ['equipe']
    ordering = ['equipe', 'ordem']

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'equipe', 'cor']
    list_filter = ['equipe']
    search_fields = ['nome']

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'equipe', 'criado_por', 'prioridade', 'ativo', 'data_inicio', 'data_fim']
    list_filter = ['ativo', 'prioridade', 'equipe', 'data_inicio', 'data_fim']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_em', 'atualizado_em']

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'projeto', 'status', 'prioridade', 'criada_por', 'data_limite']
    list_filter = ['status', 'prioridade', 'projeto__equipe', 'criada_em']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'criada_em'
    readonly_fields = ['criada_em', 'atualizada_em']
    filter_horizontal = ['etiquetas']

@admin.register(Atribuicao)
class AtribuicaoAdmin(admin.ModelAdmin):
    list_display = ['tarefa', 'usuario', 'atribuida_por', 'atribuida_em']
    list_filter = ['atribuida_em', 'tarefa__projeto__equipe']
    search_fields = ['usuario__username', 'tarefa__titulo']
    date_hierarchy = 'atribuida_em'

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['tarefa', 'usuario', 'criado_em']
    list_filter = ['criado_em', 'tarefa__projeto__equipe']
    search_fields = ['conteudo', 'usuario__username']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_em', 'editado_em']

@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ['nome_original', 'tarefa', 'usuario', 'tamanho', 'enviado_em']
    list_filter = ['enviado_em', 'tarefa__projeto__equipe']
    search_fields = ['nome_original', 'tarefa__titulo']
    date_hierarchy = 'enviado_em'
    readonly_fields = ['enviado_em']
