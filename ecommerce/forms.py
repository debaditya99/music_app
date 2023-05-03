from django import forms

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

COUNTRY_CHOICES = (
    ('IN','India'),
    ('NP','Nepal')
)

STATE_CHOICES = (
    ('DL','Delhi'),
    ('HR','Haryana'),
    ('PB','Punjab'),
    ('UP','Uttar Pradesh'),
    ('LK','Lucknow'),
    ('BH','Bihar'),
    ('BN','Bangalore'),
    ('MH','Maharastra')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address.widget.attrs.update({'class':'form-control'})
    shipping_address2 = forms.CharField(required=False)
    shipping_country = forms.ChoiceField(required=False,choices=COUNTRY_CHOICES, label='(select country)')
    shipping_country.widget.attrs.update({'class':'form-control'})
    shipping_state = forms.ChoiceField(choices=STATE_CHOICES, label='(select state)')
    shipping_state.widget.attrs.update({'class':'form-control'})
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = forms.ChoiceField(choices = COUNTRY_CHOICES,label='(select country)',required=False)
    billing_country.widget.attrs.update({'class': 'form-control'})
    billing_state = forms.ChoiceField(choices=STATE_CHOICES, label='(select state)',required=False)
    billing_state.widget.attrs.update({'class': 'form-control'})
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField() 


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)