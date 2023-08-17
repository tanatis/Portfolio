from django import forms

from portfolio.position.models import Position


class AddPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'
