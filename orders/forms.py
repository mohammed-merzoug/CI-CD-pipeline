from django import forms


class OrderCreateForm(forms.Form):
    """Formulaire de création de commande"""
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Instructions de livraison (optionnel)'
        }),
        label='Notes'
    )
