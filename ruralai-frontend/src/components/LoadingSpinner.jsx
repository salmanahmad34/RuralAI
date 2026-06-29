import React from 'react'

const LoadingSpinner = ({ size = "h-8 w-8", text = "Processing..." }) => {
  return (
    <div className="flex flex-col justify-center items-center p-8 space-y-4">
      <div className={`animate-spin rounded-full ${size} border-4 border-gray-200 dark:border-gray-800 border-t-green-500`}></div>
      {text && <p className="text-sm font-medium text-gray-500 dark:text-gray-400 animate-pulse">{text}</p>}
    </div>
  )
}

export default LoadingSpinner
