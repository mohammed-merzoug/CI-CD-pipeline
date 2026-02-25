from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Profil utilisateur étendu"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'

    def __str__(self):
        return f"Profil de {self.user.username}"


class Address(models.Model):
    """Adresse de livraison/facturation"""
    ADDRESS_TYPES = (
        ('shipping', 'Livraison'),
        ('billing', 'Facturation'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, verbose_name="Type d'adresse")
    full_name = models.CharField(max_length=200, verbose_name="Nom complet")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    address_line1 = models.CharField(max_length=250, verbose_name="Adresse ligne 1")
    address_line2 = models.CharField(max_length=250, blank=True, verbose_name="Adresse ligne 2")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=20, verbose_name="Code postal")
    country = models.CharField(max_length=100, default='France', verbose_name="Pays")
    is_default = models.BooleanField(default=False, verbose_name="Adresse par défaut")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.city}"

    def save(self, *args, **kwargs):
        # Si cette adresse est définie comme par défaut, retirer le statut des autres
        if self.is_default:
            Address.objects.filter(
                user=self.user,
                address_type=self.address_type,
                is_default=True
            ).update(is_default=False)
        super().save(*args, **kwargs)
