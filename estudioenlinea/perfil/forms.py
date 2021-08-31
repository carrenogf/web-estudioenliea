from django import forms
from emitidos.models import Contribuyente


class ContribuyenteModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Razon_Social

class resumen_form(forms.Form):
    contribuyente = ContribuyenteModelChoiceField(queryset=Contribuyente.objects.all())

    def __init__(self, *args, **kwargs):
        super(resumen_form, self).__init__(*args, **kwargs)
        self.fields['contribuyente'].widget.attrs.update({'class': 'form-control'})