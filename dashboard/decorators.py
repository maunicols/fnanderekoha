from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def foundation_member_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'perfiles') and request.user.perfiles.is_foundation_member:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('landing-home')
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'perfiles') and request.user.perfiles.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Solo los administradores pueden realizar esta acción.')
        return redirect('dashboard:activity-list')
    return wrapper
