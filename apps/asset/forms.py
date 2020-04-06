from django import forms
from asset.models import *


class DomainForms(forms.ModelForm):
    class Meta:
        model = DomainList
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DomainForms, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = 'form-control'

