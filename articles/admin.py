from django.contrib import admin
from .models import (Article, Subscription)
from .forms import ArticleForm
from tag.models import Tag
from tag.forms import BaseTagFormSet


class TagInline(admin.StackedInline):
    model = Tag.article.through
    formset = BaseTagFormSet
    extra = 0


class ArticleExtension(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'edited', 'get_hits'
                    )

    inlines = [TagInline]

    form = ArticleForm

    def get_form(self, request, *args, **kwargs):
        """
        set an author by default
        """
        form = super().get_form(request, *args, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


admin.site.register(Article, ArticleExtension)
admin.site.register(Subscription)
