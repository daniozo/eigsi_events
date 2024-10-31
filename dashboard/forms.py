from django import forms
from django.forms import ClearableFileInput
from dashboard.models import Event, EventGallery


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'is_public', 'event_type', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre de l\'évènement'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'placeholder': 'Lieu'}),
            'event_type': forms.Select(),
            'is_public': forms.CheckboxInput(),
            'poster': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={
            'class': 'sr-only',
            'accept': 'image/*'
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class EventGalleryForm(forms.ModelForm):
    images = MultipleFileField(
        label='Images',
        required=False
    )

    class Meta:
        model = EventGallery
        fields = ['images']

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images:
            for image in images:
                if not image.content_type.startswith('image'):
                    raise forms.ValidationError("Un des fichiers n'est pas une image.")
        return images
