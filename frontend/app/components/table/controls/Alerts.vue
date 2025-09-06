<script setup lang="ts">
import { ref } from 'vue'

// Modal state
const isOpen = ref(false)

</script>

<template>
  <UModal v-model:open="isOpen">
    <UButton
      variant="ghost"
      size="sm"
      icon="i-heroicons-bell"
      class="h-8 w-8"
      aria-label="Notifications"
    />
    
    <template #content>
      <div class="w-full mx-auto">
        <UCard class="shadow-lg">
          <template #header>
            <div class="pb-2 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-xl font-semibold">Alerts</h3>
            </div>
          </template>
          
          <div class="py-4">
            <p class="text-sm text-gray-500">No new alerts at this time.</p>
          </div>
          
          <template #footer>
            <div class="flex justify-end">
              <UButton
                type="button"
                variant="ghost"
                @click="isOpen = false"
              >
                Close
              </UButton>
            </div>
          </template>
        </UCard>
      </div>
    </template>
  </UModal>
</template>