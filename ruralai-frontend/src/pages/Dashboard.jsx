import React from 'react'
import { Tractor, HeartPulse, BookOpen, Droplets, Building2, Landmark } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import VoiceInput from '../components/VoiceInput'
import TextInput from '../components/TextInput'
import AgentCard from '../components/AgentCard'
import ResultsDisplay from '../components/ResultsDisplay'
import LoadingSpinner from '../components/LoadingSpinner'
import useFetch from '../hooks/useFetch'

const Dashboard = () => {
  const { t, i18n } = useTranslation()
  const { data: results, loading, fetchQuery } = useFetch()

  const categories = [
    { id: 'agriculture', name: t('categories.agriculture'), icon: Tractor, color: 'bg-green-100 text-green-600 dark:bg-green-900/30', border: 'hover:border-green-500' },
    { id: 'health', name: t('categories.health'), icon: HeartPulse, color: 'bg-red-100 text-red-600 dark:bg-red-900/30', border: 'hover:border-red-500' },
    { id: 'education', name: t('categories.education'), icon: BookOpen, color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30', border: 'hover:border-blue-500' },
    { id: 'water', name: t('categories.water'), icon: Droplets, color: 'bg-cyan-100 text-cyan-600 dark:bg-cyan-900/30', border: 'hover:border-cyan-500' },
    { id: 'infrastructure', name: t('categories.infrastructure'), icon: Building2, color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30', border: 'hover:border-orange-500' },
    { id: 'finance', name: t('categories.finance'), icon: Landmark, color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30', border: 'hover:border-purple-500' }
  ]

  const handleTranscription = (text) => {
    fetchQuery(text, '', i18n.language)
  }

  const handleSubmit = (text, category) => {
    fetchQuery(text, category, i18n.language)
  }

  return (
    <div className="max-w-5xl mx-auto space-y-12 animate-in fade-in duration-500">
      
      <section className="text-center space-y-4 pt-8 pb-4">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-gray-900 dark:text-gray-100">
          {t('app.title').split(' - ')[0]} <span className="text-green-500">- {t('app.title').split(' - ')[1]}</span>
        </h1>
        <p className="text-xl text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
          {t('app.subtitle')}
        </p>
      </section>

      <section className="bg-card border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
          <div className="md:col-span-4 h-full">
            <VoiceInput onTranscription={handleTranscription} />
          </div>
          <div className="md:col-span-8 h-full">
            <TextInput onSubmit={handleSubmit} categories={categories} />
          </div>
        </div>
      </section>

      {loading && <LoadingSpinner />}
      {!loading && results && <ResultsDisplay results={results} />}

      <section className="pt-8 border-t border-gray-100 dark:border-gray-800">
        <h2 className="text-2xl font-bold mb-8 text-center text-gray-900 dark:text-gray-100">Browse by Category</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {categories.map((cat) => (
            <AgentCard 
              key={cat.id}
              title={cat.name}
              description={`Get specific advice, schemes, and help for ${cat.name.toLowerCase()}.`}
              icon={cat.icon}
              to={`/${cat.id}`}
              colorClass={cat.color}
              borderColorClass={cat.border}
            />
          ))}
        </div>
      </section>
    </div>
  )
}

export default Dashboard
