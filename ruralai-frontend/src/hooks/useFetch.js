import { useState } from 'react'
import { queryAgent } from '../services/api'

const useFetch = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchQuery = async (query, category, language) => {
    setLoading(true)
    setError(null)
    try {
      const response = await queryAgent(query, category, language)
      setData(response.data)
      return response.data
    } catch (err) {
      setError(err.message || 'An error occurred while fetching data')
    } finally {
      setLoading(false)
    }
  }

  return { data, loading, error, fetchQuery }
}

export default useFetch
