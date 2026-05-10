import { useEffect, useMemo, useState } from "react";
import TreeView, { TreeNode } from "../components/TreeView";

const API_BASE = (import.meta as any).env?.VITE_API_URL ?? "";

type Substrate = "laptop" | "dev" | "stage" | "prod";
type Variant = "APEX-M" | "APEX-G" | "APEX-A";

type RenderResponse = {
  format: "docker-compose" | "bicep-parameters";
  blueprint: string | null;
  parameters: Record<string, unknown> | null;
  compose_yaml: string | null;
  substrate: Substrate;
  primary_variant: Variant;
  use_case_id: string | null;
  summary: {
    wave: "w1" | "w2" | "w3";
    tenant: string;
    substrate?: Substrate;
    primary_variant?: Variant;
    use_case_id?: string | null;
    practices_selected: string[];
    service_count: number;
    scenario_count: number;
    agent_role_filters: number;
  };
};

type UseCase = {
  use_case_id: string;
  service_code: string;
  primary_variant?: Variant;
  client?: string;
  client_segment?: string;
};

const SUBSTRATE_NOTES: Record<Substrate, string> = {
  laptop: "Docker Compose · all Microsoft SDKs mocked · $0 cost · Independence-clean",
  dev: "Lab Azure tenant · real SDKs · no private networking · gates 7+8+13 waivable",
  stage: "Pre-prod tenant · full private networking · all 14 gates required",
  prod: "Production tenant · CMK + Customer Lockbox · all 14 gates + Independence consultation",
};

const VARIANT_NOTES: Record<Variant, string> = {
  "APEX-M": "Microsoft variant — first shipped, fully functional",
  "APEX-G": "Google Cloud variant — Future · Independence Stub",
  "APEX-A": "AWS variant — Future · Independence Stub",
};

export default function Wizard() {
  const [tree, setTree] = useState<TreeNode[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [tenant, setTenant] = useState("contoso-prod");
  const [wave, setWave] = useState<"w1" | "w2" | "w3">("w2");
  const [substrate, setSubstrate] = useState<Substrate>("dev");
  const [primaryVariant, setPrimaryVariant] = useState<Variant>("APEX-M");
  const [useCases, setUseCases] = useState<UseCase[]>([]);
  const [useCaseId, setUseCaseId] = useState<string>("");
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

  // Reload use cases when the operator picks a different service in the tree
  // (or just on mount). For now, fetch all and filter client-side.
  useEffect(() => {
    fetch(`${API_BASE}/api/catalog/use-cases`)
      .then((r) => (r.ok ? r.json() : []))
      .then((data: UseCase[]) => {
        setUseCases(data);
        if (!useCaseId && data.length > 0) setUseCaseId(data[0].use_case_id);
      })
      .catch(() => setUseCases([]));
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
          substrate,
          primary_variant: primaryVariant,
          use_case_id: useCaseId || null,
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

        <label className="block text-sm mb-1">Cloud variant</label>
        <select
          value={primaryVariant}
          onChange={(e) => setPrimaryVariant(e.target.value as Variant)}
          className="w-full border rounded px-2 py-1 text-sm"
        >
          <option value="APEX-M">APEX-M (Microsoft)</option>
          <option value="APEX-G" disabled>APEX-G (Google · stub)</option>
          <option value="APEX-A" disabled>APEX-A (AWS · stub)</option>
        </select>
        <p className="text-[11px] text-gray-500 mb-3 mt-1">{VARIANT_NOTES[primaryVariant]}</p>

        <label className="block text-sm mb-1">Substrate</label>
        <select
          value={substrate}
          onChange={(e) => setSubstrate(e.target.value as Substrate)}
          className="w-full border rounded px-2 py-1 text-sm"
        >
          <option value="laptop">laptop · Docker Compose · mocks</option>
          <option value="dev">dev (Lab) · Bicep · real SDKs</option>
          <option value="stage">stage · Bicep + private networking</option>
          <option value="prod">prod · Bicep + CMK + Customer Lockbox</option>
        </select>
        <p className="text-[11px] text-gray-500 mb-3 mt-1">{SUBSTRATE_NOTES[substrate]}</p>

        <label className="block text-sm mb-1">Use case</label>
        <select
          value={useCaseId}
          onChange={(e) => setUseCaseId(e.target.value)}
          className="w-full border rounded px-2 py-1 text-sm mb-3"
        >
          <option value="">— none —</option>
          {useCases.map((uc) => (
            <option key={uc.use_case_id} value={uc.use_case_id}>
              {uc.use_case_id}
            </option>
          ))}
        </select>

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
          disabled={substrate === "laptop"}
          title={substrate === "laptop" ? "Wave is informational only on laptop substrate" : ""}
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
          {substrate === "laptop"
            ? "Render docker-compose.yml"
            : "Render Bicep parameters"}
        </button>

        <p className="text-xs text-gray-500 mt-2">
          {substrate === "laptop" ? (
            <>
              Render emits a <code className="text-xs">docker-compose.yml</code>{" "}
              for local execution. <code className="text-xs">docker-compose up</code>{" "}
              brings the agent + mocks online; no client cloud touched.
            </>
          ) : (
            <>
              Render is preview-only. The deploy step (calls{" "}
              <code className="text-xs">az deployment group create</code>) is wired
              but not yet implemented — see{" "}
              <code className="text-xs">bicep_runner.py</code> (Sprint 46).
            </>
          )}
        </p>

        {rendered && (
          <div className="mt-4 border-t pt-3">
            <div className="text-sm font-medium mb-1">
              Format: <code className="text-xs">{rendered.format}</code>
            </div>
            <div className="text-sm font-medium mb-1">Summary</div>
            <pre className="text-xs bg-white border rounded p-2 overflow-auto max-h-32">
              {JSON.stringify(rendered.summary, null, 2)}
            </pre>
            {rendered.format === "docker-compose" ? (
              <>
                <div className="text-sm font-medium mt-2 mb-1">
                  docker-compose.yml
                </div>
                <pre className="text-xs bg-white border rounded p-2 overflow-auto max-h-96 font-mono">
                  {rendered.compose_yaml}
                </pre>
              </>
            ) : (
              <>
                <div className="text-sm font-medium mt-2 mb-1">Blueprint</div>
                <code className="block text-xs bg-white border rounded p-1 mb-2">
                  {rendered.blueprint}
                </code>
                <div className="text-sm font-medium mt-2 mb-1">Parameters</div>
                <pre className="text-xs bg-white border rounded p-2 overflow-auto max-h-96">
                  {JSON.stringify(rendered.parameters, null, 2)}
                </pre>
              </>
            )}
          </div>
        )}
      </aside>
    </section>
  );
}
