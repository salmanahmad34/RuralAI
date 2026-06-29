import React from 'react';

const steps = [
  {
    number: 1,
    icon: '🎤',
    title: 'Ask Your Question',
    description: 'Speak or type in Hindi, Marathi, Tamil, or any language'
  },
  {
    number: 2,
    icon: '🤖',
    title: 'AI Agent Routes Query',
    description: 'Smart routing to the right specialized agent'
  },
  {
    number: 3,
    icon: '🔍',
    title: 'Data Gathering',
    description: 'Real-time data from government and market APIs'
  },
  {
    number: 4,
    icon: '✨',
    title: 'Personalized Solution',
    description: 'Get recommendations in your preferred language'
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16 text-gray-900 dark:text-white">
          How RuralAI Works
        </h2>
        
        <div className="grid md:grid-cols-4 gap-8">
          {steps.map((step) => (
            <div key={step.number} className="flex flex-col items-center">
              <div className="bg-green-600 text-white w-16 h-16 rounded-full 
                flex items-center justify-center text-3xl mb-4">
                {step.icon}
              </div>
              <h3 className="text-xl font-bold text-center mb-2 text-gray-900 dark:text-white">
                {step.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 text-center text-sm">
                {step.description}
              </p>
              {step.number < 4 && (
                <div className="hidden md:block text-2xl text-green-600 mt-4">→</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
