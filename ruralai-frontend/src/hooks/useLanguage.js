import { useTranslation } from 'react-i18next'

const useLanguage = () => {
  const { i18n } = useTranslation()

  const setLanguage = (lang) => {
    i18n.changeLanguage(lang)
    localStorage.setItem('language', lang)
  }

  return {
    currentLanguage: i18n.language,
    setLanguage
  }
}

export default useLanguage
