from django import forms
import django_tables2 as tables

from .models import Sentence
from .models import Pos
from .models import Dependency
from .models import Pattern
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple


class SentenceInlineForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['sentence']
        widgets = {
            'sentence': forms.TextInput(attrs={'size': 100}),
        }


class PosTable(tables.Table):
    class Meta:
        model = Pos


class DependencyTable(tables.Table):
    class Meta:
        model = Dependency


class SentenceEditForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = [
            'sentence',
            'released_date',
            'source_link',
            'youtube_link',
            'difficulty',
            'level',
            'xml',
        ]
        widgets = {
            'sentence': forms.TextInput(attrs={'size': 120, 'readonly': True}),
            'released_date': forms.DateInput(),
            'source_link': forms.URLInput(attrs={'size': 120}),
            'youtube_link': forms.URLInput(attrs={'size': 120}),
            'difficulty': forms.NumberInput(),
            'level': forms.NumberInput(),
            'xml': forms.Textarea(attrs={'rows': 4, 'cols': 120}),
        }



class PatternForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ('pattern',)

        # widgets = {'pattern': CheckboxSelectMultiple()}

        def __init__(self, *args, **kwargs):
            super(PatternForm, self).__init__(*args, **kwargs)
            self.fields["pattern"].widget = CheckboxSelectMultiple()
            self.fields["pattern"].queryset = Pattern.objects.all()



