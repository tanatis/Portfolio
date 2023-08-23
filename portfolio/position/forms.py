from django import forms

from portfolio.position.models import Position
from portfolio.stocks_portfolio.models import Portfolio


class CreatePositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price', 'to_portfolio')

    user = None  # Add a user field

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove user from kwargs and store it
        super().__init__(*args, **kwargs)

        if user:
            self.user = user
            self.fields['to_portfolio'].queryset = Portfolio.objects.filter(user=user)


class AddToPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price',)


class SellPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price',)
