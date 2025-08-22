from django.views.generic import TemplateView

# Create your views here.

# Cria uma view para renderizar a página inicial
# e faz uma herança de TemplateView
class PaginaInicial(TemplateView):
    template_name = "paginasweb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nome"] = "Sistema Kanban"
        return context