const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API error ${response.status}: ${error}`);
  }
  return response.json();
}

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

// Stats
export async function getStats() {
  return fetchJson<{ open_tickets: number; resolved_today: number; kb_articles: number }>("/api/v1/stats/");
}

// Tickets
export interface Ticket {
  id: string;
  subject: string;
  description: string;
  status: string;
  priority: string;
  customer_email: string;
  customer_name: string | null;
  assigned_to: string | null;
  created_at: string;
  updated_at: string;
  comments?: Comment[];
}

export interface TicketList {
  items: Ticket[];
  total: number;
}

export async function getTickets(params?: { status?: string; priority?: string; search?: string; limit?: number; offset?: number }) {
  const query = new URLSearchParams();
  if (params?.status) query.set("status", params.status);
  if (params?.priority) query.set("priority", params.priority);
  if (params?.search) query.set("search", params.search);
  if (params?.limit !== undefined) query.set("limit", String(params.limit));
  if (params?.offset !== undefined) query.set("offset", String(params.offset));
  return fetchJson<TicketList>(`/api/v1/tickets/?${query.toString()}`);
}

export async function getTicket(id: string) {
  return fetchJson<Ticket>(`/api/v1/tickets/${id}`);
}

export async function createTicket(data: Omit<Ticket, "id" | "created_at" | "updated_at" | "comments">) {
  return fetchJson<Ticket>("/api/v1/tickets/", { method: "POST", body: JSON.stringify(data) });
}

export async function updateTicket(id: string, data: Partial<Omit<Ticket, "id" | "created_at" | "updated_at" | "comments">>) {
  return fetchJson<Ticket>(`/api/v1/tickets/${id}`, { method: "PATCH", body: JSON.stringify(data) });
}

export async function deleteTicket(id: string) {
  return fetch(`/api/v1/tickets/${id}`, { method: "DELETE" });
}

// Comments
export interface Comment {
  id: string;
  ticket_id: string;
  author: string;
  body: string;
  is_internal: boolean;
  created_at: string;
}

export async function getComments(ticketId: string) {
  return fetchJson<Comment[]>(`/api/v1/comments/ticket/${ticketId}`);
}

export async function createComment(data: Omit<Comment, "id" | "created_at">) {
  return fetchJson<Comment>("/api/v1/comments/", { method: "POST", body: JSON.stringify(data) });
}

// KB Articles
export interface KBArticle {
  id: string;
  title: string;
  content: string;
  category: string;
  views: number;
  created_at: string;
  updated_at: string;
}

export interface KBArticleList {
  items: KBArticle[];
  total: number;
}

export async function getArticles(params?: { category?: string; search?: string; limit?: number; offset?: number }) {
  const query = new URLSearchParams();
  if (params?.category) query.set("category", params.category);
  if (params?.search) query.set("search", params.search);
  if (params?.limit !== undefined) query.set("limit", String(params.limit));
  if (params?.offset !== undefined) query.set("offset", String(params.offset));
  return fetchJson<KBArticleList>(`/api/v1/articles/?${query.toString()}`);
}

export async function getArticle(id: string) {
  return fetchJson<KBArticle>(`/api/v1/articles/${id}`);
}
