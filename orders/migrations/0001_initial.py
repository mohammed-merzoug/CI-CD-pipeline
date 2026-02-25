# Generated migration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=100, unique=True)),
                ('shipping_full_name', models.CharField(max_length=200, verbose_name='Nom complet')),
                ('shipping_phone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('shipping_address_line1', models.CharField(max_length=250, verbose_name='Adresse ligne 1')),
                ('shipping_address_line2', models.CharField(blank=True, max_length=250, verbose_name='Adresse ligne 2')),
                ('shipping_city', models.CharField(max_length=100, verbose_name='Ville')),
                ('shipping_postal_code', models.CharField(max_length=20, verbose_name='Code postal')),
                ('shipping_country', models.CharField(default='France', max_length=100, verbose_name='Pays')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Montant total')),
                ('status', models.CharField(choices=[('pending', 'En attente'), ('paid', 'Payée'), ('processing', 'En préparation'), ('shipped', 'Expédiée'), ('delivered', 'Livrée'), ('cancelled', 'Annulée')], default='pending', max_length=20, verbose_name='Statut')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='Date de paiement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Commande',
                'verbose_name_plural': 'Commandes',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix unitaire')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantité')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Produit')),
            ],
            options={
                'verbose_name': 'Article de commande',
                'verbose_name_plural': 'Articles de commande',
            },
        ),
    ]
