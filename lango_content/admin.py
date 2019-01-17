from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from django.urls import reverse

from .forms import SentenceInlineForm
from .models import Article
from .models import Category
from .models import Sentence
from .models import Pos
from .models import Dependency
from .models import PatternType
from .models import PatternCategory
from .models import Pattern

from django import forms
from django.contrib import admin


class SentenceInline(admin.TabularInline):
    model = Sentence
    form = SentenceInlineForm
    extra = 0
    readonly_fields = ('edit_link',)

    @staticmethod
    def edit_link(obj):
        if obj.id:
            return mark_safe('<a target="_blank" href="{}">Full edit</a>'.format(
                reverse('lango_content:sentence_edit', args=[obj.id, ])))
        else:
            return ''


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'source_link', 'youtube_link')
    list_filter = ['categories']
    inlines = [SentenceInline]

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class PatternAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Category)
admin.site.register(Sentence, PatternAdmin)
admin.site.register(Pos)
admin.site.register(Dependency)
admin.site.register(Article, ArticleAdmin)
admin.site.register(PatternType)
admin.site.register(PatternCategory)
admin.site.register(Pattern)