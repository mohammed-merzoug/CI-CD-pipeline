from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category


def home(request):
    """Page d'accueil"""
    featured_products = Product.objects.filter(featured=True, available=True)[:8]
    categories = Category.objects.all()[:6]
    recent_products = Product.objects.filter(available=True)[:8]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'recent_products': recent_products,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    """Liste de tous les produits avec filtres et recherche"""
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Recherche
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Filtre par catégorie
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Filtre par prix
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Tri
    sort = request.GET.get('sort', '-created_at')
    if sort in ['price', '-price', 'name', '-created_at']:
        products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    """Détail d'un produit"""
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


def category_detail(request, slug):
    """Produits d'une catégorie spécifique"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    # Tri
    sort = request.GET.get('sort', '-created_at')
    if sort in ['price', '-price', 'name', '-created_at']:
        products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'shop/category_detail.html', context)


def about(request):
    """Page à propos"""
    return render(request, 'shop/about.html')


def contact(request):
    """Page de contact"""
    from .forms import ContactForm
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Traiter le formulaire (envoyer un email, sauvegarder, etc.)
            from django.contrib import messages
            messages.success(request, 'Votre message a été envoyé avec succès!')
            form = ContactForm()
    else:
        form = ContactForm()
    
    return render(request, 'shop/contact.html', {'form': form})


def faq(request):
    """Page FAQ"""
    return render(request, 'shop/faq.html')


def terms(request):
    """Conditions générales de vente"""
    return render(request, 'shop/terms.html')


def privacy(request):
    """Politique de confidentialité"""
    return render(request, 'shop/privacy.html')
