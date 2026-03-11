from django.core.management.base import BaseCommand
from shop.models import Product
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Link product images to products based on filename matching'

    def handle(self, *args, **kwargs):
        self.stdout.write('Linking product images...')
        
        # Path to products images
        media_root = Path('media/products')
        
        if not media_root.exists():
            self.stdout.write(self.style.ERROR('media/products directory not found!'))
            return
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(media_root.glob(f'*{ext}'))
        
        self.stdout.write(f'Found {len(image_files)} images')
        
        linked_count = 0
        not_found_count = 0
        
        for image_path in image_files:
            # Get filename without extension
            product_name = image_path.stem
            
            # Try to find matching product
            try:
                product = Product.objects.get(name__iexact=product_name)
                
                # Update product image path (relative to MEDIA_ROOT)
                relative_path = f'products/{image_path.name}'
                product.image = relative_path
                product.save()
                
                self.stdout.write(f'  ✓ Linked: {product.name} -> {image_path.name}')
                linked_count += 1
                
            except Product.DoesNotExist:
                self.stdout.write(f'  ✗ No product found for: {product_name}')
                not_found_count += 1
            except Product.MultipleObjectsReturned:
                self.stdout.write(f'  ⚠ Multiple products found for: {product_name}')
                not_found_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Finished!'))
        self.stdout.write(self.style.SUCCESS(f'   Linked: {linked_count} products'))
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(f'   Not matched: {not_found_count} images'))
