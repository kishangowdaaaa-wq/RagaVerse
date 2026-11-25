
import { useEffect, useMemo, useState } from 'react'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock3,
  GraduationCap,
  Loader2,
  Music2,
  Search,
  Sparkles,
} from 'lucide-react'

import {
  getLearningModules,
} from '../services/api'

import type {
  LearningModule,
  LearningLesson,
} from '../services/api'


const moduleIcons = [
  Music2,
  BookOpen,
  GraduationCap,
  Sparkles,
  Music2,
  Clock3,
  BookOpen,
]

const moduleAccents = [
  'from-amber-500/20 to-orange-500/5',
  'from-blue-500/20 to-cyan-500/5',
  'from-purple-500/20 to-indigo-500/5',
  'from-emerald-500/20 to-teal-500/5',
  'from-rose-500/20 to-pink-500/5',
  'from-cyan-500/20 to-blue-500/5',
  'from-orange-500/20 to-amber-500/5',
]


function MusicLearning() {
  const [modules, setModules] = useState<LearningModule[]>([])
  const [selectedModule, setSelectedModule] =
    useState<LearningModule | null>(null)

  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [completedLessons, setCompletedLessons] =
    useState<string[]>([])

  useEffect(() => {
    let active = true

    async function loadModules() {
      try {
        setLoading(true)
        setError('')

        const response = await getLearningModules()

        if (active) {
          setModules(response.results)
        }
      } catch (err) {
        if (active) {
          setError(
            err instanceof Error
              ? err.message
              : 'Unable to load learning modules.'
          )
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadModules()

    return () => {
      active = false
    }
  }, [])

  const filteredModules = useMemo(() => {
    const term = search.trim().toLowerCase()

    if (!term) return modules

    return modules.filter((module) =>
      module.title.toLowerCase().includes(term) ||
      module.description.toLowerCase().includes(term) ||
      module.lessons.some((lesson) =>
        lesson.title.toLowerCase().includes(term)
      )
    )
  }, [modules, search])

  const toggleLesson = (lessonId: string) => {
    setCompletedLessons((previous) =>
      previous.includes(lessonId)
        ? previous.filter((id) => id !== lessonId)
        : [...previous, lessonId]
    )
  }

  const getModuleProgress = (module: LearningModule) => {
    const completed = module.lessons.filter((lesson) =>
      completedLessons.includes(`${module.id}:${lesson.id}`)
    ).length

    return {
      completed,
      total: module.lessons.length,
      percentage: module.lessons.length
        ? Math.round((completed / module.lessons.length) * 100)
        : 0,
    }
  }

  const getLessonKey = (
    module: LearningModule,
    lesson: LearningLesson
  ) => `${module.id}:${lesson.id}`

  return (
    <div className="space-y-8 pb-10">

      {/* Page heading */}
      <section>
        <p className="text-xs font-semibold uppercase tracking-[0.25em] text-amber-400">
          Explore · Learn · Master
        </p>

        <h1 className="mt-3 text-3xl font-bold text-amber-100 sm:text-4xl">
          Music Learning Academy
        </h1>

        <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400">
          Build your Carnatic music foundation through structured
          lessons, musical exercises and guided learning.
        </p>
      </section>

      {/* Statistics */}
      <section className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-5">
          <BookOpen className="mb-3 text-amber-400" size={24} />
          <p className="text-3xl font-bold text-white">
            {modules.length}
          </p>
          <p className="mt-1 text-sm text-slate-400">
            Learning modules
          </p>
        </div>

        <div className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-5">
          <GraduationCap className="mb-3 text-amber-400" size={24} />
          <p className="text-3xl font-bold text-white">
            {modules.reduce(
              (total, module) => total + module.lessons.length,
              0
            )}
          </p>
          <p className="mt-1 text-sm text-slate-400">
            Available lessons
          </p>
        </div>

        <div className="col-span-2 rounded-2xl border border-amber-500/20 bg-[#0D172D] p-5 sm:col-span-1">
          <CheckCircle2 className="mb-3 text-emerald-400" size={24} />
          <p className="text-3xl font-bold text-white">
            {completedLessons.length}
          </p>
          <p className="mt-1 text-sm text-slate-400">
            Lessons completed
          </p>
        </div>
      </section>

      {selectedModule ? (
        /* Selected module details */
        <section className="space-y-6">

          <button
            onClick={() => setSelectedModule(null)}
            className="inline-flex items-center gap-2 text-sm font-semibold text-amber-400 transition hover:text-amber-200"
          >
            <ArrowLeft size={17} />
            Back to all modules
          </button>

          <div className="rounded-3xl border border-amber-500/20 bg-gradient-to-br from-[#172344] to-[#0D172D] p-6 sm:p-8">
            <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1 text-xs font-semibold text-amber-300">
              {selectedModule.level}
            </span>

            <h2 className="mt-5 text-3xl font-bold text-amber-100">
              {selectedModule.title}
            </h2>

            <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-300">
              {selectedModule.description}
            </p>

            <div className="mt-5 flex flex-wrap gap-5 text-sm text-slate-400">
              <span className="flex items-center gap-2">
                <BookOpen size={16} className="text-amber-400" />
                {selectedModule.lessons.length} lessons
              </span>

              <span className="flex items-center gap-2">
                <Clock3 size={16} className="text-amber-400" />
                {selectedModule.lessons.reduce(
                  (total, lesson) =>
                    total + lesson.duration_minutes,
                  0
                )} minutes
              </span>
            </div>

            {selectedModule.prerequisites.length > 0 && (
              <div className="mt-6">
                <p className="text-xs font-semibold uppercase tracking-wider text-amber-400">
                  Prerequisites
                </p>

                <div className="mt-2 flex flex-wrap gap-2">
                  {selectedModule.prerequisites.map((item) => (
                    <span
                      key={item}
                      className="rounded-full bg-white/5 px-3 py-2 text-xs text-slate-300"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Module progress */}
          {(() => {
            const progress = getModuleProgress(selectedModule)

            return (
              <div className="rounded-2xl border border-white/10 bg-[#0D172D] p-5">
                <div className="mb-3 flex justify-between text-sm">
                  <span className="font-medium text-white">
                    Your learning progress
                  </span>
                  <span className="font-semibold text-amber-400">
                    {progress.percentage}%
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-white/10">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-amber-400 to-amber-600 transition-all"
                    style={{ width: `${progress.percentage}%` }}
                  />
                </div>
              </div>
            )
          })()}

          {/* Lessons */}
          <div>
            <h3 className="mb-4 text-xl font-semibold text-amber-100">
              Lessons in this module
            </h3>

            <div className="space-y-3">
              {selectedModule.lessons.map((lesson, index) => {
                const lessonKey = getLessonKey(
                  selectedModule,
                  lesson
                )

                const completed =
                  completedLessons.includes(lessonKey)

                return (
                  <article
                    key={lesson.id}
                    className="rounded-2xl border border-white/10 bg-[#0D172D] p-5 transition hover:border-amber-500/30"
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-amber-400/10 font-bold text-amber-400">
                        {completed ? (
                          <CheckCircle2 size={22} />
                        ) : (
                          String(index + 1).padStart(2, '0')
                        )}
                      </div>

                      <div className="min-w-0 flex-1">
                        <h4 className="font-semibold text-white">
                          {lesson.title}
                        </h4>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                          {lesson.summary}
                        </p>

                        <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
                          <Clock3 size={14} />
                          {lesson.duration_minutes} minutes
                        </div>
                      </div>

                      <button
                        onClick={() => toggleLesson(lessonKey)}
                        className={`shrink-0 rounded-full px-3 py-2 text-xs font-semibold transition ${
                          completed
                            ? 'bg-emerald-500/15 text-emerald-300'
                            : 'border border-amber-500/30 text-amber-400 hover:bg-amber-400 hover:text-slate-950'
                        }`}
                      >
                        {completed ? 'Completed' : 'Mark done'}
                      </button>
                    </div>
                  </article>
                )
              })}
            </div>
          </div>
        </section>
      ) : (
        /* Module catalogue */
        <>
          <div className="relative max-w-xl">
            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              type="search"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search learning modules or lessons..."
              className="w-full rounded-full border border-white/10 bg-[#101A30] py-3 pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-amber-400"
            />
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 text-slate-400">
              <Loader2 className="mb-4 animate-spin text-amber-400" size={34} />
              Loading learning modules...
            </div>
          ) : error ? (
            <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-6 text-center">
              <p className="font-semibold text-red-300">
                Unable to load learning modules
              </p>

              <p className="mt-2 text-sm text-slate-400">
                {error}
              </p>

              <button
                onClick={() => window.location.reload()}
                className="mt-4 rounded-full bg-amber-400 px-5 py-2 text-sm font-semibold text-slate-950"
              >
                Retry
              </button>
            </div>
          ) : filteredModules.length === 0 ? (
            <div className="rounded-2xl border border-white/10 bg-[#0D172D] p-10 text-center text-slate-400">
              No learning modules found.
            </div>
          ) : (
            <section className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
              {filteredModules.map((module) => {
                const originalIndex = modules.findIndex(
                  (item) => item.id === module.id
                )

                const Icon =
                  moduleIcons[originalIndex % moduleIcons.length]

                const progress = getModuleProgress(module)

                return (
                  <article
                    key={module.id}
                    className={`group flex flex-col rounded-2xl border border-amber-500/15 bg-gradient-to-br ${moduleAccents[originalIndex % moduleAccents.length]} p-5 transition duration-300 hover:-translate-y-1 hover:border-amber-400/50`}
                  >
                    <div className="mb-5 flex items-start justify-between">
                      <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-amber-400/20 bg-[#101B35] text-amber-400">
                        <Icon size={25} />
                      </div>

                      <span className="rounded-full border border-amber-400/20 bg-amber-400/10 px-3 py-1 text-xs font-medium text-amber-300">
                        {module.level}
                      </span>
                    </div>

                    <h3 className="text-xl font-semibold text-amber-100">
                      {module.title}
                    </h3>

                    <p className="mt-3 min-h-16 text-sm leading-6 text-slate-400">
                      {module.description}
                    </p>

                    <div className="mt-5 flex items-center gap-4 text-xs text-slate-400">
                      <span className="flex items-center gap-1.5">
                        <BookOpen size={15} className="text-amber-400" />
                        {module.lessons.length} lessons
                      </span>

                      <span className="flex items-center gap-1.5">
                        <Clock3 size={15} className="text-amber-400" />
                        {module.lessons.reduce(
                          (total, lesson) =>
                            total + lesson.duration_minutes,
                          0
                        )} min
                      </span>
                    </div>

                    <div className="mt-5">
                      <div className="mb-2 flex justify-between text-xs">
                        <span className="text-slate-500">
                          Progress
                        </span>
                        <span className="text-amber-400">
                          {progress.completed}/{progress.total}
                        </span>
                      </div>

                      <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
                        <div
                          className="h-full rounded-full bg-amber-400 transition-all"
                          style={{ width: `${progress.percentage}%` }}
                        />
                      </div>
                    </div>

                    <button
                      onClick={() => setSelectedModule(module)}
                      className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-300 to-amber-600 py-3 text-sm font-semibold text-slate-950 transition hover:brightness-110"
                    >
                      Explore module
                      <ArrowRight size={17} />
                    </button>
                  </article>
                )
              })}
            </section>
          )}
        </>
      )}
    </div>
  )
}

export default MusicLearning
