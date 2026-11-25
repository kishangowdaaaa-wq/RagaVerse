
import { useEffect, useState } from 'react'
import type { LucideIcon } from 'lucide-react'
import { AIAssistant } from './components/AIAssistant'
import RagaExplorer from './components/RagaExplorer'
import MusicLearning from './components/MusicLearning'
import AudioIntelligence from './components/AudioIntelligence'

import {
  Home,
  Sparkles,
  Music2,
  CalendarDays,
  Library,
  UserRound,
  Settings,
  Bell,
  Search,
  ArrowRight,
  Play,
  BookOpen,
  Trophy,
  Flame,
  AudioLines,
  Headphones,
  Menu,
  ChevronDown,
  ChartNoAxesCombined,
} from 'lucide-react'

type ConnectionStatus = 'loading' | 'connected' | 'failed'

type Page =
  | 'Home'
  | 'AI Assistant'
  | 'Raga Explorer'
  | 'Music Learning'
  | 'Audio Intelligence'

type Feature = {
  title: string
  description: string
  action: string
  icon: LucideIcon
  accent: string
}

const navigation = [
  { label: 'Home', icon: Home },
  { label: 'AI Assistant', icon: Sparkles },
  { label: 'Raga Explorer', icon: Music2 },
  { label: 'Music Learning', icon: BookOpen },
  { label: 'Audio Intelligence', icon: AudioLines },
  { label: 'Practice Planner', icon: CalendarDays },
  { label: 'My Library', icon: Library },
]

const features: Feature[] = [
  {
    title: 'AI Music Assistant',
    description: 'Learn ragas, understand compositions and explore Carnatic music with AI.',
    action: 'Chat Now',
    icon: Sparkles,
    accent: 'from-amber-500/20 to-blue-500/10',
  },
  {
    title: 'Raga Explorer',
    description: 'Discover ragas, arohanam, avarohanam and their musical characteristics.',
    action: 'Explore Ragas',
    icon: Music2,
    accent: 'from-blue-500/20 to-amber-500/10',
  },
  {
    title: 'Vocal Practice',
    description: 'Improve your singing with pitch awareness and practice feedback.',
    action: 'Start Practice',
    icon: AudioLines,
    accent: 'from-amber-500/20 to-purple-500/10',
  },
  {
    title: 'Practice Planner',
    description: 'Organise your musical journey with structured daily goals.',
    action: 'Plan Now',
    icon: CalendarDays,
    accent: 'from-blue-500/20 to-amber-500/10',
  },
]

const lessons = [
  { title: 'Shankarabharanam', subtitle: 'Raga fundamentals', duration: '5 min' },
  { title: 'Thodi', subtitle: 'Signature phrases', duration: '6 min' },
  { title: 'Varnam practice', subtitle: 'Musical exercises', duration: '8 min' },
]

