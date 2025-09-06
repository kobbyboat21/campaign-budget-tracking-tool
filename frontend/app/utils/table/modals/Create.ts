// Import shared types and configurations from types.ts
import { defaultCampaign, campaignFormFields, campaignValidationRules } from '../types'

// Re-export the form fields and validation rules
export const formFields = campaignFormFields
export const validationRules = campaignValidationRules

// Generate a simple ID
export const generateId = (): string => {
  return Date.now().toString() + Math.floor(Math.random() * 1000).toString()
}

// Re-export for convenience
export { defaultCampaign }