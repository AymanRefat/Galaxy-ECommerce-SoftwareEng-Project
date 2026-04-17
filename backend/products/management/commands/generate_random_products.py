import requests
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from products.models import Product, Category, ProductImage
from vendors.models import VendorProfile


User = get_user_model()

# Data from frontend/lib/mockProducts.ts for alignment
PRODUCT_DATA = [
    {
        'title': 'Wireless Noise-Cancelling Headphones',
        'price': 299.99,
        'category': 'Electronics',
        'slug': 'electronics',
        'imageUrl': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
    },
    {
        'title': 'Smart Fitness Watch Series 7',
        'price': 199.50,
        'category': 'Electronics',
        'slug': 'electronics',
        'imageUrl': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
    },
    {
        'title': 'Minimalist Leather Wallet',
        'price': 45.00,
        'category': 'Accessories',
        'slug': 'accessories',
        'imageUrl': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&q=80',
    },
    {
        'title': 'Ergonomic Office Chair',
        'price': 189.99,
        'category': 'Furniture',
        'slug': 'furniture',
        'imageUrl': 'https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=800&q=80',
    },
    {
        'title': 'Ceramic Coffee Mug - 16oz',
        'price': 18.50,
        'category': 'Home-Goods',
        'slug': 'home-goods',
        'imageUrl': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800&q=80',
    }
]

class Command(BaseCommand):
    help = 'Generates products matching the UI mockup data'

    def handle(self, *args, **kwargs):
        # 1. Create Superuser admin:admin
        admin_user, created = User.objects.get_or_create(
            email='admin@admin.com',
            username='admin',
            defaults={
                'user_type': User.UserType.ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superuser admin created successfully.'))

        # 2. Create a default Vendor
        vendor_user, _ = User.objects.get_or_create(
            email='vendor@example.com',
            username='vendor',
            defaults={'user_type': User.UserType.VENDOR}
        )
        
        vendor_profile, _ = VendorProfile.objects.get_or_create(
            user=vendor_user,
            defaults={
                'store_name': 'Galaxy Featured Store',
                'description': 'The official store for premium Galaxy products.',
                'is_approved': True
            }
        )

        # 3. Create Products and Download Images
        self.stdout.write('Starting data generation and image downloads...')
        
        for data in PRODUCT_DATA:
            # Create Category
            category, _ = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['category']}
            )

            # Create Product
            sku = f"GALAXY-{data['slug'].upper()}-{data['title'][:3].upper()}"
            product, created = Product.objects.get_or_create(
                name=data['title'],
                category=category,
                defaults={
                    'vendor': vendor_profile,
                    'description': f"Premium quality {data['title']} for the modern lifestyle.",
                    'price': data['price'],
                    'stock_quantity': 50,
                    'sku': sku
                }
            )

            if created:
                image_name = f"{data['slug']}.jpg"
                cache_dir = Path(settings.BASE_DIR) / 'seed_images'
                cache_dir.mkdir(exist_ok=True)
                cache_path = cache_dir / image_name
                
                image_content = None
                
                # Check if image is cached locally
                if cache_path.exists():
                    self.stdout.write(f'Using cached image for: {product.name}')
                    with open(cache_path, 'rb') as f:
                        image_content = f.read()
                else:
                    self.stdout.write(f'Downloading image for: {product.name}...')
                    try:
                        response = requests.get(data['imageUrl'], timeout=10)
                        if response.status_code == 200:
                            image_content = response.content
                            # Save to cache
                            with open(cache_path, 'wb') as f:
                                f.write(image_content)
                            self.stdout.write(self.style.SUCCESS(f'Downloaded and cached image for {product.name}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Failed to download image: {e}'))

                if image_content:
                    try:
                        product_image = ProductImage(
                            product=product,
                            is_primary=True
                        )
                        product_image.image.save(image_name, ContentFile(image_content), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Successfully assigned image to {product.name}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Failed to save image to model: {e}'))
            else:
                self.stdout.write(f'Product {product.name} already exists.')


        self.stdout.write(self.style.SUCCESS('Successfully synchronized backend data with UI mockup.'))
