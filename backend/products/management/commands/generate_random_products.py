import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product, Category
from vendors.models import VendorProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates random products and a super user'

    def handle(self, *args, **kwargs):
        # Create Superuser admin:admin
        try:
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
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))

        # Create a Vendor for products
        vendor_user, created = User.objects.get_or_create(
            email='vendor@example.com',
            username='vendor',
            defaults={
                'user_type': User.UserType.VENDOR,
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created:
            vendor_user.set_password('vendor')
            vendor_user.save()
        
        vendor_profile, created = VendorProfile.objects.get_or_create(
            user=vendor_user,
            defaults={
                'store_name': 'Random Vendor Store',
                'description': 'A store for random products.',
                'is_approved': True
            }
        )

        # Create Category
        category, created = Category.objects.get_or_create(
            name='Random Category',
            slug='random-category'
        )

        # Generate Random Products
        products_to_create = 10
        self.stdout.write(f'Generating {products_to_create} random products...')
        
        # Use get_or_create logic to ensure idempotency as requested.
        for i in range(products_to_create):
            # Using a fixed set of SKUs to allow get_or_create to work idempotently
            sku = f"RAND-PROD-{i+1:03d}"
            product, p_created = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'vendor': vendor_profile,
                    'category': category,
                    'name': f'Random Product {i+1}',
                    'description': f'This is randomly generated product number {i+1}.',
                    'price': round(random.uniform(10.0, 500.0), 2),
                    'stock_quantity': random.randint(1, 100),
                }
            )
            if p_created:
                self.stdout.write(self.style.SUCCESS(f'Created Product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product {product.name} already exists.'))

        self.stdout.write(self.style.SUCCESS('Successfully completed dummy data generation.'))
