import { useEffect, useMemo, useState } from "react";
import TreeView, { TreeNode } from "../components/TreeView";

const API_BASE = (import.meta as any).env?.VITE_API_URL ?? "";

type RenderResponse = {
  blueprint: string;
  parameters: Record<string, unknown>;
  summary: {
    wave: "w1" | "w2" | "w3";
    tenant: string;
    practices_selected: string[];
    service_count: number;
    scenario_count: number;
    agent_role_filters: number;
  };
};

export default function Wizard() {
  const [tree, setTree] = useState<TreeNode[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [tenant, setTenant] = useState("contoso-prod");
  const [wave, setWave] = useState<"w1" | "w2" | "w3">("w2");
  const [rendered, setRendered] = useState<RenderResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const url = `${API_BASE}/api/catalog/tree?featured_only=true`;
    fetch(url)
      .then((r) => {
        if (!r.ok) throw new Error(`tree ${r.status}`);
        return r.json();
      })
      .then((data: TreeNode[]) => {
        setTree(data);
        setLoading(false);
      })
      .catch((e: Error) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  const summary = useMemo(() => {
    let pr = 0,
      sv = 0,
      sc = 0,
      ag = 0;
    selected.forEach((id) => {
      const k = id.split(":")[0];
      if (k === "practice") pr++;
      else if (k === "service") sv++;
      else if (k === "scenario") sc++;
      else if (k === "agent") ag++;
    });
    return { pr, sv, sc, ag };
  }, [selected]);

  const onRender = async () => {
    setError(null);
    setRendered(null);
    try {
      const res = await fetch(`${API_BASE}/api/deployments/render`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          selected_ids: Array.from(selected),
          tenant,
          wave,
        }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`${res.status} ${text}`);
      }
      const data = (await res.json()) as RenderResponse;
      setRendered(data);
    } catch (e: any) {
      setError(e.message ?? String(e));
    }
  };

  const canRender = selected.size > 0 && tenant.trim().length >= 3;

  return (
    <section className="grid grid-cols-1 lg:grid-cols-[1fr_24rem] gap-4">
      <div>
        <header className="mb-3">
          <h1 className="text-2xl font-bold">Deploy Wizard</h1>
          <p className="text-sm text-gray-600">
            Pick the practices, services, scenarios, and agents to deploy onto an
            Azure tenant. Selections roll up: select a practice and every service
            beneath it is included; expand to deselect specific scenarios or
            agents. Output is a Bicep parameter file for{" "}
            <code className="text-xs">apex-m/infra/bicep/blueprints/&lt;wave&gt;.bicep</code>{" "}
            (APEX-M variant).
          </p>
        </header>

        {loading && <p>Loading catalog…</p>}
        {error && (
          <p className="text-sm text-red-700 border border-red-200 bg-red-50 rounded p-2">
            {error}
          </p>
        )}
        {!loading && tree.length > 0 && (
          <TreeView nodes={tree} selectedIds={selected} onChange={setSelected} />
        )}
      </div>

      <aside className="border rounded p-3 bg-gray-50 h-fit sticky top-2">
        <h2 className="font-bold mb-3">Deployment</h2>

        <label className="block text-sm mb-1">Tenant slug</label>
        <input
          value={tenant}
          onChange={(e) => setTenant(e.target.value)}
          className="w-full border rounded px-2 py-1 text-sm mb-3"
          placeholder="contoso-prod"
        />

        <label className="block text-sm mb-1">Wave</label>
        <select
          value={wave}
          onChange={(e) => setWave(e.target.value as any)}
          className="w-full border rounded px-2 py-1 text-sm mb-3"
        >
          <option value="w1">W1 — Foundation</option>
          <option value="w2">W2 — Pilot</option>
          <option value="w3">W3 — Scale & Fuse</option>
        </select>

        <div className="text-sm border-t pt-2 mb-3">
          <div className="font-medium mb-1">Selection</div>
          <ul className="text-gray-700">
            <li>{summary.pr} practice{summary.pr === 1 ? "" : "s"}</li>
            <li>{summary.sv} service{summary.sv === 1 ? "" : "s"}</li>
            <li>{summary.sc} scenario{summary.sc === 1 ? "" : "s"}</li>
            <li>{summary.ag} agent{summary.ag === 1 ? "" : "s"}</li>
          </ul>
        </div>

        <button
          type="button"
          disabled={!canRender}
          onClick={onRender}
          className="w-full bg-blue-600 text-white rounded px-3 py-2 text-sm disabled:bg-gray-300"
        >
          Render Bicep parameters
        </button>

        <p className="text-xs text-gray-500 mt-2">
          Render is preview-only. The deploy step (calls{" "}
          <code className="text-xs">az deployment group create</code>) is wired
          but not yet implemented — see <code className="text-xs">bicep_runner.py</code>.
        </p>

        {rendered && (
          <div className="mt-4 border-t pt-3">
            <div className="text-sm font-medium mb-1">Blueprint</div>
            <code className="block text-xs bg-white border rounded p-1 mb-2">
              {rendered.blueprint}
            </code>
            <div className="text-sm font-medium mb-1">Summary</div>
            <pre className="text-xs bg-white border rounded p-2 overflow-auto max-h-32">
              {JSON.stringify(rendered.summary, null, 2)}
            </pre>
            <div className="text-sm font-medium mt-2 mb-1">Parameters</div>
            <pre className="text-xs bg-white border rounded p-2 overflow-auto max-h-96">
              {JSON.stringify(rendered.parameters, null, 2)}
            </pre>
          </div>
        )}
      </aside>
    </section>
  );
}
