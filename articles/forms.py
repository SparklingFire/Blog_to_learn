from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text', 'author')
        widgets = {'author': forms.HiddenInput}


class SearchForm(forms.Form):
    search_form = forms.CharField(help_text=None, label=None)
