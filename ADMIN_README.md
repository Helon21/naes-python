# 🚀 Sistema Administrativo - NAES2025

## 📋 Visão Geral

O sistema administrativo foi criado para dar aos administradores controle total sobre usuários, equipes e projetos. Apenas usuários com tipo "admin" podem acessar estas funcionalidades.

## 🔐 Acesso Administrativo

### Login como Administrador
1. Acesse: `http://127.0.0.1:8000/login/`
2. Use as credenciais da conta admin:
   - **Usuário:** `admin`
   - **Senha:** (a que você criou)

### Verificar Tipo de Usuário
- Apenas usuários com `perfil.tipo_usuario = 'admin'` podem acessar o painel administrativo
- Usuários normais verão apenas o menu padrão

## 🎯 Funcionalidades Administrativas

### 1. Dashboard Administrativo
- **URL:** `/projetos/admin-dashboard/`
- **Funcionalidades:**
  - Estatísticas gerais do sistema
  - Contadores de usuários, equipes, projetos e tarefas
  - Gráfico de usuários por tipo
  - Lista de equipes ativas
  - Ações rápidas para criar usuários e equipes

### 2. Gerenciamento de Usuários
- **URL:** `/projetos/admin-usuarios/`
- **Funcionalidades:**
  - Listar todos os usuários do sistema
  - Filtrar por tipo de usuário, status e busca por nome
  - Ver informações detalhadas de cada usuário
  - Editar usuários existentes
  - Ativar/desativar usuários

### 3. Criação de Usuários
- **URL:** `/projetos/admin-usuarios/criar/`
- **Funcionalidades:**
  - Criar novos usuários com senha
  - Definir tipo de usuário (admin ou membro)
  - Configurar nome, sobrenome e email
  - Validação automática de dados

### 4. Edição de Usuários
- **URL:** `/projetos/admin-usuarios/<id>/editar/`
- **Funcionalidades:**
  - Modificar dados pessoais
  - Alterar tipo de usuário
  - Ativar/desativar conta
  - Manter histórico de alterações

### 5. Gerenciamento de Equipes
- **URL:** `/projetos/admin-equipes/`
- **Funcionalidades:**
  - Listar todas as equipes
  - Filtrar por status e quantidade de membros
  - Ver detalhes de cada equipe
  - Ativar/desativar equipes
  - Excluir equipes (com confirmação)
  - **Nota:** Edição de equipes não está disponível no momento

### 6. Criação de Equipes (Exclusivo para Admins)
- **URL:** `/projetos/admin-equipes/criar/`
- **Funcionalidades:**
  - Criar novas equipes (apenas administradores)
  - Definir nome e descrição
  - Configurar status ativo/inativo
  - Preparar para adição de membros
  - **Importante:** Usuários normais não podem criar equipes
  - **Status automático:** Cria automaticamente 4 status padrão para tarefas

### 7. Gerenciamento de Membros de Equipes (Exclusivo para Admins)
- **URL:** `/projetos/admin-equipes/<equipe_id>/membros/`
- **Funcionalidades:**
  - Adicionar novos usuários às equipes
  - Definir papel de cada membro (Administrador ou Membro)
  - Alterar papel de membros existentes
  - Remover membros das equipes
  - Visualizar lista completa de membros
  - **Proteção:** Criador da equipe não pode ser removido

### 8. Criação de Projetos (Exclusivo para Admins)
- **URL:** `/projetos/projetos/criar/`
- **Funcionalidades:**
  - Criar novos projetos dentro de equipes específicas
  - Acesso direto através do dashboard de gerenciamento de equipes
  - **Restrição:** Apenas administradores podem criar projetos
  - **Integração:** Botão de criação disponível na lista de equipes administrativas

## 🎨 Interface do Usuário

### Menu de Navegação
- **Menu Admin:** Dropdown com todas as funcionalidades administrativas
- **Ícones:** Bootstrap Icons para melhor identificação visual
- **Responsivo:** Funciona em dispositivos móveis e desktop

### Design
- **Bootstrap 5:** Interface moderna e responsiva
- **Cards:** Organização clara das informações
- **Tabelas:** Dados organizados e fáceis de ler
- **Formulários:** Validação e feedback visual

## 🔧 Configuração Técnica

