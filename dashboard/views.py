from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from shop.models import Product, Category
from orders.models import Order
from django.contrib.auth.models import User
from .forms import ProductForm, CategoryForm


@staff_member_required
def dashboard_home(request):
    """Page d'accueil du dashboard"""
    # Statistiques
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_revenue = Order.objects.filter(status__in=['paid', 'processing', 'shipped', 'delivered']).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=10, available=True).count()
    
    # Dernières commandes
    recent_orders = Order.objects.all()[:10]
    
    # Produits les plus vendus (approximation)
    popular_products = Product.objects.filter(available=True)[:5]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'popular_products': popular_products,
    }
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def product_list(request):
    """Liste des produits"""
    products = Product.objects.all()
    
    # Recherche
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    context = {'products': products, 'query': query}
    return render(request, 'dashboard/product_list.html', context)


@staff_member_required
def product_create(request):
    """Créer un nouveau produit"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit créé avec succès!')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Créer'})


@staff_member_required
def product_edit(request, pk):
    """Modifier un produit"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès!')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'product': product,
        'action': 'Modifier'
    })


@staff_member_required
def product_delete(request, pk):
    """Supprimer un produit"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produit supprimé avec succès!')
        return redirect('dashboard:product_list')
    
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})


@staff_member_required
def category_list(request):
    """Liste des catégories"""
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})


@staff_member_required
def category_create(request):
    """Créer une nouvelle catégorie"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/category_form.html', {'form': form, 'action': 'Créer'})


@staff_member_required
def category_edit(request, pk):
    """Modifier une catégorie"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie modifiée avec succès!')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'dashboard/category_form.html', {
        'form': form,
        'category': category,
        'action': 'Modifier'
    })


@staff_member_required
def category_delete(request, pk):
    """Supprimer une catégorie"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Catégorie supprimée avec succès!')
        return redirect('dashboard:category_list')
    
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})


@staff_member_required
def order_list(request):
    """Liste des commandes"""
    orders = Order.objects.all()
    
    # Filtre par statut
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'dashboard/order_list.html', context)


@staff_member_required
def order_detail(request, order_number):
    """Détail d'une commande"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            if new_status == 'paid' and not order.paid_at:
                order.paid_at = timezone.now()
            order.save()
            messages.success(request, 'Statut de la commande mis à jour!')
            return redirect('dashboard:order_detail', order_number=order_number)
    
    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    })


@staff_member_required
def user_list(request):
    """Liste des utilisateurs"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})
