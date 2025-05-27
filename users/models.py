from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Perfiles(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('STAFF', 'Personal de la Fundación'),
        ('USER', 'Usuario'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to="profile_pics")
    role = models.CharField(
        'Rol', 
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='USER'
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    @property
    def is_foundation_member(self):
        return self.role in ['ADMIN', 'STAFF']