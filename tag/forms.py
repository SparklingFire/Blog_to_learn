from django import forms
from django.forms import (modelformset_factory, BaseModelFormSet)
from .models import Tag
import re


class BaseTagFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        tags = []
        for form in self.forms:
            tag = form.cleaned_data.get('tag')
            if tag in tags:
                raise forms.ValidationError('Тэг введен повторно')

            tags.append(tag)

            if not tag:
                raise forms.ValidationError('Create a tag')

            if len(tag) < 2:
                raise forms.ValidationError('The tag is too short')


TagFormSet = modelformset_factory(Tag, fields=('tag',), formset=BaseTagFormSet)
