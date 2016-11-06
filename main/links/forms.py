from django import forms

from .models import Link


class LinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['key'].required = False

    def clean_key(self):
        key = self.cleaned_data.get('key')
        if key and Link.objects.filter(key=key).exists():
            raise forms.ValidationError('Custom link is already taken!')
        return key

    def clean(self, *args, **kwargs):
        cleaned_data = super(LinkForm, self).clean(*args, **kwargs)
        return cleaned_data

    def save(self, commit=True):
        '''
        Overrides LinkForm.save().
        Generates key if key does not exist.
        Sets user if user is authenticated.
        '''
        link = super(LinkForm, self).save(commit=False)

        # Generate random key for Link if key does not exist.
        if not link.key:
            link.key = Link.make_key()

        # Set user if user is authenticated.
        if self.user and self.user.is_authenticated:
            link.user = self.user

        link.save()
        return link

    class Meta:
        model = Link
        fields = ['destination', 'key']
