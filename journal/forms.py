from django import forms
from .models import JournalEntry, JournalImage

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class JournalEntryForm(forms.ModelForm):
    images = MultipleFileField(required=False, label="Photos")

    class Meta:
        model = JournalEntry
        fields = ['mood', 'content', 'audio', 'video']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your thoughts here...'}),
            'mood': forms.Select(attrs={'class': 'mood-select'}),
        }
