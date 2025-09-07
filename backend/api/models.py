from django.db import models
import uuid

# Create your models here.
class Campaign(models.Model):
    """
    Campaign model for tracking marketing campaigns.
    
    This model stores information about marketing campaigns including their budget,
    actual spend, and current status. It uses UUID as primary key for better security
    and distribution in database systems.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Campaign name")
    budget = models.DecimalField(max_digits=12, decimal_places=2, 
                               help_text="Total budget allocated for the campaign")
    spend = models.DecimalField(max_digits=12, decimal_places=2,
                              help_text="Current amount spent on the campaign")
    status = models.CharField(
        max_length=10,
        choices=[
            ('active', 'Active'),
            ('paused', 'Paused'),
            ('completed', 'Completed')
        ],
        default='active',
        help_text="Current status of the campaign"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the campaign was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the campaign was last updated")
    
    def __str__(self):
        return self.name
        
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
