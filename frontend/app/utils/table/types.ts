// Campaign-related shared types
export interface Campaign {
  id: string
  name: string
  budget: number
  spend: number
  status: 'active' | 'paused' | 'completed'
}

export interface FormField {
  id: string
  label: string
  type: string
  placeholder: string
  modelValue: string
  inputProps: Record<string, any>
  items?: Array<{ label: string; value: string }>
}

// Default empty campaign
export const defaultCampaign: Campaign = {
  id: '',
  name: '',
  budget: 0,
  spend: 0,
  status: 'active'
}

// Status options for dropdowns
export const statusOptions = [
  { label: 'Active', value: 'active' },
  { label: 'Paused', value: 'paused' },
  { label: 'Completed', value: 'completed' }
]

// Shared form fields configuration for campaign forms
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

// Shared validation rules for campaign forms
export const campaignValidationRules = {
  name: { required: true, message: 'Campaign name is required' },
  budget: { required: true, min: 0.01, message: 'Budget must be greater than £0' },
  spend: { required: true, min: 0, message: 'Spend must be a positive number' },
  status: { required: true, message: 'Status is required' }
}
