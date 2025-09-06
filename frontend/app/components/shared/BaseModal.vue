<script setup lang="ts">
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  open: {
    type: Boolean,
    required: true
  },
  showDefaultCancel: {
    type: Boolean,
    default: true
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  }
})

defineEmits(['update:open', 'close'])
</script>

<template>
  <UModal :open="open" @update:open="$emit('update:open', $event)">
    <slot name="trigger"></slot>
    
    <template #content>
      <div class="w-full mx-auto">
        <UCard class="shadow-lg">
          <template #header>
            <div class="pb-2 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-xl font-semibold">{{ title }}</h3>
              <p v-if="subtitle" class="text-sm text-gray-500 mt-1">{{ subtitle }}</p>
            </div>
          </template>
          
          <div class="py-4">
            <slot></slot>
          </div>
          
          <template #footer>
            <div class="flex flex-col sm:flex-row sm:justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
              <UButton
                v-if="showDefaultCancel"
                type="button"
                variant="ghost"
                @click="$emit('close')"
                class="w-full sm:w-auto"
              >
                {{ cancelText }}
              </UButton>
              <slot name="footer"></slot>
            </div>
          </template>
        </UCard>
      </div>
    </template>
  </UModal>
</template>
