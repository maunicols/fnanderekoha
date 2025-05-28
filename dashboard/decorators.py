from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse

def foundation_member_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'perfiles') and request.user.perfiles.is_foundation_member:
            return view_func(request, *args, **kwargs)
            
        # Para solicitudes AJAX, devolver un error JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'No tienes permiso para realizar esta acción.'
            }, status=403)
            
        # Para solicitudes normales, redirigir con un mensaje
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
