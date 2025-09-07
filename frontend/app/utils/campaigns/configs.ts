import type { TableColumn } from '@nuxt/ui'
import type { Campaign, FormField } from './types'
import { statusOptions, statusColorMap, formatCurrency } from './constants'

/**
 * Shared form fields configuration for campaign forms
 */
export const campaignFormFields: FormField[] = [
  {
    id: 'name',
    label: 'Campaign Name',
    type: 'text',
    placeholder: 'Enter campaign name',
    modelValue: 'name',
    inputProps: {}
  },
  {
    id: 'budget',
    label: 'Budget (£)',
    type: 'number',
    placeholder: 'Enter budget amount',
    modelValue: 'budget',
    inputProps: { min: '0.01' }
  },
  {
    id: 'spend',
    label: 'Spend (£)',
    type: 'number',
    placeholder: 'Enter spend amount',
    modelValue: 'spend',
    inputProps: { min: '0' }
  },
  {
    id: 'status',
    label: 'Status',
    type: 'select',
    placeholder: 'Select status',
    modelValue: 'status',
    inputProps: {},
    items: statusOptions
  }
]

/**
 * Shared validation rules for campaign forms
 */
export const campaignValidationRules = {
  name: { required: true, message: 'Campaign name is required' },
  budget: { required: true, min: 0.01, message: 'Budget must be greater than £0' },
  spend: { required: true, min: 0, message: 'Spend must be a positive number' },
  status: { required: true, message: 'Status is required' }
}

/**
 * Generate table columns configuration for campaigns
 * @param h - Vue's h function for creating virtual DOM nodes
 * @param components - Object containing component references
 * @returns Array of table column configurations
 */
export const generateCampaignColumns = (
  h: Function,
  components: {
    UBadge: any,
    CampaignsActionsEdit: any,
    CampaignsActionsDelete: any
  }
): TableColumn<Campaign>[] => {
  const { UBadge, CampaignsActionsEdit, CampaignsActionsDelete } = components
  
  return [
    {
      accessorKey: 'name',
      header: 'Name'
    },
    {
      accessorKey: 'budget',
      header: () => h('div', { class: 'text-right' }, 'Budget'),
      cell: ({ row }) => {
        const amount = Number(row.getValue('budget'))
        return h('div', { class: 'text-right font-medium' }, formatCurrency(amount))
      }
    },
    {
      accessorKey: 'spend',
      header: () => h('div', { class: 'text-right' }, 'Spend'),
      cell: ({ row }) => {
        const amount = Number(row.getValue('spend'))
        return h('div', { class: 'text-right font-medium' }, formatCurrency(amount))
      }
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }) => {
        const status = row.getValue('status') as string
        const color = statusColorMap[status as keyof typeof statusColorMap]

        return h(UBadge, { class: 'capitalize', variant: 'subtle', color }, () => status)
      }
    },
    {
      id: 'actions',
      header: '',
      cell: ({ row }) => {
        const campaign = row.original
        return h('div', { class: 'flex gap-2 justify-center' }, [
          h(CampaignsActionsEdit, { campaign }),
          h(CampaignsActionsDelete, { campaign })
        ])
      }
    }
  ]
}
