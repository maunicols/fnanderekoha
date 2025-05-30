from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse, FileResponse
from .decorators import foundation_member_required, admin_required
from .models import Activity, Participant, ActivityFile
from .forms import ActivityForm, EnrollmentForm, ActivityFileForm, DocumentUploadForm
from django.utils import timezone
import json
import os

@login_required
def dashboard_home(request):
    # Actividades próximas
    upcoming_activities = Activity.objects.filter(
        date__gte=timezone.now(),
        status='PROGRAMADA'
    ).order_by('date')[:5]
    
    # Actividades en curso
    ongoing_activities = Activity.objects.filter(
        status='EN_CURSO'
    )
    
    # Estadísticas básicas
    total_participants = Participant.objects.count()
    total_activities = Activity.objects.count()
    
    context = {
        'upcoming_activities': upcoming_activities,
        'ongoing_activities': ongoing_activities,
        'total_participants': total_participants,
        'total_activities': total_activities,
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
def activity_list(request):
    activity_list = Activity.objects.all().order_by('-date')
    paginator = Paginator(activity_list, 10)  # 10 actividades por página
    
    page = request.GET.get('page')
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)
    
    # Obtener las actividades en las que el usuario está inscrito
    user_activities = set(
        Participant.objects.filter(user=request.user)
        .values_list('activity_id', flat=True)
    )
    
    return render(request, 'dashboard/activity_list.html', {
        'activities': activities,
        'page_obj': activities,
        'is_admin': request.user.perfiles.role == 'ADMIN',
        'is_staff': request.user.perfiles.role == 'STAFF',
        'is_foundation_member': request.user.perfiles.is_foundation_member,
        'user_activities': user_activities
    })

@login_required
@foundation_member_required
@admin_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            messages.success(request, 'Actividad creada exitosamente.')
            return redirect('dashboard:activity-list')
    else:
        form = ActivityForm()
    
    return render(request, 'dashboard/activity_form.html', {
        'form': form,
        'title': 'Nueva Actividad'
    })

@login_required
@foundation_member_required
@admin_required
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad actualizada exitosamente.')
            return redirect('dashboard:activity-list')
    else:
        form = ActivityForm(instance=activity)
    
    return render(request, 'dashboard/activity_form.html', {
        'form': form,
        'title': 'Editar Actividad',
        'activity': activity
    })

@login_required
@foundation_member_required
@admin_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Actividad eliminada exitosamente.')
        return redirect('dashboard:activity-list')
    
    return render(request, 'dashboard/activity_confirm_delete.html', {
        'activity': activity
    })

@login_required
def participant_list(request):
    # Filtrar por actividad si se proporciona un ID
    activity_id = request.GET.get('activity')
    if activity_id:
        participant_list = Participant.objects.filter(activity_id=activity_id).order_by('-created_at')
        activity = get_object_or_404(Activity, pk=activity_id)
    else:
        participant_list = Participant.objects.all().order_by('-created_at')
        activity = None

    paginator = Paginator(participant_list, 15)  # 15 participantes por página
    
    page = request.GET.get('page')
    try:
        participants = paginator.page(page)
    except PageNotAnInteger:
        participants = paginator.page(1)
    except EmptyPage:
        participants = paginator.page(paginator.num_pages)
    
    return render(request, 'dashboard/participant_list.html', {
        'participants': participants,
        'page_obj': participants,  # Necesario para la paginación
        'activity': activity,
        'is_admin': request.user.perfiles.role == 'ADMIN',
        'is_foundation_member': request.user.perfiles.is_foundation_member
    })

