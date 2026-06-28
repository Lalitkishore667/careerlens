import { useState } from 'react'
import { toast } from 'sonner'

export default function UploadSection({ onAnalyze, isLoading }) {
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [sessionId, setSessionId] = useState(null)

  const handleFileSelect = async (file) => {
    setResumeFile(file)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await fetch('http://localhost:8000/upload-resume', {
        method: 'POST',
        body: formData,
      } )
      const data = await response.json()
      setSessionId(data.session_id)
      toast.success('Resume uploaded!')
    } catch (error) {
      toast.error('Upload failed')
    }
  }

  const handleAnalyze = () => {
    if (!sessionId || !jobDescription.trim()) {
      toast.error('Upload resume and enter job description')
      return
    }
    onAnalyze(sessionId, jobDescription)
  }

  return (
    <div className="py-20 bg-gray-900">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-12 text-white">Start Your Analysis</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <label className="block text-white mb-4 font-semibold">Upload Resume</label>
            <div onClick={() => document.getElementById('file-input').click()} className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-purple-500">
              <input id="file-input" type="file" accept=".pdf,.docx" onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])} className="hidden" />
              <p className="text-white">{resumeFile ? resumeFile.name : 'Click to upload resume'}</p>
            </div>
          </div>
          <div>
            <label className="block text-white mb-4 font-semibold">Job Description</label>
            <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} placeholder="Paste job description..." className="w-full h-64 bg-gray-800 border border-gray-600 rounded-lg p-4 text-white" />
          </div>
        </div>
        <div className="mt-8 flex justify-center">
          <button onClick={handleAnalyze} disabled={isLoading || !sessionId} className="bg-purple-600 hover:bg-purple-700 text-white px-12 py-3 rounded-lg font-semibold disabled:opacity-50">
            {isLoading ? 'Analyzing...' : 'Analyze My Resume'}
          </button>
        </div>
      </div>
    </div>
  )
}
