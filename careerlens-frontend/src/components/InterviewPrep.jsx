import { useState } from 'react'

export default function InterviewPrep({ questions }) {
  const [expanded, setExpanded] = useState(null)

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-8 mb-8">
      <h3 className="text-2xl font-bold text-white mb-2">Interview Prep</h3>
      <p className="text-gray-400 mb-6">10 role-specific questions to help you prepare</p>
      <div className="space-y-4">
        {questions.map((q, i) => (
          <div key={i} className="border border-gray-700 rounded-lg overflow-hidden">
            <button onClick={() => setExpanded(expanded === i ? null : i)} className="w-full bg-gray-700 hover:bg-gray-600 p-4 flex justify-between items-start">
              <div className="text-left">
                <h4 className="font-semibold text-white mb-2">{i + 1}. {q.question}</h4>
                <div className="flex gap-2">
                  <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">{q.difficulty}</span>
                  <span className="text-xs bg-purple-500/20 text-purple-300 px-2 py-1 rounded">{q.category}</span>
                </div>
              </div>
              <span className="text-white">{expanded === i ? '▼' : '▶'}</span>
            </button>
            {expanded === i && (
              <div className="bg-gray-900 p-4 border-t border-gray-700">
                <p className="text-sm font-semibold text-cyan-400 mb-2">Hint / Approach:</p>
                <p className="text-gray-300">{q.hint}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
