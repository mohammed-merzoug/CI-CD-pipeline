from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
import uuid


class Order(models.Model):
    """Commande"""
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('paid', 'Payée'),
        ('processing', 'En préparation'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    )

    order_number = models.CharField(max_length=100, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Client")
    
    # Informations de livraison
    shipping_full_name = models.CharField(max_length=200, verbose_name="Nom complet")
    shipping_phone = models.CharField(max_length=20, verbose_name="Téléphone")
    shipping_address_line1 = models.CharField(max_length=250, verbose_name="Adresse ligne 1")
    shipping_address_line2 = models.CharField(max_length=250, blank=True, verbose_name="Adresse ligne 2")
    shipping_city = models.CharField(max_length=100, verbose_name="Ville")
    shipping_postal_code = models.CharField(max_length=20, verbose_name="Code postal")
    shipping_country = models.CharField(max_length=100, default='France', verbose_name="Pays")
    
    # Informations de commande
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de paiement")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return f"Commande {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Générer un numéro de commande unique"""
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"

    def get_total_cost(self):
        """Calculer le coût total de la commande"""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Article de commande"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")

    class Meta:
        verbose_name = 'Article de commande'
        verbose_name_plural = 'Articles de commande'

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_cost(self):
        """Calculer le coût total de cet article"""
        return self.price * self.quantity
