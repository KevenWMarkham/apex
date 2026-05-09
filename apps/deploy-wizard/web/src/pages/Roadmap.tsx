import { useEffect, useMemo, useState } from "react";

const API_BASE = (import.meta as any).env?.VITE_API_URL ?? "";

type SprintItem = {
  id: string;
  title: string;
  done?: boolean;
  bicep_ref?: string;
  roadmap_ref?: string[];
  services_guide_ref?: string;
};

type Sprint = {
  id: string;
  name: string;
  range?: string;
  objective?: string;
  note?: string;
  items: SprintItem[];
};

type ServiceStatus = {
  status: string;
  title?: string;
  flagship?: boolean;
  sprint?: string;
  services_guide_ref?: string;
  scenarios?: Record<string, { status: string; sprint?: string; agents?: Record<string, any> }>;
  note?: string;
};

type Plan = {
  practice: string;
  practice_label: string;
  plan_version: number;
  plan_owner?: string;
  services_guide_ref?: string;
  roadmap_ref?: string;
  sprints: Sprint[];
  services: Record<string, ServiceStatus>;
};

type ApiResponse = { practices: Plan[] };

const STATUS_COLOR: Record<string, string> = {
  planned: "text-gray-700 bg-gray-100",
  scaffolded: "text-cyan-700 bg-cyan-50",
  implemented: "text-indigo-700 bg-indigo-50",
  deployed: "text-green-700 bg-green-50",
  pilot: "text-amber-700 bg-amber-50",
  ga: "text-emerald-700 bg-emerald-50 font-semibold",
};

function StatusBadge({ status }: { status: string }) {
  const cls = STATUS_COLOR[status] ?? "text-gray-700 bg-gray-100";
  return (
    <span className={`text-[10px] uppercase tracking-wide px-1.5 py-0.5 rounded ${cls}`}>
      {status}
    </span>
  );
}

function SprintCard({ sprint }: { sprint: Sprint }) {
  const total = sprint.items?.length ?? 0;
  const done = sprint.items?.filter((i) => i.done).length ?? 0;
  const pct = total ? Math.round((done * 100) / total) : 0;
  return (
    <article className="border rounded p-3 mb-3 bg-white">
      <header className="flex items-baseline justify-between gap-3 mb-2">
        <div>
          <h3 className="font-bold">
            <code className="text-sm">{sprint.id}</code> · {sprint.name}
          </h3>
          {sprint.range && <div className="text-xs text-gray-500">{sprint.range}</div>}
        </div>
        <div className="text-sm">
          <span className="font-mono">
            {done}/{total}
          </span>{" "}
          done
        </div>
      </header>

      <div className="w-full bg-gray-100 rounded h-1.5 mb-3">
        <div
          className={`h-1.5 rounded ${
            pct === 100 ? "bg-green-500" : pct > 0 ? "bg-blue-500" : "bg-gray-300"
          }`}
          style={{ width: `${pct}%` }}
        />
      </div>

      {sprint.objective && (
        <p className="text-sm text-gray-700 mb-2">{sprint.objective}</p>
      )}
      {sprint.note && (
        <p className="text-xs text-amber-700 italic mb-2">{sprint.note}</p>
      )}

      <ul className="space-y-1">
        {sprint.items?.map((item) => (
          <li key={item.id} className="flex items-start gap-2 text-sm">
            <input
              type="checkbox"
              checked={!!item.done}
              readOnly
              className="mt-1"
              aria-label={item.done ? "done" : "not done"}
            />
            <div className="flex-1">
              <span className="font-mono text-xs text-gray-500 mr-1">{item.id}</span>
              {item.title}
              {(item.bicep_ref || item.roadmap_ref || item.services_guide_ref) && (
                <div className="text-xs text-gray-500 mt-0.5 flex flex-wrap gap-2">
                  {item.bicep_ref && <code>{item.bicep_ref}</code>}
                  {item.roadmap_ref && (
                    <span>refs: {item.roadmap_ref.join(", ")}</span>
                  )}
                  {item.services_guide_ref && (
                    <span>SG: {item.services_guide_ref}</span>
                  )}
                </div>
              )}
            </div>
          </li>
        ))}
      </ul>
    </article>
  );
}

