"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getTicket, updateTicket, getComments, createComment } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function TicketDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [ticket, setTicket] = useState<any>(null);
  const [comments, setComments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [author, setAuthor] = useState("");
  const [body, setBody] = useState("");
  const [isInternal, setIsInternal] = useState(false);

  async function load() {
    if (!id) return;
    setLoading(true);
    try {
      const [t, c] = await Promise.all([getTicket(id), getComments(id)]);
      setTicket(t);
      setComments(c);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [id]);

  async function handleResolve() {
    if (!id) return;
    await updateTicket(id, { status: "resolved" });
    await load();
  }

  async function handleAddComment(e: React.FormEvent) {
    e.preventDefault();
    if (!id || !author.trim() || !body.trim()) return;
    await createComment({ ticket_id: id, author, body, is_internal: isInternal });
    setAuthor("");
    setBody("");
    setIsInternal(false);
    await load();
  }

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

  if (loading) return <p className="text-slate-500">Loading...</p>;
  if (!ticket) return <p className="text-slate-500">Ticket not found.</p>;

  return (
    <div className="space-y-4">
      <Link href="/tickets" className="text-sm text-slate-600 hover:underline">← Back to tickets</Link>

      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold">{ticket.subject}</h1>
          <div className="mt-2 flex gap-2">
            <Badge className={statusColors[ticket.status] || "bg-slate-100"}>{ticket.status}</Badge>
            <Badge className={priorityColors[ticket.priority] || "bg-slate-100"}>{ticket.priority}</Badge>
          </div>
        </div>
        {ticket.status !== "resolved" && ticket.status !== "closed" && (
          <Button onClick={handleResolve} variant="default">
            Resolve
          </Button>
        )}
      </div>

      <Card>
        <CardContent className="pt-6">
          <p className="text-sm text-slate-500">
            From: {ticket.customer_name || ticket.customer_email} ({ticket.customer_email})
          </p>
          <p className="mt-2 whitespace-pre-wrap">{ticket.description}</p>
          <div className="mt-4 text-sm text-slate-500">
            Assigned to: {ticket.assigned_to || "Unassigned"}
          </div>
        </CardContent>
      </Card>

      <h2 className="text-lg font-semibold">Comments</h2>
      <div className="space-y-3">
        {comments.length === 0 && <p className="text-sm text-slate-500">No comments yet.</p>}
        {comments.map((comment) => (
          <Card key={comment.id} className={comment.is_internal ? "border-orange-300" : ""}>
            <CardContent className="pt-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">{comment.author}</span>
                {comment.is_internal && <Badge className="bg-orange-100 text-orange-800">Internal</Badge>}
              </div>
              <p className="mt-2 whitespace-pre-wrap text-sm">{comment.body}</p>
              <p className="mt-1 text-xs text-slate-400">{new Date(comment.created_at).toLocaleString()}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Add Comment</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleAddComment} className="space-y-3">
            <Input placeholder="Your name" value={author} onChange={(e) => setAuthor(e.target.value)} />
            <textarea
              placeholder="Write a comment..."
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="flex min-h-[80px] w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-400"
            />
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={isInternal} onChange={(e) => setIsInternal(e.target.checked)} />
              Internal note
            </label>
            <Button type="submit" disabled={!author.trim() || !body.trim()}>
              Post Comment
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
