from django.contrib import admin
from .models import Campaign

# Register your models here.
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'spend', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at')
