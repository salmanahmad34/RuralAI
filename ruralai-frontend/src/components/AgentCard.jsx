import React from 'react'
import { Link } from 'react-router-dom'
import { cn } from '../lib/utils'

const AgentCard = ({ title, description, icon: Icon, to, colorClass, borderColorClass, onClick }) => {
  const content = (
    <div className={cn("group relative overflow-hidden rounded-xl border-2 bg-card p-6 shadow-sm transition-all duration-300 hover:shadow-lg hover:-translate-y-1 h-full", borderColorClass || "border-transparent hover:border-green-500")}>
      <div className={cn("inline-flex p-3 rounded-lg mb-4 transition-transform duration-300 group-hover:scale-110", colorClass)}>
        <Icon className="h-6 w-6" />
      </div>
      <h3 className="font-semibold text-lg mb-2 text-gray-900 dark:text-gray-100">{title}</h3>
      {description && <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{description}</p>}
    </div>
  )

  if (to) {
    return <Link to={to} className="block h-full" onClick={onClick}>{content}</Link>
  }

  return <button onClick={onClick} className="block w-full h-full text-left">{content}</button>
}

export default AgentCard
