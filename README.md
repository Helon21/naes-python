# Sistema Kanban

Sistema de gerenciamento de projetos com quadros Kanban desenvolvido em Django.

## Funcionalidades

- **Gestão de Equipes**: Crie e gerencie equipes com diferentes níveis de permissão
- **Controle de Projetos**: Organize projetos com prazos e prioridades
- **Quadros Kanban**: Visualize tarefas em colunas com arrastar e soltar
- **Sistema de Usuários**: Autenticação e controle de acesso

## Instalação

### 1. Criar e ativar ambiente virtual

No Linux, você precisa criar um ambiente virtual para instalar pacotes Python:

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate
```

Após ativar, você verá `(venv)` no início da linha do terminal.

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar migrações

```bash
python manage.py migrate
```

### 4. Executar o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000/`

### 5. Desativar o ambiente virtual (quando terminar)

```bash
deactivate
```

**Nota**: Sempre ative o ambiente virtual antes de trabalhar no projeto!

## Usuário Administrador

O sistema já possui um usuário administrador configurado:
- **Usuário**: Helon
- **Senha**: admin123456

## Funcionalidades de Usuário

- **Login**: Acesso ao sistema com usuário e senha
- **Registro**: Criação de novas contas para membros
- **Alteração de Senha**: Usuários podem alterar suas senhas

## Estrutura do Projeto

- `naes2025/` - Configurações principais do Django
- `projetos/` - App principal com funcionalidades do kanban
- `usuario/` - Sistema de autenticação
- `paginasweb/` - Página inicial
