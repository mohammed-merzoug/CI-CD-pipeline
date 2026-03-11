#!/bin/bash
# Entrypoint script for Django E-commerce Application

set -e

echo "Starting Django E-commerce Application..."

# Wait for database to be ready (if using external DB)
echo "Checking database connection..."
python manage.py check --database default || true

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files if needed
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Check if database is populated (count products)
PRODUCT_COUNT=$(python manage.py shell -c "from shop.models import Product; print(Product.objects.count())")

if [ "$PRODUCT_COUNT" -eq 0 ]; then
    echo "Database is empty. Populating with initial data..."
    python manage.py populate_db
    python manage.py link_images
    echo "Database populated successfully with 25 products!"
else
    echo "Database already contains $PRODUCT_COUNT products. Skipping population."
fi

# Create default superuser if it doesn't exist
echo "Checking for admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Default superuser created: admin / admin123')
else:
    print('Admin user already exists')
" || true

# Check if media files exist
if [ ! "$(ls -A /app/media/products 2>/dev/null)" ]; then
    echo "Media folder is empty. Copying product images..."
    mkdir -p /app/media/products
    # Images should already be in the container from COPY . .
    if [ -d "/app/media-seed/products" ]; then
        cp -r /app/media-seed/products/* /app/media/products/
        echo "Product images copied successfully!"
    fi
fi

echo "Initialization complete. Starting Gunicorn..."

# Execute the main command
exec "$@"
