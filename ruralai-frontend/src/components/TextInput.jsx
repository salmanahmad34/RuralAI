import React, { useState, useRef, useEffect, useId } from 'react'
import { Send, X } from 'lucide-react'
import { useTranslation } from 'react-i18next'

const TextInput = ({ onSubmit, categories }) => {
  const { t } = useTranslation()
  const [text, setText] = useState('')
  const [category, setCategory] = useState('')
  const [error, setError] = useState('')
  const textareaRef = useRef(null)
  
  const textId = useId()
  const categoryId = useId()

  const MAX_CHARS = 500

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
    }
  }, [text])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!text.trim()) {
      setError('Please enter some text.')
      return
    }
    setError('')
    onSubmit(text, category)
    setText('')
  }

  const handleClear = () => {
    setText('')
    setError('')
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col space-y-4 bg-card p-6 rounded-xl border shadow-sm h-full" noValidate>
      {categories && categories.length > 0 && (
        <div className="flex gap-2 items-center">
          <label htmlFor={categoryId} className="sr-only">Select Category</label>
          <select 
            id={categoryId}
            value={category} 
            onChange={(e) => setCategory(e.target.value)}
            className="border border-gray-300 dark:border-gray-700 bg-background rounded-md px-3 py-2 text-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500 w-full md:w-1/3"
            aria-label="Filter by category"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
        </div>
      )}
      <div className="relative flex-grow flex flex-col">
        <label htmlFor={textId} className="sr-only">{t('input.text_placeholder')}</label>
        <textarea
          id={textId}
          ref={textareaRef}
          value={text}
          onChange={(e) => {
            if (e.target.value.length <= MAX_CHARS) {
              setText(e.target.value)
              if (error) setError('')
            }
          }}
          placeholder={t('input.text_placeholder')}
          className={`w-full flex-grow min-h-[120px] overflow-hidden p-3 rounded-md border bg-background text-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500 resize-none transition-colors ${error ? 'border-red-500 focus-visible:ring-red-500' : 'border-gray-300 dark:border-gray-700'}`}
          aria-invalid={!!error}
          aria-describedby={error ? `${textId}-error` : undefined}
        />
        <div className="absolute bottom-3 right-3 text-xs text-gray-400 font-medium bg-background/80 px-1 rounded" aria-live="polite">
          {text.length}/{MAX_CHARS}
        </div>
      </div>
      {error && (
        <span id={`${textId}-error`} className="text-xs text-red-500 font-medium" role="alert">
          {error}
        </span>
      )}
      <div className="flex justify-end space-x-2 pt-2 border-t border-gray-100 dark:border-gray-800">
        <button
          type="button"
          onClick={handleClear}
          disabled={!text}
          className="flex items-center space-x-1 px-3 py-2 text-sm text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500"
          aria-label="Clear text input"
        >
          <X className="h-4 w-4" aria-hidden="true" />
          <span>{t('input.clear')}</span>
        </button>
        <button
          type="submit"
          disabled={!text.trim()}
          className="flex items-center space-x-2 bg-green-500 text-white py-2 px-6 rounded-md hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm font-medium focus:outline-none focus-visible:ring-2 focus-visible:ring-green-600 focus-visible:ring-offset-2"
          aria-label="Submit query"
        >
          <span>{t('input.submit')}</span>
          <Send className="h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </form>
  )
}

export default TextInput
