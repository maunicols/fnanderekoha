from django.contrib import admin
from .models import Mensaje
from users.models import Perfiles
# Register your models here.
admin.site.register(Mensaje)
admin.site.register(Perfiles)
