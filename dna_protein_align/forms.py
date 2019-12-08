from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class IndexForm(forms.Form):
    seq = forms.CharField(max_length=255)
    remove_search_history = forms.BooleanField(required=False)

    def clean_seq(self):
        data = self.cleaned_data['seq']

        # This is just my guess on how to validate a DNA sequence
        for bp in data:
            if bp not in ['A', 'C', 'G', 'T']:
                raise ValidationError(_('Only A, C, G, and T allowed in sequence'))

        return data

    def clean_remove_search_history(self):
        return self.cleaned_data['remove_search_history']