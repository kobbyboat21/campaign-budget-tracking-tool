<script setup lang="ts">
import { ref, inject } from 'vue'
import { campaignFormFields as formFields, campaignValidationRules as validationRules } from '~/utils/campaigns/configs'
import { useCampaigns } from '~/composables/useCampaigns'

const props = defineProps({
  campaign: {
    type: Object,
    required: true
  },
  onUpdated: {
    type: Function,
    default: () => {}
  }
})

// Get API functions from composable
const { updateCampaign, fetchCampaigns } = useCampaigns()

// Get refresh function from parent
const refreshTable = inject('refreshTable', () => {})

// Create a copy of the campaign for editing
const editedCampaign = ref({...props.campaign})

// Modal state
const isOpen = ref(false)

// Handle form submission
const handleSubmit = async (event) => {
  // Prevent default form submission
  event.preventDefault()
  
  // Validate budget is greater than zero
  if (editedCampaign.value.budget <= 0) {
    alert('Budget must be greater than £0')
    return
  }
  
  try {
    // Use the API composable to update the campaign
    await updateCampaign(props.campaign.id, {
      name: editedCampaign.value.name,
      budget: editedCampaign.value.budget,
      spend: editedCampaign.value.spend,
      status: editedCampaign.value.status
    })
    
    // Fetch all campaigns to ensure the UI is updated with the latest data
    await fetchCampaigns()
    
    console.log('Campaign updated and table refreshed')
    
    // Close the modal
    closeModal()
    
    // Call the onUpdated prop function to notify parent
    props.onUpdated()
    
    // Force table refresh
    refreshTable()
  } catch (error) {
    console.error('Failed to update campaign:', error)
    // Here you could add error handling UI feedback
  }
}

// Close the modal
const closeModal = () => {
  isOpen.value = false
}

// Open the modal
const openModal = () => {
  // Reset the form with the current campaign data
  editedCampaign.value = { ...props.campaign }
  isOpen.value = true
}
</script>

<template>
  <SharedBaseModal 
    v-model:open="isOpen"
    title="Edit Campaign"
    subtitle="Update campaign details below"
    @close="closeModal"
  >
    <template #trigger>
      <UButton
        variant="ghost"
        size="sm"
        color="primary"
        icon="i-heroicons-pencil-square"
        class="h-8 w-8"
        @click="openModal"
        aria-label="Edit Campaign"
      />
    </template>
    
    <form @submit.prevent="handleSubmit" class="space-y-5">
      <!-- Dynamically render form fields based on configuration -->
      <div v-for="field in formFields" :key="field.id" class="space-y-3">
        <label :for="`edit-campaign-${field.id}`" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          {{ field.label }}
        </label>
        
        <!-- Render UInput for text/number fields -->
        <UInput 
          v-if="field.type !== 'select'"
          :id="`edit-campaign-${field.id}`"
          v-model="editedCampaign[field.modelValue]"
          :type="field.type"
          :placeholder="field.placeholder"
          v-bind="field.inputProps"
          class="w-full"
        />
        
        <!-- Render USelect for select fields -->
        <USelect
          v-else
          :id="`edit-campaign-${field.id}`"
          v-model="editedCampaign[field.modelValue]"
          :items="field.items"
          :placeholder="field.placeholder"
          class="w-full"
        />
      </div>
    </form>
    
    <template #footer>
      <UButton
        type="button"
        color="primary"
        @click="handleSubmit"
        class="w-full sm:w-auto"
      >
        Save Changes
      </UButton>
    </template>
  </SharedBaseModal>
</template>