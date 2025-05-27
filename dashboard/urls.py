from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('actividades/', views.activity_list, name='activity-list'),
    path('actividades/nueva/', views.activity_create, name='activity-create'),
    path('actividades/<int:pk>/editar/', views.activity_edit, name='activity-edit'),
    path('actividades/<int:pk>/eliminar/', views.activity_delete, name='activity-delete'),
    path('participantes/', views.participant_list, name='participant-list'),
]
