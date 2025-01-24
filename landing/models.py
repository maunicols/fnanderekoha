from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Mensaje(models.Model):
    asunto = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)             # Email como clave primaria
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,                                         # autor puede ser opcional
        related_name='mensajes'
    )
    contenido = models.TextField(max_length=1000)                         # Contenido del mensaje
    creado = models.DateTimeField(auto_now_add=True)       # Fecha de creación automática

    def clean(self):
        # Llamar a las validaciones de la clase base (si existen)
        super().clean()
        
        # Asegurar que el email sea obligatorio
        if not self.email:
            # Si no se proporciona el email, intentamos obtenerlo del usuario autenticado
            if self.autor and hasattr(self.autor, 'email'):
                self.email = self.autor.email
            else:
                raise ValidationError("El campo 'email' es obligatorio para visitantes anónimos.")
        
        

    def save(self, *args, **kwargs):
        # Llamar a clean() antes de guardar
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f'Mensaje de {self.autor}, asunto: {self.asunto} '
    
