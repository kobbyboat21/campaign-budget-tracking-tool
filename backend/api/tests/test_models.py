from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
import uuid

# We haven't created the model yet, but we're writing tests first (TDD)
# The import will fail until we create the model
from api.models import Campaign

class CampaignModelTest(TestCase):
    def test_campaign_creation(self):
        """Test that a campaign can be created with valid data"""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            budget=Decimal('1000.00'),
            spend=Decimal('500.00'),
            status="active"
        )
        self.assertEqual(campaign.name, "Test Campaign")
        self.assertEqual(campaign.budget, Decimal('1000.00'))
        self.assertEqual(campaign.spend, Decimal('500.00'))
        self.assertEqual(campaign.status, "active")
        self.assertIsInstance(campaign.id, uuid.UUID)
    
    def test_string_representation(self):
        """Test the string representation of a campaign"""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            budget=Decimal('1000.00'),
            spend=Decimal('500.00')
        )
        self.assertEqual(str(campaign), "Test Campaign")
    
    def test_status_choices(self):
        """Test that status must be one of the valid choices"""
        # This should work
        campaign = Campaign.objects.create(
            name="Valid Status",
            budget=Decimal('1000.00'),
            spend=Decimal('500.00'),
            status="paused"
        )
        self.assertEqual(campaign.status, "paused")
        
        # This should fail - we'll test by creating and then validating
        campaign = Campaign(
            name="Invalid Status",
            budget=Decimal('1000.00'),
            spend=Decimal('500.00'),
            status="invalid"
        )
        
        # Django's full_clean() will validate against choices
        with self.assertRaises(ValidationError):
            campaign.full_clean()
            
    def test_decimal_precision(self):
        """Test that decimal fields have the correct precision"""
        campaign = Campaign.objects.create(
            name="Decimal Test",
            budget=Decimal('1234567890.12'),  # Test with 12 digits (10+2)
            spend=Decimal('0.05')
        )
        # Retrieve from DB to ensure precision is maintained
        retrieved = Campaign.objects.get(name="Decimal Test")
        self.assertEqual(retrieved.budget, Decimal('1234567890.12'))
        self.assertEqual(retrieved.spend, Decimal('0.05'))
