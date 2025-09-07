
<script setup lang="ts">
// Feature to be worked on. Not implemented yet.

import { ref } from 'vue'

// Modal state
const isOpen = ref(false)

// Filter options
const filterOptions = ref({
  status: [],
  minBudget: null,
  maxBudget: null
})

// Status options
const statusOptions = [
  { label: 'Active', value: 'active' },
  { label: 'Paused', value: 'paused' },
  { label: 'Completed', value: 'completed' }
]

// Open the modal
const openModal = () => {
  isOpen.value = true
}

// Apply filters
const applyFilters = () => {
  // Here you would implement the actual filtering logic
  isOpen.value = false
}

// Reset filters
const resetFilters = () => {
  filterOptions.value = {
    status: [],
    minBudget: null,
    maxBudget: null
  }
}
</script>

<template>
  <UModal v-model="isOpen">
    <UButton
      variant="ghost"
      size="sm"
      icon="i-heroicons-funnel"
      class="h-8 w-8"
      @click="openModal"
      aria-label="Filter"
    />
    
    <template #content>
      <div class="w-full mx-auto">
        <UCard class="shadow-lg">
          <template #header>
            <div class="pb-2 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-xl font-semibold">Filter Campaigns</h3>
            </div>
          </template>
          
          <div class="py-4 space-y-5">
            <div class="space-y-3">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Status
              </label>
              <USelectMenu
                v-model="filterOptions.status"
                :items="statusOptions"
                multiple
                placeholder="Select statuses"
                class="w-full"
              />
            </div>
            
            <div class="space-y-3">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Budget Range (£)
              </label>
              <div class="flex gap-2">
                <UInput
                  v-model.number="filterOptions.minBudget"
                  type="number"
                  placeholder="Min"
                  class="w-1/2"
                />
                <UInput
                  v-model.number="filterOptions.maxBudget"
                  type="number"
                  placeholder="Max"
                  class="w-1/2"
                />
              </div>
            </div>
          </div>
          
          <template #footer>
            <div class="flex flex-col sm:flex-row sm:justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
              <UButton
                variant="ghost"
                @click="resetFilters"
                class="w-full sm:w-auto"
              >
                Reset
              </UButton>
              <UButton
                variant="ghost"
                @click="isOpen = false"
                class="w-full sm:w-auto"
              >
                Cancel
              </UButton>
              <UButton
                color="primary"
                @click="applyFilters"
                class="w-full sm:w-auto"
              >
                Apply
              </UButton>
            </div>
          </template>
        </UCard>
      </div>
    </template>
  </UModal>
</template>