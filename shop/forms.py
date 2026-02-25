from django import forms


class ContactForm(forms.Form):
    """Formulaire de contact"""
    name = forms.CharField(
        max_length=100,
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=200,
        label='Sujet',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
