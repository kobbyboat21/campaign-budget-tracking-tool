<script setup lang="ts">
import { h, resolveComponent, ref, computed, provide, onMounted, watch } from 'vue'
import type { TableColumn } from '@nuxt/ui'
import { getPaginationRowModel } from '@tanstack/vue-table'
import { Campaign } from '~/utils/campaigns/types'
import { generateCampaignColumns } from '~/utils/campaigns/configs'
import { useCampaigns } from '~/composables/useCampaigns'

const UBadge = resolveComponent('UBadge')
const CampaignsActionsEdit = resolveComponent('CampaignsActionsEdit')
const CampaignsActionsDelete = resolveComponent('CampaignsActionsDelete')

// Table reference for pagination
const table = ref(null)

// Modal states
const createModalOpen = ref(false)
const alertsModalOpen = ref(false)

// Use the campaigns composable
const { campaigns, isLoading, error, fetchCampaigns, totalBudget, totalSpend } = useCampaigns()

// Pagination state
const pagination = ref({
  pageIndex: 0,
  pageSize: 5
})

// Create a refresh function that will be provided to child components
const refreshTable = async () => {
  await fetchCampaigns()
}

// Fetch campaigns on component mount
onMounted(() => {
  fetchCampaigns()
})

// Watch for changes in the campaigns array
watch(campaigns, () => {}, { deep: true })

// Generate table columns using the factory function
const columns = generateCampaignColumns(h, { UBadge, CampaignsActionsEdit, CampaignsActionsDelete })

// Provide data to child components
provide('campaigns', campaigns)
provide('refreshTable', refreshTable)
</script>

<template>
  <div class="space-y-4">
    <div v-if="isLoading" class="flex justify-center p-4">
      <UIcon name="i-heroicons-arrow-path" class="animate-spin h-6 w-6" />
    </div>
    
    <div v-else-if="error" class="text-red-500 p-4 text-center">
      {{ error }}
    </div>
    <div v-else class="w-full space-y-4 pb-4">
      <UTable
        ref="table"
        v-model:pagination="pagination"
        :data="campaigns"
        :columns="columns"
        :pagination-options="{
          getPaginationRowModel: getPaginationRowModel()
        }"
        class="flex-1"
      />

      <div class="flex justify-center border-t border-default pt-4">
        <UPagination
          :default-page="(table?.tableApi?.getState().pagination.pageIndex || 0) + 1"
          :items-per-page="table?.tableApi?.getState().pagination.pageSize"
          :total="campaigns.length"
          @update:page="(p) => table?.tableApi?.setPageIndex(p - 1)"
        />
      </div>
    </div>
  </div>
</template>
