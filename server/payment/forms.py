from django import forms


class AddFundsForm(forms.Form):
    amount = forms.DecimalField(
        required=True,
        label="Amount",
        widget=forms.NumberInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Amount'
        })
    )
    card_name = forms.CharField(
        required=False,
        label="Card Name",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Card Name'
        })
    )
    card_number = forms.CharField(
        required=False,
        label="Card Number",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Card Number'
        })
    )
    card_exp_date = forms.CharField(
        required=False,
        label="Card Expiration Date",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Card Expiration Date (MM/YY)'
        })
    )
    card_cvv_number = forms.CharField(
        required=False,
        label="CVV",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'CVV'
        })
    )
    card_address1 = forms.CharField(
        required=False,
        label="Address Line 1",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Address Line 1'
        })
    )
    card_address2 = forms.CharField(
        required=False,
        label="Address Line 2",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Address Line 2'
        })
    )
    card_city = forms.CharField(
        required=False,
        label="City",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'City'
        })
    )
    card_state = forms.CharField(
        required=False,
        label="State",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'State'
        })
    )
    card_zipcode = forms.CharField(
        required=False,
        label="Zip Code",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Zip Code'
        })
    )
    card_country = forms.CharField(
        required=False,
        label="Country",
        widget=forms.TextInput(attrs={
            'class': 'block w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',  # noqa
            'placeholder': 'Country'
        })
    )
