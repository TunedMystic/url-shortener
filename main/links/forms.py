from django import forms

from .models import Link


class LinkForm(forms.ModelForm):
    destination = forms.URLField(widget=forms.TextInput)

    def clean(self, *args, **kwargs):
        cleaned_data = super(LinkForm, self).clean(*args, **kwargs)
        return cleaned_data

    class Meta:
        model = Link
        fields = ['destination']
