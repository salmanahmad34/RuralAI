import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowLeft, Landmark, Search } from 'lucide-react'
import useFetch from '../hooks/useFetch'
import ResultsDisplay from '../components/ResultsDisplay'
import LoadingSpinner from '../components/LoadingSpinner'

const Finance = () => {
  const { t, i18n } = useTranslation()
  const { data: results, loading, fetchQuery } = useFetch()
  const [financeNeed, setFinanceNeed] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    fetchQuery(`Finance Query: ${financeNeed}`, 'finance', i18n.language)
  }

  return (
    <div className="max-w-4xl mx-auto py-8 animate-in fade-in slide-in-from-bottom-4">
      <Link to="/" className="inline-flex items-center text-purple-600 dark:text-purple-400 hover:underline mb-8 font-medium">
        <ArrowLeft className="h-4 w-4 mr-2" />
        {t('actions.back')}
      </Link>
      
      <div className="mb-8 flex items-center space-x-4">
        <div className="bg-purple-100 dark:bg-purple-900/30 p-3 rounded-xl">
          <Landmark className="h-8 w-8 text-purple-600 dark:text-purple-400" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{t('categories.finance')}</h1>
      </div>

      <div className="bg-card border border-gray-200 dark:border-gray-800 rounded-2xl p-6 md:p-8 shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Loans, Subsidies & Schemes</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">What do you need help with?</label>
            <textarea 
              value={financeNeed}
              onChange={(e) => setFinanceNeed(e.target.value)}
              placeholder="e.g. Need loan for tractor, Check PM Kisan status"
              className="w-full min-h-[120px] p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
          </div>
          <button
            type="submit"
            className="flex items-center justify-center w-full md:w-auto space-x-2 bg-purple-500 text-white py-3 px-8 rounded-md hover:bg-purple-600 transition-colors font-medium shadow-sm"
          >
            <span>Find Schemes</span>
            <Search className="h-4 w-4" />
          </button>
        </form>
      </div>

      {loading && <LoadingSpinner text="Searching government schemes and finance data..." />}
      {!loading && results && <ResultsDisplay results={results} />}
    </div>
  )
}

export default Finance
