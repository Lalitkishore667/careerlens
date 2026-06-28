import { useState } from 'react'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import UploadSection from './components/UploadSection'
import MatchScore from './components/MatchScore'
import SkillGap from './components/SkillGap'
import ResumeRewriter from './components/ResumeRewriter'
import InterviewPrep from './components/InterviewPrep'
import Footer from './components/Footer'
import { Toaster } from 'sonner'

export default function App() {
  const [showResults, setShowResults] = useState(false)
  const [results, setResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleAnalyze = async (sessionId, jobDescription) => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/full-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          job_description: jobDescription,
        } ),
      })
      const data = await response.json()
      setResults(data)
      setShowResults(true)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <Toaster />
      <Navbar />
      {!showResults ? (
        <>
          <Hero />
          <UploadSection onAnalyze={handleAnalyze} isLoading={isLoading} />
        </>
      ) : (
        <div className="max-w-6xl mx-auto px-4 py-20">
          <button
            onClick={() => setShowResults(false)}
            className="mb-8 px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg"
          >
            New Analysis
          </button>
          {results && (
            <>
              <MatchScore {...results.match} />
              <SkillGap gaps={results.gaps.gaps} />
              <ResumeRewriter {...results.rewrite} />
              <InterviewPrep questions={results.interview.questions} />
            </>
          )}
        </div>
      )}
      <Footer />
    </div>
  )
}
