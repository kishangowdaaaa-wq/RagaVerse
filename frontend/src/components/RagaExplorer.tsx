
import { useEffect, useMemo, useState } from 'react'
import {
  Search,
  Music2,
  ArrowDown,
  ArrowUp,
  Loader2,
  Filter,
  X,
  BookOpen,
  Sparkles,
  CircleDot,
} from 'lucide-react'
import { searchRagas, type Raga } from '../services/api'

interface RagaExplorerProps {
  initialQuery?: string
}

const CHAKRAS = [
  'Indu',
  'Netra',
  'Agni',
  'Veda',
  'Bana',
  'Rutu',
  'Rishi',
  'Vasu',
  'Brahma',
  'Disi',
  'Rudra',
  'Aditya',
]

function getChakraName(number: number | null, chakra?: string) {
  if (number !== null && number >= 1 && number <= 72) {
    return CHAKRAS[Math.floor((number - 1) / 6)]
  }

  return chakra || 'Not specified'
}

function getChakraRange(index: number) {
  return {
    start: index * 6 + 1,
    end: index * 6 + 6,
  }
}

export default function RagaExplorer({
  initialQuery = '',
}: RagaExplorerProps) {
  const [query, setQuery] = useState(initialQuery)
  const [ragas, setRagas] = useState<Raga[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [category, setCategory] = useState('All')
  const [melakartaNumber, setMelakartaNumber] = useState('all')
  const [selectedChakra, setSelectedChakra] = useState<number | null>(null)
  const [selectedRaga, setSelectedRaga] = useState<Raga | null>(null)

  useEffect(() => {
    setQuery(initialQuery)
  }, [initialQuery])

  useEffect(() => {
    let active = true

    const timer = window.setTimeout(async () => {
      setLoading(true)
      setError('')

      try {
        const response = await searchRagas(query)

        if (active) {
          setRagas(response.results)
        }
      } catch {
        if (active) {
          setError('Unable to load ragas. Please check your backend connection.')
          setRagas([])
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }, 300)

    return () => {
      active = false
      window.clearTimeout(timer)
    }
  }, [query])

  const melakartaRagas = useMemo(() => {
    return ragas
      .filter(
        (raga) =>
          raga.melakarta_number !== null &&
          raga.melakarta_number >= 1 &&
          raga.melakarta_number <= 72
      )
      .sort(
        (a, b) =>
          (a.melakarta_number ?? 0) - (b.melakarta_number ?? 0)
      )
  }, [ragas])

  const filteredRagas = useMemo(() => {
    return ragas.filter((raga) => {
      const categoryText = raga.category.toLowerCase()

      const matchesCategory =
        category === 'All' ||
        (category === 'Melakarta'
          ? raga.melakarta_number !== null
          : categoryText.includes('janya'))

      const matchesNumber =
        melakartaNumber === 'all' ||
        raga.melakarta_number === Number(melakartaNumber)

      const matchesChakra =
        selectedChakra === null ||
        (raga.melakarta_number !== null &&
          Math.floor((raga.melakarta_number - 1) / 6) === selectedChakra)

      return matchesCategory && matchesNumber && matchesChakra
    })
  }, [ragas, category, melakartaNumber, selectedChakra])

  const chakraRagas = useMemo(() => {
    if (selectedChakra === null) return []

    const { start, end } = getChakraRange(selectedChakra)

    return melakartaRagas.filter(
      (raga) =>
        raga.melakarta_number !== null &&
        raga.melakarta_number >= start &&
        raga.melakarta_number <= end
    )
  }, [melakartaRagas, selectedChakra])

  const openRaga = (raga: Raga) => {
    setSelectedRaga(raga)
  }

  const clearFilters = () => {
    setQuery('')
    setCategory('All')
    setMelakartaNumber('all')
    setSelectedChakra(null)
    setSelectedRaga(null)
  }

  const showWheel =
    !query.trim() &&
    category !== 'Janya' &&
    melakartaNumber === 'all'

  return (
    <div className="min-h-screen bg-[#080f20] px-4 py-8 text-slate-100 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-7xl">

        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-amber-400/20 bg-amber-400/5 px-4 py-2 text-xs font-semibold uppercase tracking-[0.25em] text-amber-300">
            <Sparkles size={14} />
            Carnatic Music Knowledge
          </div>

          <h1 className="text-3xl font-bold tracking-wide text-white sm:text-5xl">
            Raga Explorer
          </h1>

          <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">
            Explore the 72 Melakarta ragas through their traditional
            twelve-Chakra arrangement.
          </p>
        </div>

        {/* Search */}
        <div className="mx-auto mb-6 max-w-2xl">
          <div className="flex items-center gap-3 rounded-2xl border border-slate-700 bg-[#111c32] px-4 py-3 shadow-lg shadow-black/20 focus-within:border-amber-400/60">
            <Search className="shrink-0 text-amber-300" size={20} />

            <input
              value={query}
              onChange={(event) => {
                setQuery(event.target.value)
                setSelectedRaga(null)
              }}
              placeholder="Search for a raga..."
              className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
            />

            {query && (
              <button
                onClick={() => setQuery('')}
                className="text-slate-400 transition hover:text-white"
                aria-label="Clear search"
              >
                <X size={18} />
              </button>
            )}
          </div>
        </div>

        {/* Filters */}
        <div className="mb-8 flex flex-wrap items-center justify-center gap-3">
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <Filter size={16} />
            Filters
          </div>

          <select
            value={category}
            onChange={(event) => {
              setCategory(event.target.value)
              setSelectedChakra(null)
              setSelectedRaga(null)
            }}
            className="rounded-xl border border-slate-700 bg-[#111c32] px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-amber-400"
          >
            <option value="All">All ragas</option>
            <option value="Melakarta">Melakarta</option>
            <option value="Janya">Janya</option>
          </select>

          <select
            value={melakartaNumber}
            onChange={(event) => {
              setMelakartaNumber(event.target.value)
              setSelectedRaga(null)
            }}
            className="rounded-xl border border-slate-700 bg-[#111c32] px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-amber-400"
          >
            <option value="all">All Melakarta numbers</option>
            {Array.from({ length: 72 }, (_, index) => (
              <option key={index + 1} value={index + 1}>
                Melakarta {index + 1}
              </option>
            ))}
          </select>

          <select
            value={selectedChakra === null ? 'all' : selectedChakra}
            onChange={(event) => {
              setSelectedChakra(
                event.target.value === 'all'
                  ? null
                  : Number(event.target.value)
              )
              setSelectedRaga(null)
            }}
            className="rounded-xl border border-slate-700 bg-[#111c32] px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-amber-400"
          >
            <option value="all">All Chakras</option>
            {CHAKRAS.map((chakra, index) => (
              <option key={chakra} value={index}>
                {chakra} Chakra
              </option>
            ))}
          </select>

          <button
            onClick={clearFilters}
            className="rounded-xl border border-slate-700 px-4 py-2.5 text-sm text-slate-400 transition hover:border-amber-400/50 hover:text-amber-300"
          >
            Reset
          </button>
        </div>

        {loading && (
          <div className="flex items-center justify-center gap-3 py-16 text-amber-300">
            <Loader2 className="animate-spin" size={22} />
            Loading Raga catalogue...
          </div>
        )}

        {error && (
          <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-5 text-center text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && (
          <>
            {/* Interactive Chakra Wheel */}
            {showWheel && (
              <section className="mb-12">
                <div className="mb-8 text-center">
                  <h2 className="text-xl font-semibold tracking-wide text-amber-200 sm:text-2xl">
                    The 72 Melakarta Chakra Wheel
                  </h2>
                  <p className="mt-2 text-sm text-slate-400">
                    Select any Chakra around the circle to explore its six ragas.
                  </p>
                </div>

                <div className="mx-auto max-w-[620px]">
                  <div className="relative mx-auto aspect-square w-full max-w-[560px]">

                    {/* Decorative circular rings */}
                    <svg
                      viewBox="0 0 500 500"
                      className="absolute inset-0 h-full w-full"
                      aria-hidden="true"
                    >
                      <defs>
                        <radialGradient id="wheelGlow">
                          <stop offset="0%" stopColor="#fbbf24" stopOpacity="0.12" />
                          <stop offset="100%" stopColor="#fbbf24" stopOpacity="0" />
                        </radialGradient>
                      </defs>

                      <circle
                        cx="250"
                        cy="250"
                        r="240"
                        fill="url(#wheelGlow)"
                      />

                      <circle
                        cx="250"
                        cy="250"
                        r="218"
                        fill="none"
                        stroke="#d6a94b"
                        strokeOpacity="0.65"
                        strokeWidth="1.5"
                      />

                      <circle
                        cx="250"
                        cy="250"
                        r="170"
                        fill="none"
                        stroke="#d6a94b"
                        strokeOpacity="0.3"
                        strokeWidth="1"
                        strokeDasharray="4 7"
                      />

                      <circle
                        cx="250"
                        cy="250"
                        r="112"
                        fill="none"
                        stroke="#d6a94b"
                        strokeOpacity="0.35"
                        strokeWidth="1.5"
                      />

                      {CHAKRAS.map((chakra, index) => {
                        const angle =
                          ((index * 30 - 90) * Math.PI) / 180

                        const x1 = 250 + Math.cos(angle) * 112
                        const y1 = 250 + Math.sin(angle) * 112
                        const x2 = 250 + Math.cos(angle) * 218
                        const y2 = 250 + Math.sin(angle) * 218

                        return (
                          <line
                            key={chakra}
                            x1={x1}
                            y1={y1}
                            x2={x2}
                            y2={y2}
                            stroke="#d6a94b"
                            strokeOpacity="0.25"
                            strokeWidth="1"
                          />
                        )
                      })}
                    </svg>

                    {/* Center */}
                    <div className="absolute left-1/2 top-1/2 z-10 flex h-[31%] w-[31%] -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center rounded-full border border-amber-300/60 bg-gradient-to-br from-[#26344d] to-[#111b30] text-center shadow-[0_0_45px_rgba(217,165,70,0.16)]">
                      <Music2 size={25} className="mb-1 text-amber-300 sm:size-8" />

                      <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-amber-300 sm:text-xs">
                        Melakarta
                      </span>

                      <span className="mt-1 text-2xl font-bold text-white sm:text-4xl">
                        72
                      </span>

                      <span className="mt-1 text-[9px] uppercase tracking-widest text-slate-400 sm:text-[10px]">
                        12 Chakras
                      </span>
                    </div>

                    {/* Twelve Chakra buttons */}
                    {CHAKRAS.map((chakra, index) => {
                      const angle =
                        ((index * 30 - 90) * Math.PI) / 180

                      const radius = 43.5
                      const left =
                        50 + Math.cos(angle) * radius
                      const top =
                        50 + Math.sin(angle) * radius

                      const { start, end } = getChakraRange(index)
                      const isSelected = selectedChakra === index

                      return (
                        <button
                          key={chakra}
                          onClick={() => {
                            setSelectedChakra(
                              isSelected ? null : index
                            )
                            setSelectedRaga(null)
                          }}
                          style={{
                            left: `${left}%`,
                            top: `${top}%`,
                            transform: 'translate(-50%, -50%)',
                          }}
                          className={`absolute z-20 flex h-[17%] w-[17%] flex-col items-center justify-center rounded-full border text-center transition-all duration-300 hover:scale-110 ${
                            isSelected
                              ? 'border-amber-200 bg-gradient-to-br from-amber-300 to-amber-600 text-[#101a2b] shadow-[0_0_30px_rgba(251,191,36,0.5)] scale-110'
                              : 'border-amber-400/60 bg-gradient-to-br from-[#24334d] to-[#111b30] text-amber-200 shadow-[0_5px_20px_rgba(0,0,0,0.35)] hover:border-amber-200 hover:shadow-[0_0_25px_rgba(251,191,36,0.3)]'
                          }`}
                        >
                          <span className="text-[8px] font-bold uppercase tracking-wider opacity-75 sm:text-[10px]">
                            Chakra {index + 1}
                          </span>

                          <span className="mt-0.5 text-[11px] font-bold sm:text-base">
                            {chakra}
                          </span>

                          <span className="mt-0.5 text-[8px] opacity-75 sm:text-[10px]">
                            {start}–{end}
                          </span>
                        </button>
                      )
                    })}
                  </div>
                </div>

                <div className="mt-5 text-center text-xs text-slate-500">
                  <CircleDot className="mr-1 inline text-amber-400" size={13} />
                  12 Chakras · 6 ragas per Chakra · 72 Melakarta ragas
                </div>

                {/* Selected Chakra Ragas */}
                {selectedChakra !== null && (
                  <div className="mx-auto mt-10 max-w-4xl rounded-3xl border border-amber-400/30 bg-gradient-to-br from-[#17243b] to-[#0e182b] p-5 shadow-xl shadow-black/20 sm:p-8">
                    <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-400">
                          Selected Chakra
                        </p>

                        <h3 className="mt-1 text-2xl font-bold text-white">
                          {CHAKRAS[selectedChakra]} Chakra
                        </h3>

                        <p className="mt-1 text-sm text-slate-400">
                          Melakarta numbers{' '}
                          {getChakraRange(selectedChakra).start}–
                          {getChakraRange(selectedChakra).end}
                        </p>
                      </div>

                      <button
                        onClick={() => {
                          setSelectedChakra(null)
                          setSelectedRaga(null)
                        }}
                        className="rounded-full border border-slate-600 p-2 text-slate-400 transition hover:border-amber-400 hover:text-amber-300"
                        aria-label="Close Chakra selection"
                      >
                        <X size={18} />
                      </button>
                    </div>

                    {chakraRagas.length === 0 ? (
                      <p className="rounded-xl bg-black/20 p-5 text-center text-sm text-slate-400">
                        Chakra selected. Its raga records have not loaded from the catalogue.
                      </p>
                    ) : (
                      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                        {chakraRagas.map((raga) => (
                          <button
                            key={raga.name}
                            onClick={() => openRaga(raga)}
                            className={`rounded-2xl border p-4 text-left transition-all hover:-translate-y-1 hover:border-amber-300/70 hover:bg-amber-400/10 ${
                              selectedRaga?.name === raga.name
                                ? 'border-amber-300 bg-amber-400/10'
                                : 'border-slate-700 bg-[#0d1729]'
                            }`}
                          >
                            <div className="mb-2 flex items-center justify-between">
                              <span className="text-xs font-semibold text-amber-400">
                                Melakarta {raga.melakarta_number}
                              </span>
                              <Music2 size={16} className="text-amber-300" />
                            </div>

                            <h4 className="font-semibold text-white">
                              {raga.name}
                            </h4>

                            <p className="mt-2 text-xs text-slate-400">
                              View raga details →
                            </p>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </section>
            )}

            {/* Raga Details */}
            {selectedRaga && (
              <section className="mb-8 rounded-3xl border border-amber-400/30 bg-gradient-to-br from-[#192740] to-[#101a2d] p-6 shadow-xl shadow-black/20 sm:p-8">
                <div className="mb-5 flex items-start justify-between gap-4">
                  <div>
                    <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-amber-400">
                      <BookOpen size={15} />
                      Raga Details
                    </div>

                    <h2 className="text-2xl font-bold text-white sm:text-3xl">
                      {selectedRaga.name}
                    </h2>

                    {selectedRaga.melakarta_number !== null && (
                      <p className="mt-2 text-sm text-amber-300">
                        Melakarta {selectedRaga.melakarta_number}
                        {' · '}
                        {getChakraName(
                          selectedRaga.melakarta_number,
                          selectedRaga.chakra
                        )}{' '}
                        Chakra
                      </p>
                    )}
                  </div>

                  <button
                    onClick={() => setSelectedRaga(null)}
                    className="rounded-full border border-slate-600 p-2 text-slate-400 transition hover:border-amber-400 hover:text-amber-300"
                    aria-label="Close raga details"
                  >
                    <X size={18} />
                  </button>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl border border-slate-700 bg-[#0b1527] p-5">
                    <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-emerald-300">
                      <ArrowUp size={17} />
                      Arohanam
                    </div>
                    <p className="text-lg font-medium leading-8 text-white">
                      {selectedRaga.arohanam || 'Not available'}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-700 bg-[#0b1527] p-5">
                    <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-sky-300">
                      <ArrowDown size={17} />
                      Avarohanam
                    </div>
                    <p className="text-lg font-medium leading-8 text-white">
                      {selectedRaga.avarohanam || 'Not available'}
                    </p>
                  </div>
                </div>

                <div className="mt-4 rounded-2xl border border-slate-700 bg-[#0b1527] p-5">
                  <h4 className="mb-2 text-sm font-semibold text-amber-300">
                    Characteristics
                  </h4>
                  <p className="text-sm leading-7 text-slate-300">
                    {selectedRaga.notes || 'No additional notes available.'}
                  </p>
                </div>

                {selectedRaga.aliases?.length > 0 && (
                  <div className="mt-4">
                    <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-slate-500">
                      Also known as
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {selectedRaga.aliases.map((alias) => (
                        <span
                          key={alias}
                          className="rounded-full border border-slate-700 bg-[#0b1527] px-3 py-1.5 text-xs text-slate-300"
                        >
                          {alias}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <p className="mt-5 text-xs text-slate-500">
                  Category: {selectedRaga.category}
                </p>
              </section>
            )}

            {/* Search and Filter Results */}
            {!showWheel && (
              <div className="mb-5">
                <h2 className="text-xl font-semibold text-white">
                  Raga Results
                </h2>
                <p className="mt-1 text-sm text-slate-400">
                  {filteredRagas.length} ragas found
                </p>
              </div>
            )}

            {filteredRagas.length > 0 && (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {filteredRagas.map((raga) => (
                  <button
                    key={raga.name}
                    onClick={() => openRaga(raga)}
                    className={`rounded-2xl border p-5 text-left transition-all hover:-translate-y-1 hover:border-amber-400/60 hover:bg-[#17243b] ${
                      selectedRaga?.name === raga.name
                        ? 'border-amber-400 bg-[#17243b]'
                        : 'border-slate-700 bg-[#111c32]'
                    }`}
                  >
                    <div className="mb-3 flex items-center justify-between">
                      <span className="rounded-full border border-amber-400/20 bg-amber-400/10 px-3 py-1 text-xs font-medium text-amber-300">
                        {raga.category}
                      </span>
                      <Music2 size={18} className="text-amber-300" />
                    </div>

                    <h3 className="text-lg font-semibold text-white">
                      {raga.name}
                    </h3>

                    {raga.melakarta_number !== null && (
                      <p className="mt-2 text-xs text-amber-300">
                        Melakarta {raga.melakarta_number}
                        {' · '}
                        {getChakraName(
                          raga.melakarta_number,
                          raga.chakra
                        )}{' '}
                        Chakra
                      </p>
                    )}

                    <p className="mt-3 line-clamp-2 text-sm leading-6 text-slate-400">
                      {raga.notes}
                    </p>

                    <p className="mt-4 text-xs font-semibold text-amber-300">
                      Explore raga →
                    </p>
                  </button>
                ))}
              </div>
            )}

            {filteredRagas.length === 0 && (
              <div className="rounded-2xl border border-slate-700 bg-[#111c32] px-5 py-14 text-center">
                <Music2 className="mx-auto mb-4 text-slate-500" size={32} />
                <h3 className="text-lg font-semibold text-white">
                  No ragas found
                </h3>
                <p className="mt-2 text-sm text-slate-400">
                  Try a different search term or clear your filters.
                </p>
                <button
                  onClick={clearFilters}
                  className="mt-5 rounded-xl bg-amber-400 px-5 py-2.5 text-sm font-semibold text-[#101a2b] transition hover:bg-amber-300"
                >
                  Clear filters
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
