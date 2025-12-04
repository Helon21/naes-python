# Checklist de Requisitos do Projeto

## ✅ Implementado

1. **select_related** - ✅ Já está sendo usado em algumas views:
   - `KanbanView`: `select_related('status')`
   - `admin_usuarios`: `select_related('projeto', 'status')`
   - `admin_equipes`: `select_related('usuario')`
   - `admin_gerenciar_membros_equipe`: `prefetch_related('membros__usuario')`

2. **form_valid realizando tarefas com outras classes** - ✅ Implementado:
   - `EquipeCreateView.form_valid`: Cria `MembroEquipe` após criar equipe
   - `TarefaCreateView.form_valid`: Cria `Anexo` após criar tarefa, calcula ordem

3. **jQuery** - ✅ jQuery está incluído no base.html

4. **Interface amigável e fluxo coerente** - ✅ Sistema completo com navegação funcional

## ❌ Faltando Implementar

1. **Django Debug Toolbar** - ❌ Não está instalado/configurado
   - Precisa adicionar ao requirements.txt
   - Precisa configurar no settings.py

2. **Django Filter** - ❌ Não está implementado
   - Precisa instalar django-filter
   - Implementar em pelo menos 2 ListViews (EquipeListView e ProjetoListView)

3. **Lookups em filtros** - ❌ Não está implementado
   - Precisa usar: icontains, exact, gte, lte

4. **Paginação** - ❌ Não está implementada
   - Precisa adicionar `paginate_by` nas ListViews
   - Precisa adicionar controles de paginação nos templates

5. **Bibliotecas JavaScript** - ⚠️ Parcialmente implementado
   - jQuery: ✅ Implementado
   - DataTables: ❌ Não implementado
   - Máscaras: ⚠️ Parcial (tem máscara de data em projeto/form.html)
   - Galeria de fotos: ❌ Não implementado
   - Calendário: ⚠️ Usa datetime-local nativo

## 📋 Plano de Implementação

### Prioridade Alta (Requisitos obrigatórios):
1. Django Debug Toolbar
2. Django Filter com lookups (icontains, exact, gte, lte)
3. Paginação nas ListViews

### Prioridade Média (Melhorias):
4. DataTables em pelo menos uma lista
5. Máscaras em mais campos
6. Galeria de fotos para anexos

