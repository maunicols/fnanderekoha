from django.contrib import admin
from .models import Activity, Participant, ActivityFile

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1

class ActivityFileInline(admin.TabularInline):
    model = ActivityFile
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'date', 'status', 'location')
    list_filter = ('activity_type', 'status', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    inlines = [ActivityFileInline, ParticipantInline]

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva actividad
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity', 'email', 'phone', 'attendance_confirmed')
    list_filter = ('attendance_confirmed', 'activity__activity_type')
    search_fields = ('name', 'email', 'phone')
    autocomplete_fields = ['activity']

@admin.register(ActivityFile)
class ActivityFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'activity__activity_type')
    search_fields = ('title', 'description', 'activity__title')
    date_hierarchy = 'uploaded_at'

    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo archivo
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
