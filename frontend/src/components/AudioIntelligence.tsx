
import { useState } from 'react'
import {
  AudioLines,
  Upload,
  Music2,
  Activity,
  Sparkles,
  LoaderCircle,
  AlertCircle,
} from 'lucide-react'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8765'
).replace(/\/$/, '')

const API_PREFIX = '/api/v1'

type AudioAnalysis = {
  audio: {
    sample_rate: number
    duration_seconds: number
    channels: number
    waveform: number[]
    peak_amplitude: number
  }
  pitch: {
    average_frequency: number | null
    frequencies: (number | null)[]
    times: number[]
    confidence: number[]
    voiced_frames: number
    total_frames: number
    voiced_ratio: number
  }
  swara: {
    tonic_frequency: number
    detected_swaras: string[]
  }
  raga: {
    candidate_count: number
    candidates: {
      name: string
      match_percentage: number
      arohanam?: string
      avarohanam?: string
      notes?: string
    }[]
    warning?: string
  }
}

function AudioIntelligence() {
  const [file, setFile] = useState<File | null>(null)
  const [tonic, setTonic] = useState('261.63')
  const [analysis, setAnalysis] = useState<AudioAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyzeAudio = async () => {
    if (!file) {
      setError('Please select an audio recording first.')
      return
    }

    const tonicValue = Number(tonic)

    if (!Number.isFinite(tonicValue) || tonicValue <= 0) {
      setError('Enter a valid positive tonic frequency.')
      return
    }

    setLoading(true)
    setError('')
    setAnalysis(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('tonic_frequency', tonic)

    try {
      const token = sessionStorage.getItem('ragaverse_token')

if (!token) {
  throw new Error('Please log in to analyze audio.')
}

const response = await fetch(
  `${API_BASE_URL}${API_PREFIX}/audio/analyze`,
  {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  },
)

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Audio analysis failed.')
      }

      setAnalysis(data.analysis)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to analyze this recording.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-7">
      <section>
        <p className="text-xs font-semibold uppercase tracking-[0.25em] text-amber-400">
          Listen · Analyze · Discover
        </p>

        <h1 className="mt-2 text-3xl font-bold text-amber-200 sm:text-4xl">
          Audio Intelligence
        </h1>

        <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400">
          Upload your Carnatic music recording and explore its
          pitch, swaras and possible raga identities with RagaVerse AI.
        </p>
      </section>

      <section className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-6">
        <div className="mb-6 flex items-center gap-3">
          <div className="rounded-xl bg-amber-400/10 p-3 text-amber-400">
            <Upload size={23} />
          </div>

          <div>
            <h2 className="font-semibold text-amber-100">
              Upload your recording
            </h2>
            <p className="text-xs text-slate-400">
              WAV, FLAC, OGG or AIFF · Maximum 20 MB · 5 minutes
            </p>
          </div>
        </div>

        <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-amber-400/30 bg-[#101D36] px-5 py-10 text-center transition hover:border-amber-300 hover:bg-[#142442]">
          <AudioLines size={38} className="mb-4 text-amber-400" />

          <span className="font-semibold text-amber-100">
            {file ? file.name : 'Choose an audio recording'}
          </span>

          <span className="mt-2 text-xs text-slate-400">
            Select an audio file from your computer
          </span>

          <input
            type="file"
            accept=".wav,.flac,.ogg,.aiff,.aif,audio/wav,audio/flac,audio/ogg"
            className="hidden"
            onChange={(event) => {
              setFile(event.target.files?.[0] || null)
              setAnalysis(null)
              setError('')
            }}
          />
        </label>

        {file && (
          <div className="mt-4 flex flex-wrap justify-between gap-2 text-xs text-slate-400">
            <span>{(file.size / (1024 * 1024)).toFixed(2)} MB</span>
            <span>{file.type || 'Audio file'}</span>
          </div>
        )}

        <div className="mt-6 max-w-sm">
          <label className="mb-2 block text-sm font-medium text-amber-100">
            Reference tonic frequency (Sa)
          </label>

          <div className="relative">
            <input
              type="number"
              min="1"
              step="0.01"
              value={tonic}
              onChange={(event) => setTonic(event.target.value)}
              className="w-full rounded-xl border border-white/10 bg-[#101A30] px-4 py-3 pr-16 text-white outline-none focus:border-amber-400"
            />

            <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">
              Hz
            </span>
          </div>

          <p className="mt-2 text-xs text-slate-500">
            Default: 261.63 Hz (approximately middle C).
            Enter the actual Sa frequency of your recording.
          </p>
        </div>

        <button
          onClick={analyzeAudio}
          disabled={loading || !file}
          className="mt-7 inline-flex items-center gap-3 rounded-full bg-gradient-to-r from-amber-300 to-amber-600 px-7 py-3 font-semibold text-slate-950 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? (
            <LoaderCircle size={19} className="animate-spin" />
          ) : (
            <Sparkles size={19} />
          )}

          {loading ? 'Analyzing recording...' : 'Analyze Audio'}
        </button>

        {error && (
          <div className="mt-5 flex items-start gap-3 rounded-xl border border-red-400/20 bg-red-500/10 p-4 text-sm text-red-300">
            <AlertCircle size={19} className="shrink-0" />
            {error}
          </div>
        )}
      </section>

      {analysis && (
        <>
          <section className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-5">
              <Activity className="mb-3 text-amber-400" />
              <p className="text-2xl font-bold text-white">
                {analysis.audio.duration_seconds}s
              </p>
              <p className="mt-1 text-sm text-slate-400">Duration</p>
            </div>

            <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-5">
              <AudioLines className="mb-3 text-amber-400" />
              <p className="text-2xl font-bold text-white">
                {analysis.pitch.average_frequency ?? '—'} Hz
              </p>
              <p className="mt-1 text-sm text-slate-400">
                Average detected pitch
              </p>
            </div>

            <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-5">
              <Music2 className="mb-3 text-amber-400" />
              <p className="text-2xl font-bold text-white">
                {analysis.swara.detected_swaras.length}
              </p>
              <p className="mt-1 text-sm text-slate-400">
                Detected swara frames
              </p>
            </div>
          </section>

          <section className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-6">
            <h2 className="mb-5 text-lg font-semibold text-amber-100">
              Audio waveform
            </h2>

            <div className="flex h-28 items-center gap-[2px] overflow-hidden">
              {analysis.audio.waveform.map((value, index) => (
                <div
                  key={index}
                  className="min-w-[2px] flex-1 rounded-full bg-gradient-to-t from-amber-700 to-amber-300"
                  style={{
                    height: `${Math.max(3, value * 100)}%`,
                  }}
                />
              ))}
            </div>
          </section>

          <section className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-6">
            <h2 className="mb-4 text-lg font-semibold text-amber-100">
              Detected swara sequence
            </h2>

            <div className="flex flex-wrap gap-2">
              {analysis.swara.detected_swaras.map((swara, index) => (
                <span
                  key={`${swara}-${index}`}
                  className="rounded-lg border border-amber-400/20 bg-amber-400/10 px-3 py-2 font-semibold text-amber-300"
                >
                  {swara}
                </span>
              ))}
            </div>
          </section>

          <section className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-6">
            <div className="mb-5 flex items-center gap-3">
              <Sparkles className="text-amber-400" />
              <h2 className="text-lg font-semibold text-amber-100">
                Raga candidates
              </h2>
            </div>

            <p className="mb-5 text-xs text-slate-400">
              Preliminary scale compatibility results. These are
              suggestions, not definitive raga identifications.
            </p>

            <div className="space-y-4">
              {analysis.raga.candidates.map((candidate, index) => (
                <div
                  key={`${candidate.name}-${index}`}
                  className="rounded-xl border border-white/10 bg-[#101A30] p-4"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <h3 className="font-semibold text-amber-100">
                      {index + 1}. {candidate.name}
                    </h3>

                    {candidate.match_percentage !== undefined && (
                      <span className="text-sm font-semibold text-amber-400">
                        {candidate.match_percentage}%
                      </span>
                    )}
                  </div>

                  {candidate.arohanam && (
                    <p className="mt-3 text-sm text-slate-300">
                      Arohanam: {candidate.arohanam}
                    </p>
                  )}

                  {candidate.avarohanam && (
                    <p className="mt-1 text-sm text-slate-300">
                      Avarohanam: {candidate.avarohanam}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  )
}

export default AudioIntelligence
