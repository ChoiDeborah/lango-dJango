from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.utils.safestring import  mark_safe
from django.urls import reverse

from .forms import SentenceInlineForm
from .models import Article
from .models import Category
from .models import Sentence


class SentenceInline(admin.TabularInline):
    model = Sentence
    form = SentenceInlineForm
    extra = 0
    readonly_fields = ('change_link',)

    def change_link(self, obj):
        if obj.id:
            return mark_safe('<a target="_blank" href="{}">Full edit</a>'.format(
                reverse('admin:lango_content_sentence_change', args=[obj.id, ])))
        else:
            return ''


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'source')
    list_filter = ['categories']
    inlines = [SentenceInline]

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Category)
admin.site.register(Sentence)
admin.site.register(Article, ArticleAdmin)