function ServicesTable({ plan }: { plan: Plan }) {
  const rows = Object.entries(plan.services || {});
  return (
    <div className="border rounded overflow-hidden mb-4">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-left">
          <tr>
            <th className="p-2">Service</th>
            <th className="p-2">Title</th>
            <th className="p-2">Status</th>
            <th className="p-2">Sprint</th>
            <th className="p-2">Featured</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([code, svc]) => {
            const featured = Object.keys(svc.scenarios ?? {}).length;
            return (
              <tr key={code} className="border-t">
                <td className="p-2 font-mono">
                  {code} {svc.flagship && <span title="Flagship">⭐</span>}
                </td>
                <td className="p-2">{svc.title}</td>
                <td className="p-2">
                  <StatusBadge status={svc.status} />
                </td>
                <td className="p-2 font-mono text-xs">{svc.sprint || ""}</td>
                <td className="p-2">{featured}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default function Roadmap() {
  const [plans, setPlans] = useState<Plan[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activePractice, setActivePractice] = useState<string>("rc");

  useEffect(() => {
    fetch(`${API_BASE}/api/catalog/build-status`)
      .then((r) => {
        if (!r.ok) throw new Error(`build-status ${r.status}`);
        return r.json() as Promise<ApiResponse>;
      })
      .then((data) => setPlans(data.practices))
      .catch((e: Error) => setError(e.message));
  }, []);

  const active = useMemo(() => {
    if (!plans) return null;
    return plans.find((p) => p.practice === activePractice) ?? plans[0] ?? null;
  }, [plans, activePractice]);

  const totals = useMemo(() => {
    if (!active) return { done: 0, total: 0 };
    let done = 0;
    let total = 0;
    active.sprints?.forEach((s) =>
      s.items?.forEach((i) => {
        total++;
        if (i.done) done++;
      })
    );
    return { done, total };
  }, [active]);

  if (error) {
    return (
      <p className="text-sm text-red-700 border border-red-200 bg-red-50 rounded p-2">
        {error}
      </p>
    );
  }
  if (!plans) return <p>Loading roadmap…</p>;
  if (plans.length === 0) {
    return (
      <p className="text-sm">
        No build plans yet. Add <code>services/&lt;practice&gt;/_build-status.yaml</code> to populate this page.
      </p>
    );
  }

  return (
    <section>
      <header className="mb-4">
        <h1 className="text-2xl font-bold">Build Roadmap</h1>
        <p className="text-sm text-gray-600">
          Per-practice sprint plan with services and agents tracked end-to-end.
          Source of truth: <code>services/&lt;practice&gt;/_build-status.yaml</code>.
          Edits there flow back here on next page load.
        </p>
      </header>

      <nav className="flex gap-2 border-b pb-2 mb-4">
        {plans.map((p) => (
          <button
            key={p.practice}
            type="button"
            onClick={() => setActivePractice(p.practice)}
            className={`text-sm px-3 py-1 rounded border ${
              p.practice === active?.practice
                ? "bg-blue-600 text-white border-blue-600"
                : "bg-white text-gray-800 border-gray-300"
            }`}
          >
            {p.practice_label}
          </button>
        ))}
      </nav>

      {active && (
        <>
          <div className="mb-4 bg-gray-50 border rounded p-3 text-sm">
            <div className="flex items-baseline justify-between">
              <div>
                <span className="font-bold">{active.practice_label}</span>{" "}
                <span className="text-gray-500">· plan v{active.plan_version}</span>
                {active.plan_owner && (
                  <span className="text-gray-500"> · {active.plan_owner}</span>
                )}
              </div>
              <div className="font-mono">
                {totals.done}/{totals.total} items done
              </div>
            </div>
            {active.services_guide_ref && (
              <div className="text-xs text-gray-500 mt-1">
                Reference: <code>{active.services_guide_ref}</code>
              </div>
            )}
          </div>

          <h2 className="text-lg font-bold mb-2">Services</h2>
          <ServicesTable plan={active} />

          <h2 className="text-lg font-bold mb-2">Sprints</h2>
          {active.sprints?.map((s) => (
            <SprintCard key={s.id} sprint={s} />
          ))}
        </>
      )}
    </section>
  );
}
