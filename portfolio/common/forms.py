from django import forms


class SearchTickerForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search stocks ...',
                'class': '',
            }
        )
    )