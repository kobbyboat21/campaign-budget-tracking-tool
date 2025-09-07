import type { Campaign } from './types'

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

// Status color mapping
export const statusColorMap = {
  active: 'success' as const,
  paused: 'warning' as const,
  completed: 'info' as const
}

/**
 * Format a number as GBP currency
 * @param amount - The amount to format
 * @returns Formatted currency string
 */
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP'
  }).format(amount)
}

/**
 * Generate a simple unique ID
 * @returns A string ID based on timestamp and random number
 */
export const generateId = (): string => {
  return Date.now().toString() + Math.floor(Math.random() * 1000).toString()
}
