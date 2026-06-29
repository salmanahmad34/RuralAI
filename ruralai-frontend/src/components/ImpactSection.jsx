import React from 'react';

export default function ImpactSection() {
  const metrics = [
    { number: '700M+', label: 'Rural Indians' },
    { number: '100+', label: 'Gov Schemes' },
    { number: '6', label: 'AI Agents' },
    { number: '4', label: 'Languages' },
  ];

  return (
    <section className="py-20 bg-gradient-to-r from-green-600 to-blue-600 text-white">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16">
          Impact by Numbers
        </h2>
        
        <div className="grid md:grid-cols-4 gap-8">
          {metrics.map((metric) => (
            <div key={metric.label} className="text-center">
              <div className="text-5xl font-bold mb-2">{metric.number}</div>
              <div className="text-lg">{metric.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