function App() {
  const [connection, setConnection] = useState<ConnectionStatus>(
    import.meta.env.VITE_API_BASE_URL ? 'loading' : 'failed'
  )

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [activePage, setActivePage] = useState<Page>('Home')
  const [globalSearch, setGlobalSearch] = useState('')

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_BASE_URL

    if (!apiUrl) return

    const controller = new AbortController()

    fetch(`${apiUrl}/`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Backend request failed')
        }

        setConnection('connected')
      })
      .catch((error: Error) => {
        if (error.name !== 'AbortError') {
          setConnection('failed')
        }
      })

    return () => {
      controller.abort()
    }
  }, [])

  const openPage = (page: Page) => {
    setActivePage(page)
    setMobileMenuOpen(false)
  }

  return (
    <div className="min-h-screen bg-[#050B1B] text-white">

      {/* Mobile navigation */}
      <div className="flex items-center justify-between border-b border-amber-500/20 p-4 lg:hidden">
        <div className="flex items-center gap-2 text-2xl font-bold text-amber-400">
          <Music2 size={25} />
          RagaVerse
        </div>

        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="rounded-lg border border-amber-500/30 p-2"
          aria-label="Toggle navigation"
        >
          <Menu />
        </button>
      </div>

      <div className="flex min-h-screen">

        {/* Sidebar */}
        <aside
          className={`${
            mobileMenuOpen ? 'flex' : 'hidden'
          } absolute z-20 min-h-screen w-64 flex-col border-r border-amber-500/20 bg-[#080F24] p-5 lg:relative lg:flex`}
        >
          <div className="mb-12 flex items-center gap-3 px-2">
            <Music2 size={34} className="text-amber-400" />
            <span className="text-3xl font-bold tracking-tight text-amber-400">
              RagaVerse
            </span>
          </div>

          <p className="mb-4 px-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
            Workspace
          </p>

          <nav className="flex flex-col gap-2">
            {navigation.map((item) => {
              const Icon = item.icon
              const isActive = item.label === activePage

              return (
                <button
                  key={item.label}
                  onClick={() => {
                    if (
                      item.label === 'Home' ||
                      item.label === 'AI Assistant' ||
                      item.label === 'Raga Explorer' ||
                      item.label === 'Music Learning' ||
                      item.label === 'Audio Intelligence'
                    ) {
                      openPage(item.label as Page)
                    } else {
                      setMobileMenuOpen(false)
                    }
                  }}
                  className={`flex items-center gap-3 rounded-xl px-4 py-3 text-left transition ${
                    isActive
                      ? 'bg-gradient-to-r from-amber-300 to-amber-600 font-semibold text-slate-950'
                      : 'text-slate-300 hover:bg-white/5 hover:text-amber-300'
                  }`}
                >
                  <Icon size={19} />
                  <span>{item.label}</span>
                </button>
              )
            })}
          </nav>

          <div className="mt-8 border-t border-white/10 pt-6">
            <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-slate-300 hover:bg-white/5">
              <UserRound size={19} />
              Profile
            </button>

            <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-slate-300 hover:bg-white/5">
              <Settings size={19} />
              Settings
            </button>
          </div>

          <div className="mt-auto rounded-2xl border border-amber-500/20 bg-gradient-to-br from-amber-500/10 to-blue-900/20 p-4">
            <Music2 className="mb-3 text-amber-400" size={27} />
            <p className="font-semibold text-amber-200">
              Music is a journey.
            </p>
            <p className="mt-1 text-sm text-slate-400">
              Keep learning. Keep practising. Keep evolving.
            </p>
          </div>
        </aside>

        {/* Main content */}
        <main className="min-w-0 flex-1 px-4 py-5 sm:px-7 lg:px-9">

          {/* Top bar */}
          <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
            <div className="relative w-full max-w-md">
              <Search
                size={19}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <input
                type="search"
                value={globalSearch}
                onChange={(e) => setGlobalSearch(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    openPage('Raga Explorer')
                  }
                }}
                placeholder="Search ragas, compositions..."
                className="w-full rounded-full border border-white/15 bg-[#101A30] py-3 pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-amber-400"
              />
            </div>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-xs">
                <span
                  className={`h-2.5 w-2.5 rounded-full ${
                    connection === 'connected'
                      ? 'bg-emerald-400'
                      : connection === 'loading'
                        ? 'bg-amber-400'
                        : 'bg-red-400'
                  }`}
                />

                <span className="text-slate-400">
                  {connection === 'connected'
                    ? 'Backend connected'
                    : connection === 'loading'
                      ? 'Connecting...'
                      : 'Backend offline'}
                </span>
              </div>

              <button
                className="text-amber-300 transition hover:text-amber-200"
                aria-label="Notifications"
              >
                <Bell size={21} />
              </button>

              <div className="flex items-center gap-2">
                <div className="flex h-9 w-9 items-center justify-center rounded-full border border-amber-400/50 bg-gradient-to-br from-amber-300 to-amber-700 font-bold text-slate-950">
                  R
                </div>
                <span className="hidden text-sm sm:block">Musician</span>
                <ChevronDown size={15} className="text-slate-400" />
              </div>
            </div>
          </header>

          {/* Page content */}
          {activePage === 'AI Assistant' ? (
            <AIAssistant />
          ) : activePage === 'Raga Explorer' ? (
            <RagaExplorer initialQuery={globalSearch} />
          ) : activePage === 'Music Learning' ? (
            <MusicLearning />
          ) : activePage === 'Audio Intelligence' ? (
            <AudioIntelligence />
          ) : (
            <>
              {/* Hero section */}
              <section className="relative mb-9 overflow-hidden rounded-3xl border border-amber-500/25 bg-gradient-to-br from-[#111D3B] via-[#0C1730] to-[#101126] p-7 sm:p-10 lg:p-12">
                <div className="pointer-events-none absolute -right-12 -top-24 h-80 w-80 rounded-full border border-amber-400/10" />
                <div className="pointer-events-none absolute -right-4 -top-16 h-64 w-64 rounded-full border border-amber-400/10" />

                <div className="relative z-10 max-w-2xl">
                  <p className="mb-4 text-xs font-semibold uppercase tracking-[0.3em] text-amber-400">
                    Explore Â· Learn Â· Practice Â· Evolve
                  </p>

                  <h1 className="font-serif text-5xl font-bold tracking-tight text-amber-300 sm:text-7xl">
                    RagaVerse
                  </h1>

                  <h2 className="mt-4 text-xl font-medium text-amber-100 sm:text-2xl">
                    Your Intelligent Carnatic Music Companion
                  </h2>

                  <p className="mt-4 max-w-lg text-sm leading-7 text-slate-300 sm:text-base">
                    Discover the timeless beauty of Carnatic music
                    with the power of artificial intelligence.
                    Learn, explore and deepen your musical journey.
                  </p>

                  <button
                    onClick={() => openPage('AI Assistant')}
                    className="mt-7 inline-flex items-center gap-3 rounded-full bg-gradient-to-r from-amber-300 to-amber-600 px-7 py-3.5 font-semibold text-slate-950 shadow-lg shadow-amber-900/20 transition hover:scale-[1.02]"
                  >
                    <Play size={17} fill="currentColor" />
                    Start Your Musical Journey
                    <ArrowRight size={18} />
                  </button>
                </div>

                <div className="pointer-events-none absolute bottom-8 right-12 hidden items-center justify-center lg:flex">
                  <div className="flex h-52 w-52 items-center justify-center rounded-full border border-amber-400/20 bg-amber-400/5">
                    <div className="flex h-40 w-40 items-center justify-center rounded-full border border-amber-400/20">
                      <Music2 size={100} strokeWidth={0.8} className="text-amber-400/70" />
                    </div>
                  </div>
                </div>
              </section>

              {/* Feature cards */}
              <section className="mb-10">
                <div className="mb-5 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-400">
                      Discover
                    </p>
                    <h2 className="mt-1 text-2xl font-semibold text-white">
                      Explore RagaVerse
                    </h2>
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
                  {features.map((feature) => {
                    const Icon = feature.icon

                    return (
                      <article
                        key={feature.title}
                        className={`group rounded-2xl border border-amber-500/20 bg-gradient-to-br ${feature.accent} p-5 transition duration-300 hover:-translate-y-1 hover:border-amber-400/60`}
                      >
                        <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-400/20 bg-[#101B35] text-amber-400">
                          <Icon size={25} />
                        </div>

                        <h3 className="text-lg font-semibold text-amber-100">
                          {feature.title}
                        </h3>

                        <p className="mt-2 min-h-16 text-sm leading-6 text-slate-400">
                          {feature.description}
                        </p>

                        <button
                          onClick={() => {
                            if (feature.title === 'AI Music Assistant') {
                              openPage('AI Assistant')
                            } else if (feature.title === 'Raga Explorer') {
                              openPage('Raga Explorer')
                            } else if (feature.title === 'Vocal Practice') {
                              openPage('Audio Intelligence')
                            }
                          }}
                          className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-amber-400 transition group-hover:text-amber-200"
                        >
                          {feature.action}
                          <ArrowRight size={16} />
                        </button>
                      </article>
                    )
                  })}
                </div>
              </section>

              {/* Dashboard section */}
              <section className="grid grid-cols-1 gap-5 xl:grid-cols-3">

                {/* Welcome and statistics */}
                <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-6 xl:col-span-2">
                  <div className="flex items-center gap-3">
                    <Sparkles size={25} className="text-amber-400" />
                    <div>
                      <h2 className="text-xl font-semibold text-amber-100">
                        Welcome to your musical journey!
                      </h2>
                      <p className="mt-1 text-sm text-slate-400">
                        Every practice brings you closer to mastery.
                      </p>
                    </div>
                  </div>

                  <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
                    <div className="rounded-xl bg-[#14223D] p-4">
                      <Music2 className="mb-3 text-amber-400" />
                      <p className="text-3xl font-bold text-white">12</p>
                      <p className="mt-1 text-sm text-slate-400">
                        Ragas explored
                      </p>
                    </div>

                    <div className="rounded-xl bg-[#14223D] p-4">
                      <Flame className="mb-3 text-amber-400" />
                      <p className="text-3xl font-bold text-white">8</p>
                      <p className="mt-1 text-sm text-slate-400">
                        Practice sessions
                      </p>
                    </div>

                    <div className="rounded-xl bg-[#14223D] p-4">
                      <Trophy className="mb-3 text-amber-400" />
                      <p className="text-3xl font-bold text-white">85%</p>
                      <p className="mt-1 text-sm text-slate-400">
                        Goal progress
                      </p>
                    </div>
                  </div>
                </div>

                {/* Quick access */}
                <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-6">
                  <div className="mb-5 flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-amber-100">
                      Quick Access
                    </h2>
                    <BookOpen size={20} className="text-amber-400" />
                  </div>

                  <div className="space-y-5">
                    {lessons.map((lesson) => (
                      <div
                        key={lesson.title}
                        className="flex items-center gap-3"
                      >
                        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-amber-500/30 to-blue-900/50 text-amber-300">
                          <Headphones size={20} />
                        </div>

                        <div className="min-w-0 flex-1">
                          <p className="truncate text-sm font-medium text-white">
                            {lesson.title}
                          </p>
                          <p className="text-xs text-slate-400">
                            {lesson.subtitle} Â· {lesson.duration}
                          </p>
                        </div>

                        <button
                          aria-label={`Play ${lesson.title}`}
                          className="rounded-full border border-amber-500/40 p-2 text-amber-400 hover:bg-amber-400 hover:text-slate-950"
                        >
                          <Play size={13} fill="currentColor" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </section>

              {/* Progress and quote */}
              <section className="mt-5 grid grid-cols-1 gap-5 lg:grid-cols-2">
                <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-6">
                  <div className="mb-6 flex items-center gap-3">
                    <ChartNoAxesCombined className="text-amber-400" />
                    <h2 className="text-lg font-semibold text-amber-100">
                      Your Musical Progress
                    </h2>
                  </div>

                  <div className="flex h-28 items-end justify-around gap-3">
                    {[35, 55, 45, 70, 60, 90, 78].map((height, index) => (
                      <div
                        key={index}
                        className="w-full rounded-t-lg bg-gradient-to-t from-amber-700 to-amber-300 transition hover:from-amber-500"
                        style={{ height: `${height}%` }}
                      />
                    ))}
                  </div>

                  <p className="mt-4 text-center text-xs text-slate-500">
                    Weekly practice activity Â· Sample visualization
                  </p>
                </div>

                <div className="relative overflow-hidden rounded-2xl border border-amber-500/20 bg-gradient-to-br from-[#172344] to-[#0D172D] p-6">
                  <div className="absolute -right-5 -top-5 opacity-10">
                    <Music2 size={140} className="text-amber-300" />
                  </div>

                  <p className="text-4xl font-serif text-amber-400">â€œ</p>

                  <blockquote className="relative z-10 font-serif text-xl italic leading-8 text-amber-100">
                    Music is the divine language that brings the soul closer to the infinite.
                  </blockquote>

                  <p className="mt-4 text-sm text-amber-400">
                    â€” A celebration of Carnatic music
                  </p>
                </div>
              </section>

              {/* Footer */}
              <footer className="mt-10 border-t border-white/10 py-6 text-center text-xs text-slate-500">
                RagaVerse Â· Explore. Learn. Practice. Evolve.
              </footer>
            </>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