@login_required
def activity_enroll(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    
    # Verificar si ya está inscrito
    if Participant.objects.filter(activity=activity, user=request.user).exists():
        messages.warning(request, 'Ya estás inscrito en esta actividad.')
        return redirect('dashboard:activity-list')
    
    # Verificar si está abierta para inscripciones
    if not activity.is_open_for_enrollment():
        messages.error(request, 'No es posible inscribirse en esta actividad en este momento.')
        return redirect('dashboard:activity-list')
    
    # Verificar capacidad
    if not activity.has_available_capacity():
        messages.error(request, 'Lo sentimos, esta actividad ya está llena.')
        return redirect('dashboard:activity-list')
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            # Crear participante con información del usuario
            name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            
            participant = form.save(commit=False)
            participant.activity = activity
            participant.user = request.user
            participant.name = name
            participant.email = request.user.email
            participant.attendance_confirmed = False
            participant.save()
            
            messages.success(request, f'Te has inscrito exitosamente en {activity.title}.')
            return redirect('dashboard:activity-list')
    else:
        form = EnrollmentForm()
    
    return render(request, 'dashboard/activity_enroll.html', {
        'form': form,
        'activity': activity
    })

@login_required
def activity_unenroll(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    participant = get_object_or_404(Participant, activity=activity, user=request.user)
    
    # Verificar si está abierta para cambios
    if not activity.is_open_for_enrollment():
        messages.error(request, 'No es posible cancelar la inscripción en esta actividad en este momento.')
        return redirect('dashboard:activity-list')
    
    participant.delete()
    messages.success(request, f'Has cancelado tu inscripción en {activity.title}.')
    return redirect('dashboard:activity-list')

@login_required
def activity_change_status(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    
    # Verificar permisos
    if not activity.can_manage_attendance(request.user):
        return JsonResponse({
            'success': False,
            'message': 'No tienes permisos para cambiar el estado de esta actividad'
        })
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status not in dict(Activity.STATUS_CHOICES):
                return JsonResponse({
                    'success': False,
                    'message': 'Estado inválido'
                })
            
            # No permitir cambiar a PROGRAMADA si ya estaba EN_CURSO o COMPLETADA
            if new_status == 'PROGRAMADA' and activity.status in ['EN_CURSO', 'COMPLETADA']:
                return JsonResponse({
                    'success': False,
                    'message': 'No se puede cambiar a Programada una actividad que ya está en curso o completada'
                })
            
            activity.status = new_status
            activity.save()
            
            return JsonResponse({'success': True})
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Datos inválidos'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })

@login_required
@foundation_member_required
def confirm_attendance(request, participant_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            confirmed = data.get('confirmed', False)
            
            participant = get_object_or_404(Participant, pk=participant_id)
            participant.attendance_confirmed = confirmed
            participant.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Asistencia actualizada exitosamente',
                'confirmed': participant.attendance_confirmed
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Datos inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)

@login_required
def library_view(request):
    """Vista de la biblioteca de documentos."""
    activities = Activity.objects.prefetch_related('files').order_by('-date')
    
    if request.user.perfiles.is_foundation_member:
        form = DocumentUploadForm()
    else:
        form = None
    
    return render(request, 'dashboard/library.html', {
        'activities': activities,
        'can_upload': request.user.perfiles.is_foundation_member,
        'form': form,
    })

@login_required
@foundation_member_required
def upload_document(request):
    """Vista para subir documentos."""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('dashboard:library')
        else:
            messages.error(request, 'Error al subir el documento.')
            return redirect('dashboard:library')
    return redirect('dashboard:library')

@login_required
def download_document(request, file_id):
    """Vista para descargar documentos."""
    document = get_object_or_404(ActivityFile, pk=file_id)
    try:
        response = FileResponse(document.file)
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response
    except Exception as e:
        messages.error(request, 'Error al descargar el archivo.')
        return redirect('dashboard:library')

@login_required
def activity_detail(request, pk):
    """Vista detallada de una actividad."""
    activity = get_object_or_404(Activity, pk=pk)
    
    context = {
        'activity': activity,
        'is_enrolled': Participant.objects.filter(activity=activity, user=request.user).exists(),
    }
    return render(request, 'dashboard/activity_detail.html', context)
