
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8765"
).replace(/\/+$/, "")

const API_PREFIX = "/api/v1"

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const headers = new Headers(options.headers)

  if (token) {
    headers.set("Authorization", `Bearer ${token}`)
  }

  if (options.body && !(options.body instanceof URLSearchParams)) {
    headers.set("Content-Type", "application/json")
  }

  const response = await fetch(
    `${API_BASE_URL}${API_PREFIX}${path}`,
    {
      ...options,
      headers,
    }
  )

  if (!response.ok) {
    let message = `Request failed (${response.status})`

    try {
      const data = await response.json()
      message = data.detail || data.message || message
    } catch {
      // Keep the status-based error message.
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}


// Authentication

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface User {
  id: number
  full_name: string
  email: string
  is_active: boolean
  created_at: string
}

export async function registerUser(
  fullName: string,
  email: string,
  password: string
) {
  return request<User>("/users/register", {
    method: "POST",
    body: JSON.stringify({
      full_name: fullName,
      email,
      password,
    }),
  })
}

export async function login(email: string, password: string) {
  const form = new URLSearchParams()

  form.set("username", email)
  form.set("password", password)

  return request<LoginResponse>("/auth/login", {
    method: "POST",
    body: form,
  })
}


// Conversations

export interface Conversation {
  id: number
  title: string
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: number
  role: "user" | "assistant"
  content: string
  created_at: string
}

export interface ConversationDetail extends Conversation {
  messages: ChatMessage[]
}

export interface ChatResponse {
  user_message: ChatMessage
  assistant_message: ChatMessage
}

export async function getConversations(token: string) {
  return request<Conversation[]>("/conversations/", {}, token)
}

export async function createConversation(
  token: string,
  title: string
) {
  return request<Conversation>(
    "/conversations/",
    {
      method: "POST",
      body: JSON.stringify({ title }),
    },
    token
  )
}

export async function getConversation(
  token: string,
  id: number
) {
  return request<ConversationDetail>(
    `/conversations/${id}`,
    {},
    token
  )
}

export async function sendChatMessage(
  token: string,
  conversationId: number,
  content: string
) {
  return request<ChatResponse>(
    `/conversations/${conversationId}/messages`,
    {
      method: "POST",
      body: JSON.stringify({ content }),
    },
    token
  )
}

export async function deleteConversation(
  token: string,
  id: number
) {
  return request<void>(
    `/conversations/${id}`,
    {
      method: "DELETE",
    },
    token
  )
}


// Raga Explorer

export interface Raga {
  name: string
  aliases: string[]
  category: string
  melakarta_number: number | null
  arohanam: string
  avarohanam: string
  notes: string
  chakra?: string
  source?: string
}

export interface RagaSearchResponse {
  count: number
  results: Raga[]
}

export async function searchRagas(
  query: string,
  melakartaNumber?: number
) {
  const params = new URLSearchParams()

  if (query.trim()) {
    params.set("q", query.trim())
  }

  if (melakartaNumber !== undefined) {
    params.set("melakarta_number", String(melakartaNumber))
  }

  return request<RagaSearchResponse>(
    `/ragas/?${params.toString()}`
  )
}

export async function getRaga(name: string) {
  return request<Raga>(
    `/ragas/${encodeURIComponent(name)}`
  )
}


// Music Learning

export interface LearningLesson {
  id: string
  title: string
  summary: string
  duration_minutes: number
}

export interface LearningModule {
  id: string
  title: string
  level: string
  description: string
  prerequisites: string[]
  lessons: LearningLesson[]
}

export interface LearningModuleListResponse {
  count: number
  results: LearningModule[]
}

export async function getLearningModules(
  level?: string,
  query?: string
) {
  const params = new URLSearchParams()

  if (level) {
    params.set("level", level)
  }

  if (query?.trim()) {
    params.set("q", query.trim())
  }

  const queryString = params.toString()

  return request<LearningModuleListResponse>(
    `/learning/${queryString ? `?${queryString}` : ""}`
  )
}

export async function getLearningModule(moduleId: string) {
  return request<LearningModule>(
    `/learning/${encodeURIComponent(moduleId)}`
  )
}
