from django import forms
from .models import Contribuyente


class ContribuyenteModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Razon_Social

class MisComprobantesRecibidos_Form(forms.Form):
    contribuyente = ContribuyenteModelChoiceField(queryset=Contribuyente.objects.all())
    file = forms.FileField(label="Excel Mis Comprobantes Recibidos")

    def __init__(self, *args, **kwargs):
        super(MisComprobantesRecibidos_Form, self).__init__(*args, **kwargs)
        self.fields['contribuyente'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
