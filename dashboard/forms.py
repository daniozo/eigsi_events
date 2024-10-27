from django import forms
from dashboard.models import Event


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'is_public', 'event_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre de l\'évènement'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'placeholder': 'Lieu'}),
            'event_type': forms.Select(),
            'is_public': forms.CheckboxInput(),
            # 'poster': forms.FileInput(),
        }
