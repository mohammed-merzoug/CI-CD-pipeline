from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    """Panier d'achat"""

    def __init__(self, request):
        """Initialiser le panier"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Créer un nouveau panier dans la session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Ajouter un produit au panier ou mettre à jour sa quantité"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Marquer la session comme modifiée"""
        self.session.modified = True

    def remove(self, product):
        """Retirer un produit du panier"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Itérer sur les articles du panier et récupérer les produits depuis la base de données"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Compter tous les articles dans le panier"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculer le coût total du panier"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Vider le panier"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
