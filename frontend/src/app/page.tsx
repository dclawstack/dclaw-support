"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getStats, getTickets, getArticles } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function Dashboard() {
  const [stats, setStats] = useState({ open_tickets: 0, resolved_today: 0, kb_articles: 0 });
  const [recentTickets, setRecentTickets] = useState<any[]>([]);
  const [recentArticles, setRecentArticles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, t, a] = await Promise.all([
          getStats(),
          getTickets({ limit: 5 }),
          getArticles({ limit: 5 }),
        ]);
        setStats(s);
        setRecentTickets(t.items);
        setRecentArticles(a.items);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <p className="text-slate-500">Loading...</p>;

  const statusColors: Record<string, string> = {
    open: "bg-blue-100 text-blue-800",
    in_progress: "bg-yellow-100 text-yellow-800",
    waiting: "bg-purple-100 text-purple-800",
    resolved: "bg-green-100 text-green-800",
    closed: "bg-slate-100 text-slate-800",
  };

  const priorityColors: Record<string, string> = {
    low: "bg-slate-100 text-slate-800",
    medium: "bg-blue-100 text-blue-800",
    high: "bg-orange-100 text-orange-800",
    urgent: "bg-red-100 text-red-800",
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-500">Open Tickets</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.open_tickets}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-500">Resolved Today</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.resolved_today}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-500">KB Articles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{stats.kb_articles}</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Tickets</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {recentTickets.length === 0 && <p className="text-sm text-slate-500">No tickets yet.</p>}
            {recentTickets.map((ticket) => (
              <div key={ticket.id} className="flex items-center justify-between rounded-md border p-3">
                <div className="min-w-0">
                  <Link href={`/tickets/${ticket.id}`} className="truncate font-medium hover:underline">
                    {ticket.subject}
                  </Link>
                  <p className="text-xs text-slate-500">{ticket.customer_email}</p>
                </div>
                <div className="flex shrink-0 gap-2">
                  <Badge className={statusColors[ticket.status] || "bg-slate-100"}>{ticket.status}</Badge>
                  <Badge className={priorityColors[ticket.priority] || "bg-slate-100"}>{ticket.priority}</Badge>
                </div>
              </div>
            ))}
            <Link href="/tickets" className="inline-block text-sm font-medium text-slate-900 hover:underline">
              View all tickets →
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent KB Articles</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {recentArticles.length === 0 && <p className="text-sm text-slate-500">No articles yet.</p>}
            {recentArticles.map((article) => (
              <div key={article.id} className="flex items-center justify-between rounded-md border p-3">
                <div className="min-w-0">
                  <Link href={`/articles/${article.id}`} className="truncate font-medium hover:underline">
                    {article.title}
                  </Link>
                  <p className="text-xs text-slate-500">{article.category} • {article.views} views</p>
                </div>
              </div>
            ))}
            <Link href="/articles" className="inline-block text-sm font-medium text-slate-900 hover:underline">
              View all articles →
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
