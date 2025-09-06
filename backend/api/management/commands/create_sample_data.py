from django.core.management.base import BaseCommand
from api.models import Campaign
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates sample campaign data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of campaigns to create')

    def handle(self, *args, **options):
        count = options['count']
        
        # Campaign name prefixes and suffixes for generating random names
        prefixes = ['Summer', 'Winter', 'Spring', 'Fall', 'Holiday', 'Black Friday', 
                   'Cyber Monday', 'Back to School', 'New Year', 'Valentine\'s Day']
        suffixes = ['Sale', 'Promotion', 'Campaign', 'Special', 'Discount', 'Event', 
                   'Launch', 'Offer', 'Deal', 'Giveaway']
        
        # Status options with weights to make active more common
        statuses = ['active', 'active', 'active', 'paused', 'paused', 'completed']
        
        # Delete existing campaigns if any
        existing_count = Campaign.objects.count()
        if existing_count > 0:
            self.stdout.write(f'Deleting {existing_count} existing campaigns...')
            Campaign.objects.all().delete()
        
        # Create new campaigns
        self.stdout.write(f'Creating {count} sample campaigns...')
        
        for i in range(count):
            # Generate random name
            name = f"{random.choice(prefixes)} {random.choice(suffixes)} {i+1}"
            
            # Generate random budget between 1000 and 10000
            budget = Decimal(random.randint(1000, 10000))
            
            # Generate random spend between 0 and budget
            spend = Decimal(random.randint(0, int(budget)))
            
            # Pick random status
            status = random.choice(statuses)
            
            # Create campaign with slightly randomized creation date (within last 30 days)
            days_ago = random.randint(0, 30)
            created_date = timezone.now() - timedelta(days=days_ago)
            
            campaign = Campaign.objects.create(
                name=name,
                budget=budget,
                spend=spend,
                status=status
            )
            
            # Manually update created_at for more realistic data
            # Note: This bypasses auto_now_add but is useful for sample data
            Campaign.objects.filter(id=campaign.id).update(created_at=created_date)
            
            self.stdout.write(f'Created campaign: {name} (${budget} budget, ${spend} spend, {status})')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} sample campaigns'))
