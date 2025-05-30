from django import forms
from .models import Activity, Participant, ActivityFile
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

class ActivityFileForm(forms.ModelForm):
    class Meta:
        model = ActivityFile
        fields = ['file', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DocumentUploadForm(forms.ModelForm):
    activity = forms.ModelChoiceField(
        queryset=Activity.objects.all(),
        label='Actividad',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ActivityFile
        fields = ['title', 'description', 'file', 'activity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
