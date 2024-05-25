from django import forms


class AddFundsForm(forms.Form):
    amount = forms.DecimalField(required=True)
    card_name = forms.CharField(required=False)
    card_number = forms.CharField(required=False)
    card_exp_date = forms.CharField(required=False)
    card_cvv_number = forms.CharField(required=False)
    card_address1 = forms.CharField(required=False)
    card_address2 = forms.CharField(required=False)
    card_city = forms.CharField(required=False)
    card_state = forms.CharField(required=False)
    card_zipcode = forms.CharField(required=False)
    card_country = forms.CharField(required=False)
