import floppyforms.__future__ as forms

from patients.models import Measurement


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('value', 'date')
        widgets = {
            'value':forms.RangeInput,
            'date': forms.DateInput,
        }