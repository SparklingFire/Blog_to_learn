from django.contrib import admin
from .models import Comment


class CommentExtension(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Comment, CommentExtension)
