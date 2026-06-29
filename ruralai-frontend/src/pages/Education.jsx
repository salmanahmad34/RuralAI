import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { ArrowLeft, BookOpen, Search } from 'lucide-react'
import useFetch from '../hooks/useFetch'
import ResultsDisplay from '../components/ResultsDisplay'
import LoadingSpinner from '../components/LoadingSpinner'

const Education = () => {
  const { t, i18n } = useTranslation()
  const { data: results, loading, fetchQuery } = useFetch()
  const [level, setLevel] = useState('')
  const [needs, setNeeds] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    fetchQuery(`Education query: Level: ${level}, Needs: ${needs}`, 'education', i18n.language)
  }

  return (
    <div className="max-w-4xl mx-auto py-8 animate-in fade-in slide-in-from-bottom-4">
      <Link to="/" className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline mb-8 font-medium">
        <ArrowLeft className="h-4 w-4 mr-2" />
        {t('actions.back')}
      </Link>
      
      <div className="mb-8 flex items-center space-x-4">
        <div className="bg-blue-100 dark:bg-blue-900/30 p-3 rounded-xl">
          <BookOpen className="h-8 w-8 text-blue-600 dark:text-blue-400" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">{t('categories.education')}</h1>
      </div>

      <div className="bg-card border border-gray-200 dark:border-gray-800 rounded-2xl p-6 md:p-8 shadow-sm">
        <h2 className="text-xl font-semibold mb-6">Scholarship & School Locator</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Education Level</label>
              <select 
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                className="w-full p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Level</option>
                <option value="Primary">Primary (1-5)</option>
                <option value="Secondary">Secondary (6-10)</option>
                <option value="Higher Secondary">Higher Secondary (11-12)</option>
                <option value="College">College / Higher Ed</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Specific Need</label>
              <input 
                type="text" 
                value={needs}
                onChange={(e) => setNeeds(e.target.value)}
                placeholder="e.g. Scholarship, Nearest School"
                className="w-full p-3 rounded-md border border-gray-300 dark:border-gray-700 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>
          <button
            type="submit"
            className="flex items-center justify-center w-full md:w-auto space-x-2 bg-blue-500 text-white py-3 px-8 rounded-md hover:bg-blue-600 transition-colors font-medium shadow-sm"
          >
            <span>Search Education Info</span>
            <Search className="h-4 w-4" />
          </button>
        </form>
      </div>

      {loading && <LoadingSpinner text="Searching education databases..." />}
      {!loading && results && <ResultsDisplay results={results} />}
    </div>
  )
}

export default Education
