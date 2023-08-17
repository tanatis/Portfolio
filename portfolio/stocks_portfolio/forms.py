from django import forms

from portfolio.stocks_portfolio.models import Portfolio


class AddPortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'cash')
