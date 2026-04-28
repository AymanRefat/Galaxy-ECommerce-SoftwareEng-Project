from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import VendorSubscription

class Command(BaseCommand):
    help = 'Checks active subscriptions and marks them as PAST_DUE or EXPIRED if end_date has passed.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_subs = VendorSubscription.objects.filter(status='ACTIVE', end_date__lt=now)
        count = expired_subs.count()

        for sub in expired_subs:
            sub.status = 'PAST_DUE'
            sub.save()
            self.stdout.write(self.style.WARNING(f"Subscription for {sub.vendor.store_name} marked as PAST_DUE."))

        self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} expired subscriptions."))
