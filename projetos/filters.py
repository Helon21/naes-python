import django_filters
from django import forms
from .models import Equipe, Projeto


class EquipeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Nome da Equipe',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nome...'})
    )
    

    ativa = django_filters.ChoiceFilter(
        choices=[('', 'Todos'), ('true', 'Ativa'), ('false', 'Inativa')],
        lookup_expr='exact', 
        label='Equipe Ativa',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def filter_ativa(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(ativa=True)
        elif value == 'false':
            return queryset.filter(ativa=False)
        return queryset
    

    criada_em__gte = django_filters.DateTimeFilter(
        field_name='criada_em',
        lookup_expr='gte',
        label='Criada a partir de',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    criada_em__lte = django_filters.DateTimeFilter(
        field_name='criada_em',
        lookup_expr='lte',
        label='Criada até',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Equipe
        fields = ['nome', 'ativa', 'criada_em__gte', 'criada_em__lte']


class ProjetoFilter(django_filters.FilterSet):

    titulo = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Título do Projeto',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por título...'})
    )

    ativo = django_filters.ChoiceFilter(
        choices=[('', 'Todos'), ('true', 'Ativo'), ('false', 'Inativo')],
        lookup_expr='exact', 
        label='Projeto Ativo',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def filter_ativo(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(ativo=True)
        elif value == 'false':
            return queryset.filter(ativo=False)
        return queryset
    

    prioridade = django_filters.ChoiceFilter(
        choices=[('', 'Todas')] + list(Projeto.PRIORIDADE_CHOICES),
        lookup_expr='exact',
        label='Prioridade',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    

    data_inicio__gte = django_filters.DateFilter(
        field_name='data_inicio',
        lookup_expr='gte',
        label='Data de início a partir de',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    

    data_inicio__lte = django_filters.DateFilter(
        field_name='data_inicio',
        lookup_expr='lte',
        label='Data de início até',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    

    data_fim__gte = django_filters.DateFilter(
        field_name='data_fim',
        lookup_expr='gte',
        label='Data de fim a partir de',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    # Lookup lte para data de fim
    data_fim__lte = django_filters.DateFilter(
        field_name='data_fim',
        lookup_expr='lte',
        label='Data de fim até',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Projeto
        fields = ['titulo', 'ativo', 'prioridade', 'data_inicio__gte', 'data_inicio__lte', 
                  'data_fim__gte', 'data_fim__lte']

