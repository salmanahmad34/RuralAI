import React from 'react'
import { Tractor, HeartPulse, BookOpen, Droplets, Building2, Landmark } from 'lucide-react'
import AgentCard from './AgentCard'

const AgentsPreview = () => {
  const agents = [
    {
      title: 'Agriculture Expert',
      description: 'Crop advice, weather updates, and farming techniques.',
      icon: <Tractor className="h-6 w-6 text-green-600 dark:text-green-400" />,
      path: '/dashboard'
    },
    {
      title: 'Health Assistant',
      description: 'Symptom checking, first aid, and medical facility locators.',
      icon: <HeartPulse className="h-6 w-6 text-green-600 dark:text-green-400" />,
      path: '/dashboard'
    },
    {
      title: 'Education Guide',
      description: 'Study materials, scholarships, and career counseling.',
      icon: <BookOpen className="h-6 w-6 text-green-600 dark:text-green-400" />,
      path: '/dashboard'
    },
    {
      title: 'Water Management',
      description: 'Conservation methods and local water quality reports.',
      icon: <Droplets className="h-6 w-6 text-green-600 dark:text-green-400" />,
      path: '/dashboard'
    },
    {
      title: 'Infrastructure',
      description: 'Road conditions, electricity updates, and reporting.',
      icon: <Building2 className="h-6 w-6 text-green-600 dark:text-green-400" />,
      path: '/dashboard'
    },
    {
      title: 'Finance Advisor',
      description: 'Micro-loans, government subsidies, and market prices.',
      icon: <Landmark className="h-6 w-6 text-green-600 dark:text-green-400" />,
      path: '/dashboard'
    }
  ]

  return (
    <section className="py-20 bg-white dark:bg-background">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-gray-900 dark:text-white">6 Specialized Domains</h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">Comprehensive support across all major pillars of rural development.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent, index) => (
            <AgentCard
              key={index}
              title={agent.title}
              description={agent.description}
              icon={agent.icon}
              path={agent.path}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default AgentsPreview
