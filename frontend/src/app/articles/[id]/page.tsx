"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getArticle } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function ArticleDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      if (!id) return;
      try {
        const data = await getArticle(id);
        setArticle(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  const categoryColors: Record<string, string> = {
    general: "bg-slate-100 text-slate-800",
    billing: "bg-blue-100 text-blue-800",
    technical: "bg-purple-100 text-purple-800",
    account: "bg-green-100 text-green-800",
  };

  if (loading) return <p className="text-slate-500">Loading...</p>;
  if (!article) return <p className="text-slate-500">Article not found.</p>;

  return (
    <div className="space-y-4">
      <Link href="/articles" className="text-sm text-slate-600 hover:underline">← Back to articles</Link>

      <div className="flex items-start justify-between">
        <h1 className="text-2xl font-bold">{article.title}</h1>
        <Badge className={categoryColors[article.category] || "bg-slate-100"}>{article.category}</Badge>
      </div>

      <p className="text-sm text-slate-500">{article.views} views</p>

      <Card>
        <CardContent className="pt-6">
          <div className="prose max-w-none whitespace-pre-wrap">{article.content}</div>
        </CardContent>
      </Card>
    </div>
  );
}
