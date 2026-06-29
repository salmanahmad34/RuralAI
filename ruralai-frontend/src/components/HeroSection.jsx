import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function HeroSection() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 
      dark:from-gray-900 dark:to-gray-800 flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          
          {/* Left side - Text */}
          <div className="space-y-8 animate-fade-in">
            <h1 className="text-5xl md:text-6xl font-bold 
              bg-gradient-to-r from-green-600 to-blue-600 
              bg-clip-text text-transparent">
              RuralAI
            </h1>
            
            <h2 className="text-3xl md:text-4xl font-semibold text-gray-900 dark:text-white">
              AI Village Development Officer
            </h2>
            
            <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
              Empowering 700 million rural Indians with AI-powered solutions for 
              agriculture, health, education, water, infrastructure, and financial inclusion.
            </p>
            
            <div className="flex gap-4">
              <button 
                onClick={() => navigate('/dashboard')}
                className="bg-green-600 hover:bg-green-700 text-white 
                  px-8 py-3 rounded-lg font-semibold transition">
                Get Started
              </button>
              <button className="border-2 border-green-600 text-green-600 
                hover:bg-green-50 px-8 py-3 rounded-lg font-semibold transition">
                Learn More
              </button>
            </div>
            
            <div className="flex gap-4 text-3xl">
              🌾 🏥 📚 💧 🏗️ 💰
            </div>
          </div>
          
          {/* Right side - Illustration */}
          <div className="hidden md:flex justify-center">
            <svg className="w-96 h-96" viewBox="0 0 400 400">
              {/* Simple farmer illustration */}
              <circle cx="200" cy="150" r="30" fill="#22C55E"/>
              <rect x="170" y="180" width="60" height="80" fill="#3B82F6"/>
              <rect x="160" y="100" width="80" height="60" fill="#10B981"/>
              {/* Fields below */}
              <path d="M 100 300 L 300 300 L 290 350 L 110 350 Z" fill="#86EFAC"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
