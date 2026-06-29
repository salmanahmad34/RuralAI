import React, { useId } from 'react'
import { useTranslation } from 'react-i18next'
import { Globe } from 'lucide-react'

const LanguageSwitcher = () => {
  const { i18n } = useTranslation()
  const langId = useId()

  const handleLanguageChange = (e) => {
    const newLang = e.target.value
    i18n.changeLanguage(newLang)
    localStorage.setItem('language', newLang)
  }

  return (
    <div className="relative flex items-center group">
      <Globe className="absolute left-2 w-4 h-4 text-gray-500 group-hover:text-green-500 transition-colors pointer-events-none" aria-hidden="true" />
      <label htmlFor={langId} className="sr-only">Select Language</label>
      <select
        id={langId}
        value={i18n.language}
        onChange={handleLanguageChange}
        className="appearance-none bg-transparent border border-gray-300 dark:border-gray-700 rounded-md pl-8 pr-6 py-1.5 text-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500 cursor-pointer font-medium"
        aria-label="Language selector"
      >
        <option value="en">English</option>
        <option value="hi">हिंदी</option>
        <option value="mr">मराठी</option>
        <option value="ta">தமிழ்</option>
      </select>
    </div>
  )
}

export default LanguageSwitcher
