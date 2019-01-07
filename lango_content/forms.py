from django import forms
from .models import Sentence


class SentenceInlineForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'size': 100}),
        }

