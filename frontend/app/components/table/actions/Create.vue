<script setup lang="ts">
import { ref, inject } from 'vue'
import { defaultCampaign, formFields, validationRules, generateId } from '~/utils/table/modals/Create'
import { useCampaigns } from '~/composables/useCampaigns'

// Get API functions from composable
const { createCampaign, fetchCampaigns } = useCampaigns()

// Get refresh function from parent
const refreshTable = inject('refreshTable', () => {})

// Modal state
const isOpen = ref(false)

// New campaign data
const newCampaign = ref({...defaultCampaign})

// Reset form
const resetForm = () => {
  newCampaign.value = {...defaultCampaign}
}

// Close the modal
const closeModal = () => {
  resetForm()
  isOpen.value = false
}

// Handle form submission
const handleSubmit = async (event) => {
  // Prevent default form submission
  event.preventDefault()
  
  // Validate budget is greater than zero
  if (newCampaign.value.budget <= 0) {
    alert('Budget must be greater than £0')
    return
  }
  
  try {
    // Use the API composable to create the campaign
    const result = await createCampaign({
      name: newCampaign.value.name,
      budget: newCampaign.value.budget,
      spend: newCampaign.value.spend,
      status: newCampaign.value.status
    })
    
    // Fetch all campaigns to ensure the UI is updated with the latest data
    await fetchCampaigns()
    
    console.log('Campaign created and table refreshed')
    
    // Force table refresh
    refreshTable()
    
    // Reset the form and close the modal on success
    closeModal()
  } catch (error) {
    console.error('Failed to create campaign:', error)
    // Here you could add error handling UI feedback
  }
}

// Open the modal
const openModal = () => {
  resetForm()
  isOpen.value = true
}
</script>

<template>
  <SharedBaseModal 
    v-model:open="isOpen"
    title="Add New Campaign"
    subtitle="Enter campaign details below"
    @close="closeModal"
  >
    <template #trigger>
      <UButton
        color="primary"
        icon="i-heroicons-plus"
        class="px-4 py-2"
        @click="openModal"
      >
        Add Campaign
      </UButton>
    </template>
    
    <form @submit.prevent="handleSubmit" class="space-y-5">
      <!-- Dynamically render form fields based on configuration -->
      <div v-for="field in formFields" :key="field.id" class="space-y-3">
        <label :for="`campaign-${field.id}`" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          {{ field.label }}
        </label>
        
        <!-- Render UInput for text/number fields -->
        <UInput 
          v-if="field.type !== 'select'"
          :id="`campaign-${field.id}`"
          v-model="newCampaign[field.modelValue]"
          :type="field.type"
          :placeholder="field.placeholder"
          v-bind="field.inputProps"
          class="w-full"
        />
        
        <!-- Render USelect for select fields -->
        <USelect
          v-else
          :id="`campaign-${field.id}`"
          v-model="newCampaign[field.modelValue]"
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
        Create Campaign
      </UButton>
    </template>
  </SharedBaseModal>
</template>
