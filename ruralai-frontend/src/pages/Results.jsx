import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowLeft } from 'lucide-react'
import ResultsDisplay from '../components/ResultsDisplay'

const Results = () => {
  const { t } = useTranslation()
  const location = useLocation()
  
  const resultsData = location.state?.results || null

  return (
    <div className="max-w-4xl mx-auto py-8 animate-in fade-in slide-in-from-bottom-4">
      <Link to="/" className="inline-flex items-center text-green-600 dark:text-green-400 hover:underline mb-8 font-medium">
        <ArrowLeft className="h-4 w-4 mr-2" />
        {t('actions.back')}
      </Link>
      
      {resultsData ? (
        <ResultsDisplay results={resultsData} />
      ) : (
        <div className="bg-card border border-gray-200 dark:border-gray-800 rounded-2xl p-12 text-center shadow-sm">
          <h1 className="text-3xl font-bold mb-4">{t('results.title')}</h1>
          <p className="text-gray-500">No results found or navigating here directly without context.</p>
        </div>
      )}
    </div>
  )
}

export default Results
