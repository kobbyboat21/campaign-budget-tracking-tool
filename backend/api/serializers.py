from rest_framework import serializers
from .models import Campaign
from decimal import Decimal

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'budget', 'spend', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def _validate_non_negative(self, value, field_name):
        """
        Helper method to validate that a value is not negative
        """
        if value < Decimal('0'):
            raise serializers.ValidationError(f"{field_name.capitalize()} cannot be negative")
        return value
        
    def validate_budget(self, value):
        """
        Check that budget is not negative
        """
        return self._validate_non_negative(value, "budget")
        
    def validate_spend(self, value):
        """
        Check that spend is not negative
        """
        return self._validate_non_negative(value, "spend")
