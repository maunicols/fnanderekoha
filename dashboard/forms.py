from django import forms
from .models import Activity, Participant
from django.utils import timezone

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'activity_type', 'date', 'location', 'capacity', 'status']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError("La fecha no puede ser anterior a la actual")
        return date

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su número de teléfono'
            })
        }
