import React from 'react'
import { Star } from 'lucide-react'

const Testimonials = () => {
  const testimonials = [
    {
      quote: "RuralAI helped me understand which crops would thrive in my soil. The voice feature in Marathi made it incredibly easy.",
      name: "Ramesh P.",
      role: "Farmer, Maharashtra"
    },
    {
      quote: "I found out about government education scholarships for my daughter that I never knew existed.",
      name: "Sita M.",
      role: "Parent, Tamil Nadu"
    },
    {
      quote: "Checking local market prices before selling my harvest has increased my profits by 20%.",
      name: "Amit K.",
      role: "Farmer, Uttar Pradesh"
    }
  ]

  return (
    <section id="testimonials" className="py-20 bg-green-600 dark:bg-green-900">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-white">Community Impact</h2>
          <p className="text-green-100 max-w-2xl mx-auto">See how RuralAI is making a difference across communities.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((t, idx) => (
            <div key={idx} className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl">
              <div className="flex text-yellow-400 mb-4">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-5 h-5 fill-current" />)}
              </div>
              <p className="text-gray-700 dark:text-gray-300 italic mb-6">"{t.quote}"</p>
              <div>
                <p className="font-bold text-gray-900 dark:text-white">{t.name}</p>
                <p className="text-sm text-green-600 dark:text-green-400">{t.role}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Testimonials
