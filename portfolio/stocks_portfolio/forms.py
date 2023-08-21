from django import forms

from portfolio.stocks_portfolio.models import Portfolio, CashTransaction


class AddPortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'cash')


class DeletePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance


class CashTransactionForm(forms.ModelForm):
    class Meta:
        model = CashTransaction
        fields = ('operation', 'amount')
