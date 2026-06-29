import React from 'react'
import { useTranslation } from 'react-i18next'
import { Share2, Bookmark, Printer, Clock, FileText } from 'lucide-react'

const ResultsDisplay = ({ results }) => {
  const { t } = useTranslation()

  if (!results) return null

  return (
    <div className="mt-8 p-6 bg-card border border-green-100 dark:border-green-900/30 rounded-xl shadow-sm animate-in fade-in slide-in-from-bottom-4 print:shadow-none print:border-none print:p-0 print:mt-0" role="region" aria-label="Results">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-6 border-b border-gray-100 dark:border-gray-800 pb-4 gap-4 print:border-b-2 print:border-black">
        <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center print:text-black">
          <FileText className="w-5 h-5 mr-2 text-green-500 print:text-black" aria-hidden="true" />
          {t('results.title')}
        </h2>
        <div className="flex space-x-2 no-print">
          <button className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors focus-visible:ring-2 focus-visible:ring-green-500" title={t('actions.share')} aria-label={t('actions.share')}>
            <Share2 className="h-4 w-4" aria-hidden="true" />
            <span className="hidden sm:inline">{t('actions.share')}</span>
          </button>
          <button className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors focus-visible:ring-2 focus-visible:ring-green-500" title={t('actions.print')} onClick={() => window.print()} aria-label={t('actions.print')}>
            <Printer className="h-4 w-4" aria-hidden="true" />
            <span className="hidden sm:inline">{t('actions.print')}</span>
          </button>
          <button className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors focus-visible:ring-2 focus-visible:ring-green-500" title={t('actions.save')} aria-label={t('actions.save')}>
            <Bookmark className="h-4 w-4" aria-hidden="true" />
            <span className="hidden sm:inline">{t('actions.save')}</span>
          </button>
        </div>
      </div>

      <div className="space-y-6">
        {results.mainRecommendations && results.mainRecommendations.length > 0 && (
          <div className="bg-green-50 dark:bg-green-900/10 p-4 rounded-lg border border-green-100 dark:border-green-900/20 print:border-black print:bg-white print:text-black">
            <h3 className="font-semibold text-green-800 dark:text-green-300 mb-2 print:text-black">Key Recommendations:</h3>
            <ul className="list-disc pl-5 space-y-1 text-green-700 dark:text-green-400 print:text-black">
              {results.mainRecommendations.map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>
          </div>
        )}

        {results.detailedInfo && (
          <div className="prose dark:prose-invert max-w-none text-gray-700 dark:text-gray-300 print:text-black">
            <p className="whitespace-pre-wrap leading-relaxed">{results.detailedInfo}</p>
          </div>
        )}
      </div>

      <div className="mt-8 pt-4 border-t border-gray-100 dark:border-gray-800 flex flex-col sm:flex-row justify-between items-start sm:items-center text-xs text-gray-500 gap-2 print:border-black print:text-black">
        {results.sources && (
          <div className="flex items-center">
            <span className="font-semibold mr-1">{t('results.sources')}:</span>
            {results.sources.join(', ')}
          </div>
        )}
        {results.timestamp && (
          <div className="flex items-center">
            <Clock className="w-3 h-3 mr-1" aria-hidden="true" />
            <span className="sr-only">{t('results.timestamp')}</span>
            {new Date(results.timestamp).toLocaleString()}
          </div>
        )}
      </div>
    </div>
  )
}

export default ResultsDisplay
