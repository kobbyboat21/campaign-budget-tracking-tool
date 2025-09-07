<script setup lang="ts">
import { ref, inject } from 'vue'
import { useCampaigns } from '~/composables/useCampaigns'

const props = defineProps({
  campaign: {
    type: Object,
    required: true
  },
  onDeleted: {
    type: Function,
    default: () => {}
  }
})

// Get API functions from composable
const { deleteCampaign, fetchCampaigns } = useCampaigns()

// Get refresh function from parent
const refreshTable = inject('refreshTable', () => {})

// Modal state
const isOpen = ref(false)

// Handle delete confirmation
const handleDelete = async () => {
  try {
    // Use the API composable to delete the campaign
    await deleteCampaign(props.campaign.id)
    
    // Fetch all campaigns to ensure the UI is updated with the latest data
    await fetchCampaigns()
    
    console.log('Campaign deleted and table refreshed')
    
    // Close the modal
    closeModal()
    
    // Call the onDeleted prop function to notify parent
    props.onDeleted()
    
    // Force table refresh
    refreshTable()
  } catch (error) {
    console.error('Failed to delete campaign:', error)
    // Here you could add error handling UI feedback
  }
}

// Close the modal
const closeModal = () => {
  isOpen.value = false
}
</script>

<template>
  <SharedBaseModal 
    v-model:open="isOpen"
    title="Delete Campaign"
    @close="closeModal"
  >
    <template #trigger>
      <button 
        class="flex items-center justify-center w-8 h-8 rounded-md hover:bg-gray-100 transition-colors"
        @click="isOpen = true"
        aria-label="Delete Campaign"
      >
        <!-- Direct SVG implementation for complete color control -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-red-600">
          <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
        </svg>
      </button>
    </template>
    
    <div class="py-2 space-y-4">
      <p class="text-base">
        Are you sure you want to delete the campaign <strong>{{ props.campaign.name }}</strong>?
      </p>
      <p class="text-sm text-red-500">
        This action cannot be undone.
      </p>
    </div>
    
    <template #footer>
      <UButton
        color="red"
        @click="handleDelete"
        class="w-full sm:w-auto hover:bg-red-500"
      >
        Delete
      </UButton>
    </template>
  </SharedBaseModal>
</template>