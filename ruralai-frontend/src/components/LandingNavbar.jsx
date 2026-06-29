import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LandingNavbar() {
  const [scrolled, setScrolled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    window.addEventListener('scroll', () => {
      setScrolled(window.scrollY > 50);
    });
  }, []);

  return (
    <nav className={`fixed w-full z-50 transition-all 
      ${scrolled ? 'bg-white shadow-lg dark:bg-gray-900' : 'bg-transparent'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="text-2xl font-bold text-green-600">RuralAI</div>
          
          {/* Links */}
          <div className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-600 hover:text-green-600 dark:text-gray-300">Features</a>
            <a href="#how-it-works" className="text-gray-600 hover:text-green-600 dark:text-gray-300">How It Works</a>
            <a href="#agents" className="text-gray-600 hover:text-green-600 dark:text-gray-300">Agents</a>
            <a href="#contact" className="text-gray-600 hover:text-green-600 dark:text-gray-300">Contact</a>
          </div>
          
          {/* CTA */}
          <button 
            onClick={() => navigate('/dashboard')}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
          >
            Get Started
          </button>
        </div>
      </div>
    </nav>
  );
}
