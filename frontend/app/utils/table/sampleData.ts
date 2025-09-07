import type { Campaign } from '~/utils/table/types'

// Sample campaign data
export const campaignData: Campaign[] = [
  {
    id: '1',
    name: 'Summer Sale Campaign',
    budget: 5000,
    spend: 3250,
    status: 'active'
  },
  {
    id: '2',
    name: 'Black Friday Promotion',
    budget: 7500,
    spend: 7500,
    status: 'completed'
  },
  {
    id: '3',
    name: 'New Product Launch',
    budget: 10000,
    spend: 4200,
    status: 'active'
  },
  {
    id: '4',
    name: 'Holiday Season Ads',
    budget: 6000,
    spend: 2100,
    status: 'paused'
  },
  {
    id: '5',
    name: 'Brand Awareness',
    budget: 3500,
    spend: 3200,
    status: 'active'
  }
]

// Utility functions
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP'
  }).format(amount)
}

// Status color mapping
export const statusColorMap = {
  active: 'success' as const,
  paused: 'warning' as const,
  completed: 'info' as const
}