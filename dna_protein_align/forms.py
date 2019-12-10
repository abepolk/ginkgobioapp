from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class IndexForm(forms.Form):
    seq = forms.CharField(max_length=255)
    remove_search_history = forms.BooleanField(required=False)

    # It looks ilke this is called by is_valid() or somethign
    def clean_seq(self):
        data = self.cleaned_data['seq']
        # This is just my guess on how to validate a DNA sequence
        for bp in data:
            if bp not in ['A', 'C', 'G', 'T']:
                # The validation error is repeated in main.js, because Python exceptions are currently
                # not propagated to the browser
                raise ValidationError(_('Only A, C, G, and T allowed in sequence'))

        return data

    def clean_remove_search_history(self):
        return self.cleaned_data['remove_search_history']