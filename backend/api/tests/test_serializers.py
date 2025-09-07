from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from decimal import Decimal
import uuid
from api.models import Campaign
from api.serializers import CampaignSerializer

class CampaignSerializerTest(TestCase):
    def setUp(self):
        self.campaign_data = {
            'name': 'Test Campaign',
            'budget': '1000.00',
            'spend': '500.00',
            'status': 'active'
        }
        self.campaign = Campaign.objects.create(
            name='Existing Campaign',
            budget=Decimal('2000.00'),
            spend=Decimal('1000.00'),
            status='paused'
        )
        
    def test_serializer_with_valid_data(self):
        """Test serializer with valid data"""
        serializer = CampaignSerializer(data=self.campaign_data)
        self.assertTrue(serializer.is_valid())
        campaign = serializer.save()
        self.assertEqual(campaign.name, 'Test Campaign')
        self.assertEqual(campaign.budget, Decimal('1000.00'))
        self.assertEqual(campaign.spend, Decimal('500.00'))
        self.assertEqual(campaign.status, 'active')
        self.assertIsInstance(campaign.id, uuid.UUID)
        
    def test_serializer_with_invalid_status(self):
        """Test serializer with invalid status"""
        invalid_data = self.campaign_data.copy()
        invalid_data['status'] = 'invalid'
        serializer = CampaignSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)
        
    def test_serializer_with_negative_budget(self):
        """Test serializer with negative budget"""
        invalid_data = self.campaign_data.copy()
        invalid_data['budget'] = '-1000.00'
        serializer = CampaignSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('budget', serializer.errors)
        
    def test_serializer_with_negative_spend(self):
        """Test serializer with negative spend"""
        invalid_data = self.campaign_data.copy()
        invalid_data['spend'] = '-500.00'
        serializer = CampaignSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('spend', serializer.errors)
        
    def test_serializer_read(self):
        """Test serializer read functionality"""
        serializer = CampaignSerializer(self.campaign)
        data = serializer.data
        self.assertEqual(data['name'], 'Existing Campaign')
        self.assertEqual(data['budget'], '2000.00')
        self.assertEqual(data['spend'], '1000.00')
        self.assertEqual(data['status'], 'paused')
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
