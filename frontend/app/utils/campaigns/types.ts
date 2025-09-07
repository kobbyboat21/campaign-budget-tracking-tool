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

// Type for campaign status
export type CampaignStatus = 'active' | 'paused' | 'completed'
