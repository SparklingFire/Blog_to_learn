from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'parent'}),
                             required=False)

    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) == 0:
            raise forms.ValidationError('Вы не ввели текст сообщения')
        return text
