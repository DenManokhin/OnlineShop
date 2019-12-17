from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=255)
    last_name = forms.CharField(label='Last name', max_length=255)
    email = forms.EmailField()
    address = forms.CharField(label='Address', max_length=255, help_text='Country, City, Street, Building, Flat, ZIP')
    card_name = forms.CharField(label='Name on card', max_length=22, help_text='Full name as displayed on card')
    card_number = forms.CharField(label='Credit card number', min_length=19, max_length=19)
    card_expiration = forms.DateTimeField(label='Expiration', input_formats=['%m/%y'])
    card_cvv = forms.CharField(label='CVV', min_length=3, max_length=3, widget=forms.PasswordInput)


class ReviewForm(forms.Form):
    message = forms.CharField(max_length=14000, widget=forms.Textarea)
    rating = forms.IntegerField(label="Rating", min_value=1, max_value=5)

