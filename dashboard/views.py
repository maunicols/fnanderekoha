from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import foundation_member_required, admin_required
from .models import Activity, Participant
from .forms import ActivityForm
from django.utils import timezone

@login_required
@foundation_member_required
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
@foundation_member_required
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
    
    return render(request, 'dashboard/activity_list.html', {
        'activities': activities,
        'is_admin': request.user.perfiles.role == 'ADMIN'
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
@foundation_member_required
def participant_list(request):
    participant_list = Participant.objects.all().order_by('-created_at')
    paginator = Paginator(participant_list, 15)  # 15 participantes por página
    
    page = request.GET.get('page')
    try:
        participants = paginator.page(page)
    except PageNotAnInteger:
        participants = paginator.page(1)
    except EmptyPage:
        participants = paginator.page(paginator.num_pages)
    
    return render(request, 'dashboard/participant_list.html', {'participants': participants})
