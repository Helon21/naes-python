from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        tipo = 'admin' if instance.username == 'Helon' else 'membro'
        PerfilUsuario.objects.get_or_create(usuario=instance, defaults={
            'tipo_usuario': tipo
        })

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
