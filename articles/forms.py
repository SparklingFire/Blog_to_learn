from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text', 'author')

    def __init__(self, *args, **kwargs):
        try:
            self.article = kwargs.pop('article')
        except KeyError:
            pass
        super().__init__(*args, **kwargs)


class SearchForm(forms.Form):
    search_form = forms.CharField(help_text=None, label=None)
