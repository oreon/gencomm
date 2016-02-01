from django import forms
from patients.models import Measurement


class PostForm(forms.ModelForm):

    class Meta:
        model = Measurement
        fields = ('value', 'date', 'notes')