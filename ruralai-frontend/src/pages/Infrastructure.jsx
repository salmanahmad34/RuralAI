import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowLeft, Building2, Search } from 'lucide-react'
import useFetch from '../hooks/useFetch'
import ResultsDisplay from '../components/ResultsDisplay'
import LoadingSpinner from '../components/LoadingSpinner'

const Infrastructure = () => {
  const { t, i18n } = useTranslation()
  const { data: results, loading, fetchQuery } = useFetch()
  const [infraType, setInfraType] = useState('')
  const [complaint, setComplaint] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    fetchQuery(`Infra Type: ${infraType}, Query: ${complaint}`, 'infrastructure', i18n.language)
  }

  return (
    <div className="max-w-4xl mx-auto py-8 animate-in fade-in slide-in-from-bottom-4">
      <Link to="/" className="inline-flex items-center text-orange-600 dark:text-orange-400 hover:underline mb-8 font-medium">
        <ArrowLeft className="h-4 w-4 mr-2" />
        {t('actions.back')}
      </Link>
      
      <div className="mb-8 flex items-center space-x-4">
        <div className="bg-orange-100 dark:bg-orange-900/30 p-3 rounded-xl">
          <Building2 className="h-8 w-8 text-orange-600 dark:text-orange-400" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{t('categories.infrastructure')}</h1>
      </div>

      <div className="bg-card border border-gray-200 dark:border-gray-800 rounded-2xl p-6 md:p-8 shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Road, Electricity & Comm Reports</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Infrastructure Type</label>
              <select 
                value={infraType}
                onChange={(e) => setInfraType(e.target.value)}
                className="w-full p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              >
                <option value="">Select Category</option>
                <option value="Roads">Roads & Transport</option>
                <option value="Electricity">Electricity</option>
                <option value="Telecom">Mobile/Internet Coverage</option>
                <option value="Other">Other Public Works</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Details</label>
              <input 
                type="text" 
                value={complaint}
                onChange={(e) => setComplaint(e.target.value)}
                placeholder="e.g. Village road broken, no power for 3 days"
                className="w-full p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />
            </div>
          </div>
          <button
            type="submit"
            className="flex items-center justify-center w-full md:w-auto space-x-2 bg-orange-500 text-white py-3 px-8 rounded-md hover:bg-orange-600 transition-colors font-medium shadow-sm"
          >
            <span>Submit / Track</span>
            <Search className="h-4 w-4" />
          </button>
        </form>
      </div>

      {loading && <LoadingSpinner text="Checking infrastructure status..." />}
      {!loading && results && <ResultsDisplay results={results} />}
    </div>
  )
}

export default Infrastructure
