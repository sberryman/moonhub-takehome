import { createClient, type NormalizeOAS } from 'fets'
// import openAPIDoc from '../../../api/openapi.json'
import type api from './api-type.server'

const API_URL = process.env.API_URL

export const apiClient = createClient<NormalizeOAS<typeof api>>({
	endpoint: API_URL,
})

