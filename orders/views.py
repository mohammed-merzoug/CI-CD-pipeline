from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from cart.cart import Cart
from accounts.models import Address
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    """Créer une nouvelle commande (checkout)"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Votre panier est vide!')
        return redirect('cart:cart_detail')
    
    # Récupérer les adresses de l'utilisateur
    shipping_addresses = Address.objects.filter(
        user=request.user,
        address_type='shipping'
    )
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Récupérer l'adresse sélectionnée
            address_id = request.POST.get('shipping_address')
            if address_id:
                address = get_object_or_404(Address, id=address_id, user=request.user)
                
                # Créer la commande
                order = Order.objects.create(
                    user=request.user,
                    shipping_full_name=address.full_name,
                    shipping_phone=address.phone,
                    shipping_address_line1=address.address_line1,
                    shipping_address_line2=address.address_line2,
                    shipping_city=address.city,
                    shipping_postal_code=address.postal_code,
                    shipping_country=address.country,
                    total_amount=cart.get_total_price(),
                    notes=form.cleaned_data.get('notes', '')
                )
                
                # Créer les articles de commande
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                
                # Vider le panier
                cart.clear()
                
                # Simuler le paiement (dans un vrai projet, intégrer Stripe, PayPal, etc.)
                order.status = 'paid'
                order.paid_at = timezone.now()
                order.save()
                
                messages.success(request, f'Commande {order.order_number} créée avec succès!')
                return redirect('orders:order_detail', order_number=order.order_number)
            else:
                messages.error(request, 'Veuillez sélectionner une adresse de livraison.')
    else:
        form = OrderCreateForm()
    
    context = {
        'cart': cart,
        'form': form,
        'shipping_addresses': shipping_addresses,
    }
    return render(request, 'orders/order_create.html', context)


@login_required
def order_detail(request, order_number):
    """Détail d'une commande"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    """Liste des commandes de l'utilisateur"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
