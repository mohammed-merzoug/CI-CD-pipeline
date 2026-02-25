from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate database with sample categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories and products...')

        # Créer des catégories
        categories_data = [
            {
                'name': 'Électronique',
                'description': 'Smartphones, tablettes, ordinateurs et accessoires électroniques'
            },
            {
                'name': 'Vêtements',
                'description': 'Mode homme, femme et enfant'
            },
            {
                'name': 'Maison & Jardin',
                'description': 'Meubles, décoration et équipement pour la maison'
            },
            {
                'name': 'Sports & Loisirs',
                'description': 'Équipements sportifs et articles de loisirs'
            },
            {
                'name': 'Livres',
                'description': 'Livres, ebooks et magazines'
            },
            {
                'name': 'Beauté & Santé',
                'description': 'Produits de beauté, cosmétiques et santé'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'  ✓ Catégorie créée: {category.name}')
            else:
                self.stdout.write(f'  - Catégorie existante: {category.name}')

        # Créer des produits
        products_data = [
            # Électronique
            {
                'category': 'Électronique',
                'name': 'iPhone 15 Pro',
                'description': 'Le dernier smartphone d\'Apple avec puce A17 Pro, appareil photo 48MP et écran Super Retina XDR.',
                'price': 1199.00,
                'stock': 25,
                'featured': True
            },
            {
                'category': 'Électronique',
                'name': 'Samsung Galaxy S24',
                'description': 'Smartphone Android haut de gamme avec écran AMOLED 6.2", processeur Snapdragon 8 Gen 3.',
                'price': 899.00,
                'stock': 30,
                'featured': True
            },
            {
                'category': 'Électronique',
                'name': 'MacBook Air M2',
                'description': 'Ordinateur portable ultra-fin avec puce M2, 8Go RAM, SSD 256Go, écran Retina 13.6".',
                'price': 1299.00,
                'stock': 15,
                'featured': False
            },
            {
                'category': 'Électronique',
                'name': 'AirPods Pro 2',
                'description': 'Écouteurs sans fil avec réduction de bruit active, audio spatial et boîtier de charge MagSafe.',
                'price': 279.00,
                'stock': 50,
                'featured': True
            },
            {
                'category': 'Électronique',
                'name': 'iPad Air',
                'description': 'Tablette 10.9" avec puce M1, compatible Apple Pencil et Magic Keyboard.',
                'price': 699.00,
                'stock': 20,
                'featured': False
            },

            # Vêtements
            {
                'category': 'Vêtements',
                'name': 'T-shirt Classique Blanc',
                'description': 'T-shirt 100% coton, coupe droite, parfait pour toutes occasions.',
                'price': 19.99,
                'stock': 100,
                'featured': False
            },
            {
                'category': 'Vêtements',
                'name': 'Jean Slim Bleu',
                'description': 'Jean slim en denim stretch confortable, coupe moderne.',
                'price': 59.99,
                'stock': 75,
                'featured': False
            },
            {
                'category': 'Vêtements',
                'name': 'Veste en Cuir',
                'description': 'Veste en cuir véritable, style motard, doublure intérieure.',
                'price': 199.99,
                'stock': 20,
                'featured': True
            },
            {
                'category': 'Vêtements',
                'name': 'Robe d\'été Florale',
                'description': 'Robe légère en coton avec imprimé floral, parfaite pour l\'été.',
                'price': 49.99,
                'stock': 45,
                'featured': False
            },
            {
                'category': 'Vêtements',
                'name': 'Sneakers Blanches',
                'description': 'Baskets blanches en cuir synthétique, confortables et stylées.',
                'price': 79.99,
                'stock': 60,
                'featured': True
            },

            # Maison & Jardin
            {
                'category': 'Maison & Jardin',
                'name': 'Canapé 3 Places Gris',
                'description': 'Canapé confortable en tissu gris, design moderne, structure en bois massif.',
                'price': 599.00,
                'stock': 8,
                'featured': True
            },
            {
                'category': 'Maison & Jardin',
                'name': 'Table Basse en Bois',
                'description': 'Table basse rectangulaire en bois de chêne, finition naturelle.',
                'price': 149.00,
                'stock': 15,
                'featured': False
            },
            {
                'category': 'Maison & Jardin',
                'name': 'Lampe de Bureau LED',
                'description': 'Lampe LED réglable avec bras articulé, 3 modes d\'éclairage.',
                'price': 39.99,
                'stock': 40,
                'featured': False
            },
            {
                'category': 'Maison & Jardin',
                'name': 'Set de Jardin 4 Pièces',
                'description': 'Table et 4 chaises en résine tressée, résistant aux intempéries.',
                'price': 399.00,
                'stock': 12,
                'featured': False
            },

            # Sports & Loisirs
            {
                'category': 'Sports & Loisirs',
                'name': 'Vélo VTT 27.5"',
                'description': 'VTT tout terrain avec suspension avant, 21 vitesses Shimano.',
                'price': 449.00,
                'stock': 10,
                'featured': True
            },
            {
                'category': 'Sports & Loisirs',
                'name': 'Tapis de Yoga Premium',
                'description': 'Tapis de yoga antidérapant, épaisseur 6mm, écologique.',
                'price': 34.99,
                'stock': 50,
                'featured': False
            },
            {
                'category': 'Sports & Loisirs',
                'name': 'Haltères Réglables 20kg',
                'description': 'Paire d\'haltères réglables de 2.5kg à 20kg, compact.',
                'price': 89.99,
                'stock': 25,
                'featured': False
            },
            {
                'category': 'Sports & Loisirs',
                'name': 'Ballon de Football',
                'description': 'Ballon officiel taille 5, couture thermocollée.',
                'price': 24.99,
                'stock': 60,
                'featured': False
            },

            # Livres
            {
                'category': 'Livres',
                'name': 'Le Petit Prince',
                'description': 'Classique d\'Antoine de Saint-Exupéry, édition illustrée.',
                'price': 12.99,
                'stock': 100,
                'featured': False
            },
            {
                'category': 'Livres',
                'name': 'Clean Code',
                'description': 'Guide pour développeurs par Robert C. Martin, en français.',
                'price': 39.99,
                'stock': 30,
                'featured': True
            },
            {
                'category': 'Livres',
                'name': 'L\'Art de la Guerre',
                'description': 'Traité de stratégie militaire de Sun Tzu, édition commentée.',
                'price': 15.99,
                'stock': 45,
                'featured': False
            },

            # Beauté & Santé
            {
                'category': 'Beauté & Santé',
                'name': 'Crème Hydratante Bio',
                'description': 'Crème visage hydratante aux extraits naturels, 50ml.',
                'price': 29.99,
                'stock': 70,
                'featured': False
            },
            {
                'category': 'Beauté & Santé',
                'name': 'Parfum Femme Élégance',
                'description': 'Eau de parfum florale et fraîche, flacon 100ml.',
                'price': 59.99,
                'stock': 35,
                'featured': True
            },
            {
                'category': 'Beauté & Santé',
                'name': 'Kit Manucure Professionnel',
                'description': 'Set complet avec lime, ciseaux, coupe-ongles et accessoires.',
                'price': 24.99,
                'stock': 40,
                'featured': False
            },
            {
                'category': 'Beauté & Santé',
                'name': 'Brosse à Cheveux Démêlante',
                'description': 'Brosse avec picots flexibles pour tous types de cheveux.',
                'price': 14.99,
                'stock': 80,
                'featured': False
            },
        ]

        created_count = 0
        for prod_data in products_data:
            category = categories[prod_data['category']]
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'slug': slugify(prod_data['name']),
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'available': True,
                    'featured': prod_data.get('featured', False)
                }
            )
            if created:
                created_count += 1
                status = '✓'
            else:
                status = '-'
            
            self.stdout.write(f'  {status} Produit: {product.name} ({category.name}) - {product.price}€')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Terminé! {created_count} nouveaux produits créés.'))
        self.stdout.write(self.style.SUCCESS(f'📦 Total: {Product.objects.count()} produits dans {Category.objects.count()} catégories'))
