import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function CTASection() {
  const navigate = useNavigate();

  return (
    <section className="py-20 bg-white dark:bg-gray-800">
      <div className="max-w-4xl mx-auto text-center space-y-8 px-4">
        <h2 className="text-4xl font-bold text-gray-900 dark:text-white">
          Ready to Transform Your Village?
        </h2>
        
        <p className="text-xl text-gray-600 dark:text-gray-300">
          Join millions of Indians using AI to solve real village problems
        </p>
        
        <button
          onClick={() => navigate('/dashboard')}
          className="bg-green-600 hover:bg-green-700 text-white 
            px-12 py-4 rounded-lg font-bold text-lg transition-all
            transform hover:scale-105 shadow-lg"
        >
          Start Using RuralAI Now →
        </button>
        
        <p className="text-sm text-gray-500">
          Free for all. No signup required.
        </p>
      </div>
    </section>
  );
}
