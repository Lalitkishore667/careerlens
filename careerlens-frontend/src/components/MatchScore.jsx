export default function MatchScore({ match_score, matched_skills, missing_skills, summary }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-8 mb-8">
      <h3 className="text-2xl font-bold text-white mb-6">Match Score</h3>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="flex items-center justify-center">
          <div className="relative w-48 h-48">
            <svg className="w-full h-full" viewBox="0 0 200 200">
              <circle cx="100" cy="100" r="90" fill="none" stroke="#374151" strokeWidth="8" />
              <circle cx="100" cy="100" r="90" fill="none" stroke="#7c3aed" strokeWidth="8" strokeDasharray={`${(match_score / 100) * 565.48} 565.48`} />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-5xl font-bold text-white">{match_score}</div>
                <div className="text-sm text-gray-400">%</div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <p className="text-gray-300 mb-6">{summary}</p>
          <div className="mb-6">
            <p className="text-sm font-semibold text-white mb-3">Matched Skills</p>
            <div className="flex flex-wrap gap-2">
              {matched_skills && matched_skills.slice(0, 5).map((skill, i) => (
                <span key={i} className="bg-green-500/20 text-green-300 px-3 py-1 rounded text-sm">✓ {skill}</span>
              ))}
            </div>
          </div>
          <div>
            <p className="text-sm font-semibold text-white mb-3">Missing Skills</p>
            <div className="flex flex-wrap gap-2">
              {missing_skills && missing_skills.slice(0, 5).map((skill, i) => (
                <span key={i} className="bg-red-500/20 text-red-300 px-3 py-1 rounded text-sm">✗ {skill}</span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
