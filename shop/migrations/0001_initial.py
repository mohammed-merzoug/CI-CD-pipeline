# Generated migration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nom')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Image principale')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('available', models.BooleanField(default=True, verbose_name='Disponible')),
                ('featured', models.BooleanField(default=False, verbose_name='Produit mis en avant')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='Catégorie')),
            ],
            options={
                'verbose_name': 'Produit',
                'verbose_name_plural': 'Produits',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/gallery/')),
                ('alt_text', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
            options={
                'verbose_name': 'Image produit',
                'verbose_name_plural': 'Images produits',
            },
        ),
    ]
