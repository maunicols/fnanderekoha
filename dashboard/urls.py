from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('actividades/', views.activity_list, name='activity-list'),
    path('actividades/nueva/', views.activity_create, name='activity-create'),
    path('actividades/<int:pk>/editar/', views.activity_edit, name='activity-edit'),
    path('actividades/<int:pk>/eliminar/', views.activity_delete, name='activity-delete'),
    path('actividades/<int:pk>/enlistarse/', views.activity_enroll, name='activity-enroll'),
    path('actividades/<int:pk>/desenlistarse/', views.activity_unenroll, name='activity-unenroll'),
    path('participantes/', views.participant_list, name='participant-list'),
    path('actividades/<int:pk>/cambiar-estado/', views.activity_change_status, name='activity-change-status'),
    path('participantes/<int:participant_id>/confirmar/', views.confirm_attendance, name='confirm-attendance'),
    path('activity/<int:pk>/', views.activity_detail, name='activity-detail'),
    path('library/', views.library_view, name='library'),
    path('upload-document/', views.upload_document, name='upload-document'),
    path('download-document/<int:file_id>/', views.download_document, name='download-document'),
]
