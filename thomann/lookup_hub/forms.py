from django import forms
# from django.forms.models import inlineformset_factory

from . import models



class RowForm(forms.ModelForm):
    class Meta:
        model = models.Row

        fields = (
            'category',
        )


class CellForm(forms.ModelForm):
    class Meta:
        model = models.Cell
        fields = (
            'language',
            'text',
            'comment',
            'colour',
            'row',
        )
