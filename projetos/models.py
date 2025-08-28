from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class PerfilUsuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('membro', 'Membro'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='membro')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografia")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Foto de Perfil")
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.username} ({self.get_tipo_usuario_display()})"
    
    def pode_criar_equipe(self):
        return self.tipo_usuario in ['admin']
    
    def pode_criar_projeto(self):
        return self.tipo_usuario in ['admin', 'membro']
    
    def pode_criar_tarefa(self):
        return self.tipo_usuario in ['admin', 'membro']
    
    def pode_editar_tarefa(self):
        return self.tipo_usuario in ['admin', 'membro']
    
    def pode_excluir_tarefa(self):
        return self.tipo_usuario in ['admin']
    
    def pode_excluir_projeto(self):
        return self.tipo_usuario in ['admin']
    
    def pode_excluir_equipe(self):
        return self.tipo_usuario in ['admin']
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuário"

class Equipe(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Equipe")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    criada_em = models.DateTimeField(auto_now_add=True)
    criada_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="equipes_criadas")
    ativa = models.BooleanField(default=True, verbose_name="Equipe Ativa")
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"
        ordering = ["nome"]

class MembroEquipe(models.Model):
    PAPEIS_CHOICES = [
        ('admin', 'Administrador'),
        ('membro', 'Membro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="membro_equipes")
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="membros")
    papel = models.CharField(max_length=20, choices=PAPEIS_CHOICES, default='membro')
    data_entrada = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.equipe.nome} ({self.get_papel_display()})"
    
    class Meta:
        verbose_name = "Membro da Equipe"
        verbose_name_plural = "Membros da Equipe"
        unique_together = ['usuario', 'equipe']

class StatusTarefa(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome do Status")
    cor = models.CharField(max_length=7, default="#007bff", verbose_name="Cor (Hex)")
    ordem = models.PositiveIntegerField(verbose_name="Ordem")
    
    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = "Status da Tarefa"
        verbose_name_plural = "Status das Tarefas"
        ordering = ["ordem"]
        unique_together = ['nome']

class Etiqueta(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome da Etiqueta")
    cor = models.CharField(max_length=7, default="#6c757d", verbose_name="Cor (Hex)")
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="etiquetas")
    
    def __str__(self):
        return f"{self.nome} - {self.equipe.nome}"
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        unique_together = ['nome', 'equipe']

class Projeto(models.Model):
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="projetos")
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projetos_criados")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Conclusão")
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    ativo = models.BooleanField(default=True, verbose_name="Projeto Ativo")
    
    def __str__(self):
        return f"{self.titulo} - {self.equipe.nome}"
    
    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ["-criado_em"]

class Tarefa(models.Model):
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="tarefas")
    status = models.ForeignKey(StatusTarefa, on_delete=models.CASCADE, related_name="tarefas")
    criada_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tarefas_criadas")
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)
    data_limite = models.DateTimeField(blank=True, null=True, verbose_name="Data Limite")
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name="tarefas")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem na Coluna")
    
    def __str__(self):
        return f"{self.titulo} - {self.projeto.titulo}"
    
    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ["ordem", "-criada_em"]

class Atribuicao(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="atribuicoes")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tarefas_atribuidas")
    atribuida_em = models.DateTimeField(auto_now_add=True)
    atribuida_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="atribuicoes_feitas")
    
    def __str__(self):
        return f"{self.usuario.username} - {self.tarefa.titulo}"
    
    class Meta:
        verbose_name = "Atribuição"
        verbose_name_plural = "Atribuições"
        unique_together = ['tarefa', 'usuario']

class Comentario(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="comentarios")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comentarios_feitos")
    conteudo = models.TextField(verbose_name="Conteúdo")
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.tarefa.titulo}"
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ["criado_em"]

class Anexo(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="anexos")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="anexos_enviados")
    arquivo = models.FileField(upload_to='anexos_tarefas/', verbose_name="Arquivo")
    nome_original = models.CharField(max_length=255, verbose_name="Nome Original")
    tamanho = models.PositiveIntegerField(verbose_name="Tamanho (bytes)")
    tipo_mime = models.CharField(max_length=100, verbose_name="Tipo MIME")
    enviado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome_original} - {self.tarefa.titulo}"
    
    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = ["-enviado_em"]
