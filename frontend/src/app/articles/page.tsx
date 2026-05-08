"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getArticles } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";

export default function ArticlesPage() {
  const [articles, setArticles] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await getArticles({ search: search || undefined, category: category || undefined, limit: 50 });
        setArticles(data.items);
        setTotal(data.total);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [search, category]);

  const categoryColors: Record<string, string> = {
    general: "bg-slate-100 text-slate-800",
    billing: "bg-blue-100 text-blue-800",
    technical: "bg-purple-100 text-purple-800",
    account: "bg-green-100 text-green-800",
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Knowledge Base</h1>

      <div className="flex flex-wrap gap-3">
        <Input
          placeholder="Search articles..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-64"
        />
        <Select value={category} onValueChange={setCategory} className="w-40">
          <option value="">All categories</option>
          <option value="general">General</option>
          <option value="billing">Billing</option>
          <option value="technical">Technical</option>
          <option value="account">Account</option>
        </Select>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{total} articles found</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {loading ? (
            <p className="text-slate-500">Loading...</p>
          ) : (
            articles.map((article) => (
              <div key={article.id} className="flex items-center justify-between rounded-md border p-3">
                <div className="min-w-0">
                  <Link href={`/articles/${article.id}`} className="truncate font-medium hover:underline">
                    {article.title}
                  </Link>
                  <p className="text-xs text-slate-500">{article.views} views</p>
                </div>
                <Badge className={categoryColors[article.category] || "bg-slate-100"}>{article.category}</Badge>
              </div>
            ))
          )}
          {!loading && articles.length === 0 && (
            <p className="text-slate-500">No articles found.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
