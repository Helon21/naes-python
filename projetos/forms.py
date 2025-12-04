from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Equipe, Tarefa

class AdminUserCreationForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(
        choices=PerfilUsuario.TIPO_USUARIO_CHOICES,
        label='Tipo de Usuário',
        initial='membro'
    )
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'tipo_usuario', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.tipo_usuario = self.cleaned_data['tipo_usuario']
            perfil.save()
        
        return user

class AdminUserEditForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=PerfilUsuario.TIPO_USUARIO_CHOICES,
        label='Tipo de Usuário'
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                self.fields['tipo_usuario'].initial = self.instance.perfil.tipo_usuario
            except PerfilUsuario.DoesNotExist:
                pass
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.tipo_usuario = self.cleaned_data['tipo_usuario']
            perfil.save()
        
        return user

class EquipeForm(forms.ModelForm):
    
    class Meta:
        model = Equipe
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da equipe'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite uma descrição para a equipe'
            })
        }

class TarefaForm(forms.ModelForm):
    data_limite = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M']
    )
    
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'status', 'prioridade', 'data_limite']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se for criação de tarefa (sem pk), excluir status "Concluído"
        if not self.instance.pk:
            self.fields['status'].queryset = self.fields['status'].queryset.exclude(nome='Concluído')