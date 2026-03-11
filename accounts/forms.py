from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Address


class UserRegistrationForm(forms.ModelForm):
    """Formulaire d'inscription"""
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet email est déjà utilisé.')
        return email


class UserProfileForm(forms.ModelForm):
    """Formulaire de profil utilisateur"""
    first_name = forms.CharField(max_length=150, required=False, label='Prénom')
    last_name = forms.CharField(max_length=150, required=False, label='Nom')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = UserProfile
        fields = ['phone', 'birth_date']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email


class AddressForm(forms.ModelForm):
    """Formulaire d'adresse"""
    class Meta:
        model = Address
        fields = [
            'address_type', 'full_name', 'phone',
            'address_line1', 'address_line2',
            'city', 'postal_code', 'country', 'is_default'
        ]
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
