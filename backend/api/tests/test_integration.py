from django.test import TestCase
from rest_framework.test import APIClient
from decimal import Decimal
from api.models import Campaign
import json

class FrontendIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            budget=Decimal('1000.00'),
            spend=Decimal('500.00'),
            status='active'
        )
        
    def test_cors_headers(self):
        """Test that CORS headers are present in the response"""
        response = self.client.get('/api/campaigns/', HTTP_ORIGIN='http://localhost:3000')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', response)
        
    def test_json_format(self):
        """Test that the API returns properly formatted JSON"""
        response = self.client.get(f'/api/campaigns/{self.campaign.id}/')
        self.assertEqual(response.status_code, 200)
        
        # Check that the response can be parsed as JSON
        try:
            data = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")
            
        # Check that the JSON structure matches our expectations
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('budget', data)
        self.assertIn('spend', data)
        self.assertIn('status', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        
        # Check data types
        self.assertEqual(data['name'], 'Test Campaign')
        self.assertEqual(data['budget'], '1000.00')
        self.assertEqual(data['spend'], '500.00')
        self.assertEqual(data['status'], 'active')
        
    def test_frontend_filters(self):
        """Test that the API supports filtering as needed by the frontend"""
        # Create additional campaigns with different statuses
        Campaign.objects.create(
            name='Paused Campaign',
            budget=Decimal('2000.00'),
            spend=Decimal('1000.00'),
            status='paused'
        )
        Campaign.objects.create(
            name='Completed Campaign',
            budget=Decimal('3000.00'),
            spend=Decimal('3000.00'),
            status='completed'
        )
        
        # Test filtering by status
        response = self.client.get('/api/campaigns/?status=active')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['name'], 'Test Campaign')
        
        # Test search by name
        response = self.client.get('/api/campaigns/?search=Paused')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['name'], 'Paused Campaign')
        
        # Test ordering
        response = self.client.get('/api/campaigns/?ordering=budget')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 3)
        self.assertEqual(data['results'][0]['name'], 'Test Campaign')
        self.assertEqual(data['results'][1]['name'], 'Paused Campaign')
        self.assertEqual(data['results'][2]['name'], 'Completed Campaign')
