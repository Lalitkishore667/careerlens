import { useState } from 'react'

export default function SkillGap({ gaps }) {
  const [expanded, setExpanded] = useState(null)

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-8 mb-8">
      <h3 className="text-2xl font-bold text-white mb-6">Skill Gap Roadmap</h3>
      <div className="space-y-4">
        {gaps.map((gap, i) => (
          <div key={i} className="border border-gray-700 rounded-lg overflow-hidden">
            <button onClick={() => setExpanded(expanded === i ? null : i)} className="w-full bg-gray-700 hover:bg-gray-600 p-4 flex justify-between items-center">
              <div className="text-left">
                <h4 className="font-semibold text-white">{gap.skill}</h4>
                <span className="text-sm bg-orange-500/20 text-orange-300 px-2 py-1 rounded">{gap.importance}</span>
              </div>
              <span className="text-white">{expanded === i ? '▼' : '▶'}</span>
            </button>
            {expanded === i && (
              <div className="bg-gray-900 p-4 border-t border-gray-700">
                <p className="text-gray-300 mb-4"><span className="font-semibold text-white">How to Learn:</span> {gap.how_to_learn}</p>
                <p className="text-sm font-semibold text-white mb-2">Resources:</p>
                <ul className="text-gray-400 text-sm space-y-1">
                  {gap.resources.map((r, j) => <li key={j}>→ {r}</li>)}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
