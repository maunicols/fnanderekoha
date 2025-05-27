from django.contrib import admin
from .models import Activity, Participant

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'date', 'status', 'location')
    list_filter = ('activity_type', 'status', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    inlines = [ParticipantInline]

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
