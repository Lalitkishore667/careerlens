import { toast } from 'sonner'

export default function ResumeRewriter({ original_bullets, rewritten_bullets, improvements }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-8 mb-8">
      <h3 className="text-2xl font-bold text-white mb-2">Resume Rewriter</h3>
      <p className="text-gray-300 mb-6">{improvements}</p>
      <div className="space-y-4">
        {rewritten_bullets.map((bullet, i) => (
          <div key={i} className="bg-gray-900 border border-gray-700 rounded-lg p-4 hover:border-purple-500">
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1">
                {original_bullets[i] && <p className="text-gray-500 line-through text-sm mb-2">{original_bullets[i]}</p>}
                <p className="text-white">{bullet}</p>
              </div>
              <button onClick={() => { navigator.clipboard.writeText(bullet); toast.success('Copied!') }} className="text-gray-400 hover:text-white">📋</button>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-8 flex justify-center">
        <button onClick={() => { navigator.clipboard.writeText(rewritten_bullets.join('\n\n')); toast.success('All bullets copied!') }} className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg">
          Copy All Bullets
        </button>
      </div>
    </div>
  )
}
