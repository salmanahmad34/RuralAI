import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowLeft, Tractor, Search } from 'lucide-react'
import useFetch from '../hooks/useFetch'
import ResultsDisplay from '../components/ResultsDisplay'
import LoadingSpinner from '../components/LoadingSpinner'

const Agriculture = () => {
  const { t, i18n } = useTranslation()
  const { data: results, loading, fetchQuery } = useFetch()
  const [crop, setCrop] = useState('')
  const [soilType, setSoilType] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const query = `Provide agriculture advice for Crop: ${crop}, Soil Type: ${soilType}`
    fetchQuery(query, 'agriculture', i18n.language)
  }

  return (
    <div className="max-w-4xl mx-auto py-8 animate-in fade-in slide-in-from-bottom-4">
      <Link to="/" className="inline-flex items-center text-green-600 dark:text-green-400 hover:underline mb-8 font-medium">
        <ArrowLeft className="h-4 w-4 mr-2" />
        {t('actions.back')}
      </Link>
      
      <div className="mb-8 flex items-center space-x-4">
        <div className="bg-green-100 dark:bg-green-900/30 p-3 rounded-xl">
          <Tractor className="h-8 w-8 text-green-600 dark:text-green-400" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{t('categories.agriculture')}</h1>
      </div>

      <div className="bg-card border border-gray-200 dark:border-gray-800 rounded-2xl p-6 md:p-8 shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Crop Advisory & Schemes</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Crop Name</label>
              <input 
                type="text" 
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                placeholder="e.g. Wheat, Rice, Cotton"
                className="w-full p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Soil Type</label>
              <select 
                value={soilType}
                onChange={(e) => setSoilType(e.target.value)}
                className="w-full p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              >
                <option value="">Select Soil Type</option>
                <option value="Alluvial">Alluvial</option>
                <option value="Black">Black (Regur)</option>
                <option value="Red">Red & Yellow</option>
                <option value="Laterite">Laterite</option>
                <option value="Arid">Arid</option>
              </select>
            </div>
          </div>
          <button
            type="submit"
            className="flex items-center justify-center w-full md:w-auto space-x-2 bg-green-500 text-white py-3 px-8 rounded-md hover:bg-green-600 transition-colors font-medium shadow-sm"
          >
            <span>Get Advisory</span>
            <Search className="h-4 w-4" />
          </button>
        </form>
      </div>

      {loading && <LoadingSpinner text="Analyzing agricultural data..." />}
      {!loading && results && <ResultsDisplay results={results} />}
    </div>
  )
}

export default Agriculture
