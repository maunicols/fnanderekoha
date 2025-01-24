from django import forms
from .models import Mensaje


class FormularioMensaje(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ["asunto", "email", "autor", "contenido"]

        widgets = {
            "autor": forms.Select(attrs={"hidden":"", "value": "{{user.username}}"}),
            "contenido": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {"autor": ""}

    def __init__(self, *args, is_authenticated=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if is_authenticated:
            self.fields['autor'].widget.attrs.pop('hidden')
            self.fields['email'].widget.attrs.update({"readonly":"true"})
            self.fields['autor'].widget.attrs.update({"disabled":"true"})
            self.fields['autor'].label = 'Autor'