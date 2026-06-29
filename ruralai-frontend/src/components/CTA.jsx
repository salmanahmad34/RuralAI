import React from 'react'
import { Link } from 'react-router-dom'

const CTA = () => {
  return (
    <section className="py-24 bg-white dark:bg-background border-b border-gray-100 dark:border-gray-800">
      <div className="container mx-auto px-4 text-center max-w-4xl">
        <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900 dark:text-white">Ready to empower your community?</h2>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-10 max-w-2xl mx-auto">
          Join thousands of rural citizens utilizing AI to make informed decisions about their livelihoods, health, and future.
        </p>
        <Link to="/dashboard" className="btn-primary text-xl px-12 py-6 rounded-full shadow-lg shadow-green-500/30 hover:shadow-green-500/50 hover:scale-105 transition-all">
          Get Started Now
        </Link>
      </div>
    </section>
  )
}

export default CTA
