from django import forms
from django.forms import (formset_factory, BaseInlineFormSet)
from .models import Tag
import re


class BaseTagFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            tag = form.cleaned_data.get('tag')

            if not tag:
                raise forms.ValidationError('Create a tag')

            if len(tag.tag) < 2:
                raise forms.ValidationError('The tag is too short')

            if re.match('[-\w ]+', tag.tag):
                raise forms.ValidationError('Tag may contain only letters')
