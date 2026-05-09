import { useEffect, useState } from "react";

const API_BASE = (import.meta as any).env?.VITE_API_URL ?? "";

type CategoryInfo = {
  category: string;
  count: number;
  adapters: string[];
};

const KIND_COLOR: Record<string, string> = {
  cloud: "text-blue-700 bg-blue-50 border-blue-200",
  saas: "text-purple-700 bg-purple-50 border-purple-200",
  siem: "text-amber-700 bg-amber-50 border-amber-200",
  identity: "text-emerald-700 bg-emerald-50 border-emerald-200",
  collaboration: "text-pink-700 bg-pink-50 border-pink-200",
};

export default function Adapters() {
  const [adapters, setAdapters] = useState<string[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/catalog/adapters`)
      .then((r) => {
        if (!r.ok) throw new Error(`adapters ${r.status}`);
        return r.json();
      })
      .then(setAdapters)
      .catch((e: Error) => setError(e.message));
  }, []);

  if (error)
    return (
      <p className="text-sm text-red-700 border border-red-200 bg-red-50 rounded p-2">
        {error}
      </p>
    );
  if (!adapters) return <p>Loading adapters…</p>;

  const byCategory: Record<string, string[]> = {};
  adapters.forEach((a) => {
    const category = a.split(".")[0];
    if (!byCategory[category]) byCategory[category] = [];
    byCategory[category].push(a);
  });

  return (
    <section>
      <header className="mb-4">
        <h1 className="text-2xl font-bold">Adapter Catalog</h1>
        <p className="text-sm text-gray-600">
          APEX adapters integrate non-primary services into APEX-Core
          protocols. Reference these in a use-case YAML's{" "}
          <code className="text-xs">client_approved_architecture</code> block
          to honor a client's CAB-approved cloud architecture without
          changing the primary variant. Each adapter ships a stub today;
          concrete impl builds per-engagement when the client's CAB has
          approved the integration.
        </p>
        <p className="text-xs text-gray-500 mt-2">
          Source of truth:{" "}
          <code>packages/apex-adapters/src/apex_adapters/protocol_adapters/</code>{" "}
          · Catalog reference:{" "}
          <code>docs/apex-core/Adapter-Catalog.md</code>
        </p>
      </header>

      <div className="space-y-4">
        {Object.entries(byCategory).map(([cat, list]) => (
          <article key={cat} className="border rounded p-3 bg-white">
            <header className="flex items-baseline gap-2 mb-2">
              <span
                className={`text-xs uppercase px-2 py-0.5 rounded border font-semibold ${
                  KIND_COLOR[cat] ?? "text-gray-700 bg-gray-100 border-gray-300"
                }`}
              >
                {cat}
              </span>
              <span className="text-sm text-gray-500">
                {list.length} adapter{list.length === 1 ? "" : "s"}
              </span>
            </header>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {list.map((a) => (
                <li
                  key={a}
                  className="text-sm font-mono border rounded px-2 py-1 flex items-center justify-between"
                >
                  <span>{a}</span>
                  <span className="text-[10px] uppercase tracking-wide text-cyan-700 bg-cyan-50 px-1.5 py-0.5 rounded border border-cyan-200">
                    stub
                  </span>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </div>

      <aside className="mt-6 border rounded p-3 bg-blue-50 border-blue-200 text-sm">
        <h2 className="font-bold text-blue-900 mb-1">
          How adapters compose with the primary variant
        </h2>
        <p className="text-blue-900">
          A use case picks ONE primary variant (APEX-M / APEX-G / APEX-A)
          for the agent runtime and identity rooting. Adapters fill the
          remaining protocol slots — data lake bronze sources, federated
          identity, parallel-write SIEM, etc. — per the client's
          CAB-approved architecture. Deloitte does not have an alliance
          posture with any cloud or SaaS provider; adapters honor existing
          client investments.
        </p>
      </aside>
    </section>
  );
}
