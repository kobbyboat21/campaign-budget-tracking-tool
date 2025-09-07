import { ref, computed, reactive, toRefs } from 'vue'
import type { Campaign } from '~/utils/campaigns/types'

// Create a singleton state that persists across component instances
const state = reactive({
  campaigns: [] as Campaign[],
  isLoading: false,
  error: null as string | null
})

export function useCampaigns() {
  // Get API URL from runtime config
  const config = useRuntimeConfig()
  const apiBaseUrl = config.public.apiBaseUrl
  
  // Fetch all campaigns
  async function fetchCampaigns() {
    state.isLoading = true
    state.error = null
    
    try {
      console.log('Fetching campaigns from API...')
      const response = await fetch(`${apiBaseUrl}/campaigns/`)
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('API response data:', data)
      
      // Handle different response formats
      if (data && typeof data === 'object' && 'results' in data) {
        // Handle paginated response from Django REST Framework
        console.log('Number of campaigns in results:', data.results.length)
        state.campaigns = [...data.results]
      } else if (Array.isArray(data)) {
        // Handle direct array response
        console.log('Number of campaigns in direct array:', data.length)
        state.campaigns = [...data]
      } else {
        console.error('Unexpected API response format:', data)
        state.campaigns = []
      }
      
      console.log('Campaigns after update:', state.campaigns)
      return state.campaigns
    } catch (err) {
      state.error = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error fetching campaigns:', err)
      return []
    } finally {
      state.isLoading = false
    }
  }
  
  // Create a new campaign
  async function createCampaign(campaign: Omit<Campaign, 'id'>) {
    state.isLoading = true
    state.error = null
    
    console.log('Sending campaign data to API:', campaign)
    
    try {
      const response = await fetch(`${apiBaseUrl}/campaigns/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(campaign)
      })
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      const newCampaign = await response.json()
      console.log('Campaign created successfully:', newCampaign)
      
      // Update the local state immediately for instant UI update
      state.campaigns = [...state.campaigns, newCampaign]
      
      return newCampaign
    } catch (err) {
      state.error = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error creating campaign:', err)
      return null
    } finally {
      state.isLoading = false
    }
  }
  
  // Update an existing campaign
  async function updateCampaign(id: string, campaignData: Partial<Campaign>) {
    state.isLoading = true
    state.error = null
    
    try {
      const response = await fetch(`${apiBaseUrl}/campaigns/${id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(campaignData)
      })
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      const updatedCampaign = await response.json()
      
      // Update the local state immediately for instant UI update
      state.campaigns = state.campaigns.map(campaign => 
        campaign.id === id ? { ...campaign, ...updatedCampaign } : campaign
      )
      
      return updatedCampaign
    } catch (err) {
      state.error = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error updating campaign:', err)
      return null
    } finally {
      state.isLoading = false
    }
  }
  
  // Delete a campaign
  async function deleteCampaign(id: string) {
    state.isLoading = true
    state.error = null
    
    try {
      console.log('Deleting campaign with ID:', id)
      const response = await fetch(`${apiBaseUrl}/campaigns/${id}/`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      console.log('Campaign deleted successfully')
      
      // Update the local state immediately for instant UI update
      state.campaigns = state.campaigns.filter(campaign => campaign.id !== id)
      
      return true
    } catch (err) {
      state.error = err instanceof Error ? err.message : 'Unknown error occurred'
      console.error('Error deleting campaign:', err)
      return false
    } finally {
      state.isLoading = false
    }
  }
  
  // Calculate totals
  const totalBudget = computed(() => {
    return state.campaigns.reduce((sum, campaign) => sum + campaign.budget, 0)
  })
  
  const totalSpend = computed(() => {
    return state.campaigns.reduce((sum, campaign) => sum + campaign.spend, 0)
  })
  
  // Return reactive references to state properties
  return {
    ...toRefs(state),
    fetchCampaigns,
    createCampaign,
    updateCampaign,
    deleteCampaign,
    totalBudget,
    totalSpend
  }
}
