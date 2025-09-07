from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
import uuid
import json
from api.models import Campaign

class CampaignViewSetTest(APITestCase):
    def setUp(self):
        self.campaign1 = Campaign.objects.create(
            name='Campaign 1',
            budget=Decimal('1000.00'),
            spend=Decimal('500.00'),
            status='active'
        )
        self.campaign2 = Campaign.objects.create(
            name='Campaign 2',
            budget=Decimal('2000.00'),
            spend=Decimal('1000.00'),
            status='paused'
        )
        self.valid_payload = {
            'name': 'New Campaign',
            'budget': '3000.00',
            'spend': '1500.00',
            'status': 'active'
        }
        self.invalid_payload = {
            'name': 'Invalid Campaign',
            'budget': '-1000.00',  # Negative budget should fail validation
            'spend': '500.00',
            'status': 'active'
        }
        
    def test_get_all_campaigns(self):
        """Test retrieving all campaigns"""
        url = reverse('campaign-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_get_single_campaign(self):
        """Test retrieving a single campaign"""
        url = reverse('campaign-detail', args=[str(self.campaign1.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Campaign 1')
        
    def test_create_valid_campaign(self):
        """Test creating a new campaign with valid data"""
        url = reverse('campaign-list')
        response = self.client.post(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 3)
        self.assertEqual(Campaign.objects.latest('created_at').name, 'New Campaign')
        
    def test_create_invalid_campaign(self):
        """Test creating a new campaign with invalid data"""
        url = reverse('campaign-list')
        response = self.client.post(
            url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Campaign.objects.count(), 2)
        
    def test_update_campaign(self):
        """Test updating an existing campaign"""
        url = reverse('campaign-detail', args=[str(self.campaign1.id)])
        update_data = {
            'name': 'Updated Campaign',
            'budget': '1500.00',
            'spend': '750.00',
            'status': 'paused'
        }
        response = self.client.put(
            url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.campaign1.refresh_from_db()
        self.assertEqual(self.campaign1.name, 'Updated Campaign')
        self.assertEqual(self.campaign1.status, 'paused')
        
    def test_delete_campaign(self):
        """Test deleting a campaign"""
        url = reverse('campaign-detail', args=[str(self.campaign1.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Campaign.objects.count(), 1)
        
    def test_filter_by_status(self):
        """Test filtering campaigns by status"""
        url = reverse('campaign-list') + '?status=active'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Campaign 1')
