
import { useEffect, useState } from "react"
import type { FormEvent } from "react"
import {
  Bot, Sparkles, Send, Plus, Music2, BookOpen, Mic2,
  Lightbulb, MessageCircle, LogIn, LogOut, Trash2,
  MessageSquare, Loader2, UserPlus,
} from "lucide-react"
import {
  login,
  registerUser,
  getConversations,
  createConversation,
  getConversation,
  sendChatMessage,
  deleteConversation,
} from "../services/api"
import type { Conversation, ChatMessage } from "../services/api"

const suggestions = [
  { icon: Music2, title: "Explore a Raga", prompt: "Explain the raga Shankarabharanam." },
  { icon: BookOpen, title: "Learn Music Theory", prompt: "What are arohanam and avarohanam?" },
  { icon: Mic2, title: "Vocal Practice", prompt: "How should I practise sarali varisai?" },
  { icon: Lightbulb, title: "Understand a Composition", prompt: "Explain the structure of a Carnatic kriti." },
]

type AuthMode = "login" | "register"

export function AIAssistant() {
  const [token, setToken] = useState<string | null>(
    () => sessionStorage.getItem("ragaverse_token")
  )
  const [authMode, setAuthMode] = useState<AuthMode>("login")
  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversation, setActiveConversation] = useState<number | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!token) return

    let cancelled = false

    getConversations(token)
      .then((data) => {
        if (!cancelled) setConversations(data)
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setError(err.message)
          sessionStorage.removeItem("ragaverse_token")
          setToken(null)
        }
      })
      .finally(() => {
        if (!cancelled) setLoadingHistory(false)
      })

    return () => {
      cancelled = true
    }
  }, [token])

  async function handleRegister(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError("")
    setSuccessMessage("")

    const trimmedName = fullName.trim()
    const trimmedEmail = email.trim()

    if (trimmedName.length < 2 || trimmedName.length > 100) {
      setError("Full name must contain between 2 and 100 characters.")
      return
    }

    if (password.length < 8 || password.length > 128) {
      setError("Password must contain between 8 and 128 characters.")
      return
    }

    setLoading(true)

    try {
      await registerUser(trimmedName, trimmedEmail, password)

      setEmail(trimmedEmail)
      setPassword("")
      setFullName("")
      setAuthMode("login")
      setSuccessMessage(
        "Account created successfully! Please sign in with your new account."
      )
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Account registration failed."
      )
    } finally {
      setLoading(false)
    }
  }

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError("")
    setSuccessMessage("")
    setLoading(true)

    try {
      const result = await login(email.trim(), password)
      sessionStorage.setItem("ragaverse_token", result.access_token)
      setToken(result.access_token)
      setPassword("")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed.")
    } finally {
      setLoading(false)
    }
  }

  function handleLogout() {
    sessionStorage.removeItem("ragaverse_token")
    setToken(null)
    setConversations([])
    setActiveConversation(null)
    setMessages([])
    setError("")
    setSuccessMessage("")
    setAuthMode("login")
  }

  function startNewChat() {
    setActiveConversation(null)
    setMessages([])
    setInput("")
    setError("")
  }

  async function openConversation(id: number) {
    if (!token) return

    setLoadingHistory(true)
    setError("")

    try {
      const conversation = await getConversation(token, id)
      setActiveConversation(id)
      setMessages(conversation.messages)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Could not load conversation."
      )
    } finally {
      setLoadingHistory(false)
    }
  }

  async function handleDeleteConversation(id: number) {
    if (!token) return

    try {
      await deleteConversation(token, id)
      setConversations((current) =>
        current.filter((item) => item.id !== id)
      )

      if (activeConversation === id) {
        startNewChat()
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Could not delete conversation."
      )
    }
  }

  async function sendMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const content = input.trim()

    if (!content || !token || loading) return

    setError("")
    setInput("")
    setLoading(true)

    const temporaryMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content,
      created_at: new Date().toISOString(),
    }

    setMessages((current) => [...current, temporaryMessage])

    try {
      let conversationId = activeConversation

      if (!conversationId) {
        const conversation = await createConversation(
          token,
          content.length > 45 ? `${content.slice(0, 45)}...` : content
        )

        conversationId = conversation.id
        setActiveConversation(conversation.id)
        setConversations((current) => [conversation, ...current])
      }

      const result = await sendChatMessage(token, conversationId, content)

      setMessages((current) => [
        ...current.filter(
          (message) => message.id !== temporaryMessage.id
        ),
        result.user_message,
        result.assistant_message,
      ])

      const updated = await getConversations(token)
      setConversations(updated)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to get an AI response."
      )
    } finally {
      setLoading(false)
    }
  }

  if (!token) {
    return (
      <section className="flex min-h-[calc(100vh-150px)] items-center justify-center">
        <div className="w-full max-w-md rounded-2xl border border-amber-500/20 bg-[#0D172D] p-7 sm:p-9">
          <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border border-amber-400/30 bg-amber-400/10">
            <Sparkles size={32} className="text-amber-400" />
          </div>

          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-400">
            Your Musical Companion
          </p>

          <h1 className="mt-2 text-3xl font-bold text-amber-100">
            {authMode === "login" ? "Welcome to RagaVerse" : "Join RagaVerse"}
          </h1>

          <p className="mt-3 text-sm leading-6 text-slate-400">
            {authMode === "login"
              ? "Sign in to start conversations with your AI Carnatic music assistant."
              : "Create your account and begin your Carnatic music journey."}
          </p>

          <form
            onSubmit={authMode === "login" ? handleLogin : handleRegister}
            className="mt-7 space-y-4"
          >
            {authMode === "register" && (
              <div>
                <label className="mb-2 block text-sm text-amber-200">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  minLength={2}
                  maxLength={100}
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  placeholder="Your full name"
                  className="w-full rounded-xl border border-amber-500/20 bg-[#101B35] px-4 py-3 text-sm text-white outline-none focus:border-amber-400"
                />
              </div>
            )}

            <div>
              <label className="mb-2 block text-sm text-amber-200">
                Email
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                className="w-full rounded-xl border border-amber-500/20 bg-[#101B35] px-4 py-3 text-sm text-white outline-none focus:border-amber-400"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-amber-200">
                Password
              </label>
              <input
                type="password"
                required
                minLength={8}
                maxLength={128}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Enter your password"
                className="w-full rounded-xl border border-amber-500/20 bg-[#101B35] px-4 py-3 text-sm text-white outline-none focus:border-amber-400"
              />
              {authMode === "register" && (
                <p className="mt-2 text-xs text-slate-500">
                  Password must contain 8–128 characters.
                </p>
              )}
            </div>

            {successMessage && (
              <p className="rounded-lg border border-green-500/30 bg-green-500/10 p-3 text-sm text-green-300">
                {successMessage}
              </p>
            )}

            {error && (
              <p className="rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-300 to-amber-600 px-5 py-3 font-semibold text-slate-950 transition hover:brightness-110 disabled:opacity-50"
            >
              {loading ? (
                <Loader2 size={18} className="animate-spin" />
              ) : authMode === "login" ? (
                <LogIn size={18} />
              ) : (
                <UserPlus size={18} />
              )}

              {loading
                ? "Please wait..."
                : authMode === "login"
                  ? "Sign In"
                  : "Create Account"}
            </button>
          </form>

          <div className="mt-6 border-t border-white/10 pt-5 text-center">
            <p className="text-sm text-slate-400">
              {authMode === "login"
                ? "Don't have an account?"
                : "Already have an account?"}
            </p>

            <button
              type="button"
              disabled={loading}
              onClick={() => {
                setAuthMode(
                  authMode === "login" ? "register" : "login"
                )
                setError("")
                setSuccessMessage("")
                setPassword("")
              }}
              className="mt-2 text-sm font-semibold text-amber-400 transition hover:text-amber-200 disabled:opacity-50"
            >
              {authMode === "login"
                ? "Create a new account"
                : "Sign in instead"}
            </button>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="flex min-h-[calc(100vh-150px)] flex-col">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-400">
            Your Musical Companion
          </p>
          <h1 className="mt-2 text-3xl font-bold text-amber-100">
            AI Music Assistant
          </h1>
          <p className="mt-2 text-sm text-slate-400">
            Explore Carnatic music through real AI-powered conversations.
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={startNewChat}
            className="inline-flex items-center gap-2 rounded-xl border border-amber-500/30 px-4 py-2.5 text-sm text-amber-300 transition hover:bg-amber-500/10"
          >
            <Plus size={17} /> New Chat
          </button>
          <button
            onClick={handleLogout}
            title="Sign out"
            className="rounded-xl border border-white/10 px-3 py-2.5 text-slate-400 hover:bg-white/5 hover:text-amber-300"
          >
            <LogOut size={17} />
          </button>
        </div>
      </div>

      <div className="grid min-h-[600px] flex-1 grid-cols-1 gap-4 lg:grid-cols-[230px_minmax(0,1fr)]">
        <aside className="rounded-2xl border border-amber-500/20 bg-[#0D172D] p-4">
          <h2 className="mb-4 text-sm font-semibold text-amber-200">
            Your Conversations
          </h2>

          <div className="space-y-2">
            {conversations.map((conversation) => (
              <div
                key={conversation.id}
                className={`group flex items-center gap-2 rounded-lg border px-3 py-2 ${
                  activeConversation === conversation.id
                    ? "border-amber-400/40 bg-amber-400/10"
                    : "border-transparent hover:bg-white/5"
                }`}
              >
                <button
                  onClick={() => openConversation(conversation.id)}
                  className="flex min-w-0 flex-1 items-center gap-2 text-left text-xs text-slate-300"
                >
                  <MessageSquare
                    size={15}
                    className="shrink-0 text-amber-400"
                  />
                  <span className="truncate">{conversation.title}</span>
                </button>

                <button
                  onClick={() => handleDeleteConversation(conversation.id)}
                  aria-label="Delete conversation"
                  className="text-slate-600 opacity-0 transition hover:text-red-400 group-hover:opacity-100"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}

            {!loadingHistory && conversations.length === 0 && (
              <p className="text-xs leading-5 text-slate-500">
                Your conversations will appear here.
              </p>
            )}

            {loadingHistory && (
              <p className="text-xs text-slate-500">
                Loading conversations...
              </p>
            )}
          </div>
        </aside>

        <div className="flex min-h-[600px] flex-col rounded-2xl border border-amber-500/20 bg-[#0D172D] p-5 sm:p-8">
          <div className="flex-1 space-y-5 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="flex min-h-[400px] flex-col items-center justify-center py-10 text-center">
                <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-3xl border border-amber-400/30 bg-amber-400/10">
                  <Sparkles size={38} className="text-amber-400" />
                </div>

                <h2 className="text-2xl font-semibold text-amber-100">
                  Namaskaram! Welcome to RagaVerse.
                </h2>

                <p className="mt-3 max-w-lg text-sm leading-7 text-slate-400">
                  Ask questions, explore ragas, understand compositions and
                  deepen your Carnatic music knowledge.
                </p>

                <div className="mt-8 grid w-full max-w-3xl grid-cols-1 gap-3 sm:grid-cols-2">
                  {suggestions.map((suggestion) => {
                    const Icon = suggestion.icon

                    return (
                      <button
                        key={suggestion.title}
                        onClick={() => setInput(suggestion.prompt)}
                        className="rounded-xl border border-white/10 bg-[#14223D] p-4 text-left transition hover:border-amber-400/50 hover:bg-[#192A49]"
                      >
                        <div className="mb-3 flex items-center gap-2 text-amber-400">
                          <Icon size={19} />
                          <span className="font-semibold">
                            {suggestion.title}
                          </span>
                        </div>
                        <p className="text-sm text-slate-400">
                          {suggestion.prompt}
                        </p>
                      </button>
                    )
                  })}
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  {message.role === "assistant" && (
                    <div className="mr-3 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-amber-400/30 bg-amber-400/10 text-amber-400">
                      <Bot size={20} />
                    </div>
                  )}

                  <div
                    className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-5 py-3 text-sm leading-7 ${
                      message.role === "user"
                        ? "rounded-br-sm bg-gradient-to-r from-amber-400 to-amber-600 text-slate-950"
                        : "rounded-tl-sm border border-amber-500/20 bg-[#14223D] text-slate-200"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))
            )}

            {loading && (
              <div className="flex items-center gap-3 text-sm text-amber-300">
                <Loader2 size={18} className="animate-spin" />
                RagaVerse is thinking...
              </div>
            )}
          </div>

          {error && (
            <p className="mt-4 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
              {error}
            </p>
          )}

          <div className="mt-6 flex items-start gap-3 rounded-xl border border-amber-500/15 bg-amber-500/5 p-4">
            <MessageCircle size={19} className="mt-0.5 shrink-0 text-amber-400" />
            <p className="text-xs leading-6 text-slate-400">
              RagaVerse AI responses are generated by the connected backend service.
            </p>
          </div>

          <form
            onSubmit={sendMessage}
            className="mt-5 flex items-center gap-3 rounded-2xl border border-amber-500/25 bg-[#101B35] p-2 focus-within:border-amber-400"
          >
            <input
              type="text"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask anything about Carnatic music..."
              disabled={loading}
              className="min-w-0 flex-1 bg-transparent px-3 py-3 text-sm text-white outline-none placeholder:text-slate-500 disabled:opacity-50"
            />

            <button
              type="submit"
              disabled={!input.trim() || loading}
              aria-label="Send message"
              className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-amber-300 to-amber-600 text-slate-950 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? (
                <Loader2 size={19} className="animate-spin" />
              ) : (
                <Send size={19} />
              )}
            </button>
          </form>
        </div>
      </div>
    </section>
  )
}