### URLs
Todas as URLs administrativas estão sob `/projetos/admin-*`:
- `admin-dashboard/` - Dashboard principal
- `admin-usuarios/` - Gerenciar usuários
- `admin-equipes/` - Gerenciar equipes
- `admin-equipes/<id>/membros/` - Gerenciar membros de equipes específicas

### URLs de Criação (Exclusivo para Admins)
- `projetos/criar/` - Criar novos projetos (apenas administradores)
- `projetos/criar/?equipe_id=<id>` - Criar projeto em equipe específica

### Restrições de Criação de Equipes
- **Usuários normais:** Não podem criar equipes
- **Administradores:** Podem criar equipes apenas através do painel administrativo
- **URLs removidas:** `/projetos/equipes/criar/` foi removida das URLs principais
- **Templates atualizados:** Botões de criação de equipes removidos da interface principal

### Permissões
- **Middleware:** Verificação automática de tipo de usuário
- **Views:** Decoradores `@login_required` com validação de admin
- **Templates:** Condicionais `{% if user.perfil.tipo_usuario == 'admin' %}`

### Formulários
- **AdminUserCreationForm:** Criação de usuários
- **AdminUserEditForm:** Edição de usuários
- **RegistroUsuarioForm:** Registro normal de usuários (com nome e sobrenome)
- **Validação:** Django forms com validação automática

## 📱 Como Usar

### 1. Primeiro Acesso
1. Faça login com a conta admin
2. Acesse o menu "Admin" no navbar
3. Clique em "Dashboard Admin" para visão geral

### 2. Criar Usuários
1. Menu Admin → "Criar Usuário"
2. Preencha os dados obrigatórios
3. Escolha o tipo de usuário
4. Clique em "Criar Usuário"

### 3. Gerenciar Equipes
1. Menu Admin → "Gerenciar Equipes"
2. Use os filtros para encontrar equipes
3. Clique nos botões de ação para editar/gerenciar

### 4. Atribuir Usuários a Equipes
1. Menu Admin → "Gerenciar Equipes"
2. Clique no botão "Gerenciar membros" (ícone de pessoas) da equipe desejada
3. Use o formulário para adicionar novos usuários
4. Configure o papel de cada membro (Administrador ou Membro)
5. Use os botões de ação para alterar papéis ou remover membros

### 5. Criar Projetos nas Equipes
1. Menu Admin → "Gerenciar Equipes"
2. Clique no botão "Criar projeto" (ícone de +) da equipe desejada
3. Preencha os dados do projeto (título, descrição, datas, prioridade)
4. Clique em "Criar Projeto"
5. O projeto será criado automaticamente na equipe selecionada

## 🚨 Segurança

### Validações
- Verificação de tipo de usuário em todas as views
- Tokens CSRF em todos os formulários
- Validação de dados nos formulários Django

### Acesso Restrito
- Apenas admins podem acessar as funcionalidades
- Redirecionamento automático para usuários não autorizados
- Mensagens de erro claras para tentativas de acesso

## 🐛 Solução de Problemas

### Funcionalidades Não Implementadas
- **Edição de Equipes:** Botão de edição foi removido da interface
- **Ativação/Desativação:** Funcionalidade visual implementada, mas sem backend
- **Exclusão de Equipes:** Modal de confirmação implementado, mas sem backend

### Erro de Acesso Negado
- Verifique se o usuário tem `tipo_usuario = 'admin'`
- Confirme se o perfil foi criado corretamente

### Erro de Criação de Equipe (UNIQUE constraint)
- **Problema:** `UNIQUE constraint failed: projetos_statustarefa.ordem`
- **Causa:** Conflito na criação de status padrão devido a restrição UNIQUE incorreta no modelo
- **Solução:** 
  - Campo `ordem` corrigido para permitir valores duplicados entre equipes
  - Sistema calcula ordem automaticamente por equipe
  - Migração aplicada para atualizar banco de dados
- **Status padrão:** A Fazer, Em Andamento, Em Revisão, Concluído
- **Importante:** Cada equipe pode ter seus próprios status com ordens 1, 2, 3, 4

### Usuário não aparece na lista
- Verifique se o usuário está ativo (`is_active = True`)
- Confirme se o perfil foi criado

### Equipe não aparece
- Verifique o status da equipe (`ativa = True`)
- Confirme se há projetos associados

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do Django
2. Confirme as permissões do usuário
3. Teste com uma conta admin recém-criada

---

**Desenvolvido com ❤️ para o sistema NAES2025**
