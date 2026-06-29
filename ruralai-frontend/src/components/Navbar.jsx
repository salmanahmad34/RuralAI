import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Leaf, Sun, Moon, Menu, X } from 'lucide-react'
import LanguageSwitcher from './LanguageSwitcher'

const Navbar = ({ theme, toggleTheme }) => {
  const { t } = useTranslation()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const toggleMobileMenu = () => setIsMobileMenuOpen(!isMobileMenuOpen)

  const navLinks = [
    { name: t('nav.home'), path: '/dashboard' },
    { name: t('nav.about'), path: '#' },
    { name: t('nav.help'), path: '#' }
  ]

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 shadow-sm" aria-label="Main Navigation">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center space-x-2 group" aria-label="Go to Dashboard">
          <div className="bg-green-100 dark:bg-green-900/30 p-1.5 rounded-lg group-hover:bg-green-200 transition-colors" aria-hidden="true">
            <Leaf className="h-6 w-6 text-green-600 dark:text-green-400" />
          </div>
          <span className="font-bold text-lg md:text-xl text-gray-900 dark:text-gray-100">{t('app.title').split(' - ')[0]}</span>
        </Link>
        
        {/* Desktop Nav */}
        <div className="hidden md:flex items-center space-x-6">
          <div className="flex items-center space-x-4 mr-4" role="menubar">
            {navLinks.map((link, idx) => (
              <Link key={idx} to={link.path} className="text-sm font-medium text-gray-600 hover:text-green-600 dark:text-gray-300 dark:hover:text-green-400 transition-colors" role="menuitem">
                {link.name}
              </Link>
            ))}
          </div>
          <LanguageSwitcher />
          <button
            onClick={toggleTheme}
            className="p-2 rounded-md bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500"
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? <Moon className="h-4 w-4 text-gray-700" aria-hidden="true" /> : <Sun className="h-4 w-4 text-gray-300" aria-hidden="true" />}
          </button>
        </div>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden flex items-center space-x-4">
          <button
            onClick={toggleTheme}
            className="p-2 rounded-md bg-gray-100 dark:bg-gray-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500"
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? <Moon className="h-4 w-4" aria-hidden="true" /> : <Sun className="h-4 w-4" aria-hidden="true" />}
          </button>
          <button 
            onClick={toggleMobileMenu} 
            className="p-2 text-gray-600 dark:text-gray-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500 rounded-md"
            aria-expanded={isMobileMenuOpen}
            aria-label="Toggle mobile menu"
            aria-controls="mobile-menu"
          >
            {isMobileMenuOpen ? <X className="h-6 w-6" aria-hidden="true" /> : <Menu className="h-6 w-6" aria-hidden="true" />}
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      {isMobileMenuOpen && (
        <div id="mobile-menu" className="md:hidden border-t bg-background p-4 flex flex-col space-y-4 animate-in slide-in-from-top-2" role="menu">
          {navLinks.map((link, idx) => (
            <Link key={idx} to={link.path} onClick={() => setIsMobileMenuOpen(false)} className="block px-2 py-1 text-base font-medium text-gray-600 hover:text-green-600 dark:text-gray-300 dark:hover:text-green-400" role="menuitem">
              {link.name}
            </Link>
          ))}
          <div className="pt-2 border-t border-gray-100 dark:border-gray-800">
            <LanguageSwitcher />
          </div>
        </div>
      )}
    </nav>
  )
}

export default Navbar
