import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowLeft, Droplets, Search } from 'lucide-react'
import useFetch from '../hooks/useFetch'
import ResultsDisplay from '../components/ResultsDisplay'
import LoadingSpinner from '../components/LoadingSpinner'

const Water = () => {
  const { t, i18n } = useTranslation()
  const { data: results, loading, fetchQuery } = useFetch()
  const [issue, setIssue] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    fetchQuery(`Water issue: ${issue}`, 'water', i18n.language)
  }

  return (
    <div className="max-w-4xl mx-auto py-8 animate-in fade-in slide-in-from-bottom-4">
      <Link to="/" className="inline-flex items-center text-cyan-600 dark:text-cyan-400 hover:underline mb-8 font-medium">
        <ArrowLeft className="h-4 w-4 mr-2" />
        {t('actions.back')}
      </Link>
      
      <div className="mb-8 flex items-center space-x-4">
        <div className="bg-cyan-100 dark:bg-cyan-900/30 p-3 rounded-xl">
          <Droplets className="h-8 w-8 text-cyan-600 dark:text-cyan-400" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{t('categories.water')}</h1>
      </div>

      <div className="bg-card border border-gray-200 dark:border-gray-800 rounded-2xl p-6 md:p-8 shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Water Supply & Harvesting Info</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Describe Water Issue / Query</label>
            <textarea 
              value={issue}
              onChange={(e) => setIssue(e.target.value)}
              placeholder="e.g. Borewell not working, need rainwater harvesting scheme details"
              className="w-full min-h-[120px] p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-cyan-500"
              required
            />
          </div>
          <button
            type="submit"
            className="flex items-center justify-center w-full md:w-auto space-x-2 bg-cyan-500 text-white py-3 px-8 rounded-md hover:bg-cyan-600 transition-colors font-medium shadow-sm"
          >
            <span>Check Water Resources</span>
            <Search className="h-4 w-4" />
          </button>
        </form>
      </div>

      {loading && <LoadingSpinner text="Checking local water supply data..." />}
      {!loading && results && <ResultsDisplay results={results} />}
    </div>
  )
}

export default Water
