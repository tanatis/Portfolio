from django import forms

from portfolio.position.models import Position


class CreatePositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price', 'to_portfolio')


class AddToPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price',)
