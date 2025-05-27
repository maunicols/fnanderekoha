from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfiles

class PerfilesInline(admin.StackedInline):
    model = Perfiles
    can_delete = False
    verbose_name_plural = 'perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilesInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        return obj.perfiles.get_role_display()
    get_role.short_description = 'Rol'

# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
