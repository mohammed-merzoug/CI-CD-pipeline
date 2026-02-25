from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Catégorie de produits"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_detail', args=[self.slug])


class Product(models.Model):
    """Produit"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Catégorie")
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image principale")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    available = models.BooleanField(default=True, verbose_name="Disponible")
    featured = models.BooleanField(default=False, verbose_name="Produit mis en avant")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    """Images additionnelles pour un produit"""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Image produit'
        verbose_name_plural = 'Images produits'

    def __str__(self):
        return f"Image pour {self.product.name}"
