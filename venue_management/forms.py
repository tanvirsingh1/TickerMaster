from django import forms

class PromoCodeForm(forms.Form):
    name = forms.CharField(label='Your Name')
