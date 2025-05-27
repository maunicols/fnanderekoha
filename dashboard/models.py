from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('CAPACITACION', 'Capacitación'),
        ('EVENTO', 'Evento'),
        ('REUNION', 'Reunión'),
        ('TALLER', 'Taller'),
    ]

    STATUS_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('EN_CURSO', 'En Curso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    activity_type = models.CharField('Tipo de Actividad', max_length=20, choices=ACTIVITY_TYPES)
    date = models.DateTimeField('Fecha y Hora')
    location = models.CharField('Ubicación', max_length=200)
    capacity = models.PositiveIntegerField('Capacidad', null=True, blank=True)
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='PROGRAMADA')
    
    # Metadatos
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última Actualización', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activities_created'
    )

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.title}"

class Participant(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    name = models.CharField('Nombre', max_length=200)
    email = models.EmailField('Correo Electrónico', blank=True)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    attendance_confirmed = models.BooleanField('Asistencia Confirmada', default=False)
    notes = models.TextField('Notas', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        unique_together = ['activity', 'email']  # Evita duplicados en la misma actividad

    def __str__(self):
        return f"{self.name} - {self.activity.title}"
