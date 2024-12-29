from django import forms
'''
forms:Django validation and HTML form handling.
Form:A collection of Fields
'''
class CustomerLogin(forms.Form):
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':"controls input-xlarge control-group",'placeholder':'Email'}))
    
    password=forms.CharField(label='Password',widget=forms.EmailInput(attrs={'class':"controls input-xlarge control-group",'placeholder':'Password'}))
