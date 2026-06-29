import React from 'react';

const features = [
  {
    icon: '🌾',
    title: 'Agriculture',
    description: 'Crop selection, disease detection, fertilizer recommendations, market rates'
  },
  {
    icon: '🏥',
    title: 'Health',
    description: 'Health camps, vaccination tracking, nearby hospitals, disease information'
  },
  {
    icon: '📚',
    title: 'Education',
    description: 'Scholarships, school finder, eligibility checker, career guidance'
  },
  {
    icon: '💧',
    title: 'Water',
    description: 'Groundwater levels, rainwater harvesting, water quality, bore wells'
  },
  {
    icon: '🏗️',
    title: 'Infrastructure',
    description: 'Road status, electricity, mobile coverage, government projects'
  },
  {
    icon: '💰',
    title: 'Finance',
    description: '100+ schemes, loan eligibility, subsidies, insurance options'
  },
];

export default function FeaturesSection() {
  return (
    <section id="features" className="py-20 bg-white dark:bg-gray-800">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-4 text-gray-900 dark:text-white">
          6 Specialized AI Agents
        </h2>
        <p className="text-center text-gray-600 dark:text-gray-300 mb-12">
          Each agent is trained for specific village needs
        </p>
        
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div 
              key={feature.title}
              className="bg-gray-50 dark:bg-gray-700 p-8 rounded-xl 
                hover:shadow-xl hover:scale-105 transition-all duration-300"
            >
              <div className="text-5xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-3 text-gray-900 dark:text-white">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-300">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
