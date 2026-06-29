import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request Interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method.toUpperCase()} ${config.url}`, config.data || '')
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response Interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`, response.data)
    return response
  },
  (error) => {
    console.error(`[API Error]`, error.response || error.message)
    const userMessage = error.response?.data?.message || "An unexpected error occurred. Please try again."
    return Promise.reject(new Error(userMessage))
  }
)

export const queryAgent = async (query, category, language) => {
  try {
    const response = await api.post('/api/query', { query, category, language })
    const backendData = response.data

    // Map backend schema (QueryResponse) to frontend UI expectations
    const mainRecommendations = backendData.recommendations.map(r => r.title)
    const detailedInfo = backendData.recommendations.map(r => {
      let info = r.description
      if (r.confidence) {
        info += `\n(Confidence Score: ${Math.round(r.confidence * 100)}%)`
      }
      return info
    }).join('\n\n')

    return {
      data: {
        success: true,
        mainRecommendations,
        detailedInfo,
        sources: backendData.sources,
        timestamp: backendData.timestamp
      }
    }
  } catch (error) {
    console.error("API Call to /api/query failed:", error)
    throw error
  }
}

export const getSchemes = async (category) => {
  try {
    const response = await api.get(`/api/schemes/${category}`)
    
    // Map backend scheme data model to UI items (id, name, details)
    const mappedData = response.data.map((scheme, idx) => ({
      id: scheme.id || idx,
      name: scheme.name,
      details: `${scheme.type}. benefit: ${scheme.amount_per_year} INR/year. Authority: ${scheme.authority}. Documents: ${scheme.documents_required ? scheme.documents_required.join(', ') : 'None'}`
    }))
    
    return { data: mappedData }
  } catch (error) {
    console.error(`API Call to /api/schemes/${category} failed:`, error)
    throw error
  }
}

export const getAgents = async () => {
  try {
    const response = await api.get('/api/agents')
    return response
  } catch (error) {
    console.error("API Call to /api/agents failed:", error)
    throw error
  }
}

export default api
