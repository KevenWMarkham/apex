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

type GateRow = {
  gate_id: string;
  title: string;
  status: "green" | "yellow" | "red" | "unknown";
  blocking: boolean;
  rationale: string;
  remediate: string | null;
};

type GateReport = {
  tenant: string;
  overall_status: "green" | "yellow" | "red" | "unknown";
  deploy_allowed: boolean;
  red_gates: string[];
  gates: GateRow[];
};

type DeploymentRecord = {
  id: string;
  tenant: string;
  wave: "w1" | "w2" | "w3";
  status: "pending" | "running" | "succeeded" | "failed" | "rolled_back";
  blueprint_path: string;
  bicep_what_if_summary: {
    counts: Record<string, number>;
    has_destructive: boolean;
    mode: string;
    duration_ms: number;
  } | null;
  audit_row_id: string | null;
};

const SUBSTRATE_NOTES: Record<Substrate, string> = {
  laptop: "Docker Compose · all Microsoft SDKs mocked · $0 cost · Independence-clean",
  dev: "Lab Azure tenant · real SDKs · no private networking · gates 7+8+13 waivable",
  stage: "Pre-prod tenant · full private networking · all 14 gates required",
  prod: "Production tenant · CMK + Customer Lockbox · all 15 gates + Independence consultation",
};

const VARIANT_NOTES: Record<Variant, string> = {
  "APEX-M": "Microsoft variant — first shipped, fully functional",
  "APEX-G": "Google Cloud variant — Future · Independence Stub",
  "APEX-A": "AWS variant — Future · Independence Stub",
};

const STATUS_COLOR: Record<string, string> = {
  green: "text-green-700 bg-green-50 border-green-200",
  yellow: "text-amber-700 bg-amber-50 border-amber-200",
  red: "text-red-700 bg-red-50 border-red-200",
  unknown: "text-gray-700 bg-gray-50 border-gray-200",
};

export default function Wizard() {
  const [tree, setTree] = useState<TreeNode[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [tenant, setTenant] = useState("contoso-prod");
  const [wave, setWave] = useState<"w1" | "w2" | "w3">("w2");
  const [substrate, setSubstrate] = useState<Substrate>("dev");
  const [primaryVariant, setPrimaryVariant] = useState<Variant>("APEX-M");
  const [operator, setOperator] = useState("operator@labtenant.onmicrosoft.com");
  const [confirmDestructive, setConfirmDestructive] = useState(false);
  const [useCases, setUseCases] = useState<UseCase[]>([]);
  const [useCaseId, setUseCaseId] = useState<string>("");
  const [rendered, setRendered] = useState<RenderResponse | null>(null);
  const [gateReport, setGateReport] = useState<GateReport | null>(null);
  const [deployment, setDeployment] = useState<DeploymentRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [deploying, setDeploying] = useState(false);

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
    let pr = 0, sv = 0, sc = 0, ag = 0;
    selected.forEach((id) => {
      const k = id.split(":")[0];
      if (k === "practice") pr++;
      else if (k === "service") sv++;
      else if (k === "scenario") sc++;
      else if (k === "agent") ag++;
    });
    return { pr, sv, sc, ag };
  }, [selected]);

  const pollGates = async () => {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/security-gate?tenant=${encodeURIComponent(tenant)}`);
      if (!res.ok) throw new Error(`gates ${res.status}`);
      const data = (await res.json()) as GateReport;
      setGateReport(data);
    } catch (e: any) {
      setError(e.message ?? String(e));
    }
  };

  const onRender = async () => {
    setError(null);
    setRendered(null);
    setDeployment(null);
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
      // Also poll gates after render — operator wants to see them before deploy
      pollGates();
    } catch (e: any) {
      setError(e.message ?? String(e));
    }
  };

  const onDeploy = async () => {
    if (!rendered) return;
    setError(null);
    setDeploying(true);
    setDeployment(null);
    try {
      // Build selections from the selected service ids.
      const services: string[] = [];
      selected.forEach((id) => {
        if (id.startsWith("service:")) services.push(id.slice("service:".length));
      });
      const selectionsArr = services.length > 0
        ? services.map((code) => ({ service_code: code, featured_scenarios: [] }))
        : [{ service_code: "RC-E2E-03", featured_scenarios: [] }];

      const note = confirmDestructive
        ? "confirm_destructive=true · operator-approved via wizard UI"
        : "wizard-driven deploy";
      const res = await fetch(`${API_BASE}/api/deployments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tenant,
          wave,
          selections: selectionsArr,
          operator,
          note,
        }),
      });
      if (!res.ok) {
        const detail = await res.json().catch(() => ({}));
        throw new Error(
          `${res.status}: ${detail.detail?.error ?? detail.detail ?? "deploy failed"}`,
        );
      }
      const record = (await res.json()) as DeploymentRecord;
      setDeployment(record);
    } catch (e: any) {
      setError(e.message ?? String(e));
    } finally {
      setDeploying(false);
    }
  };

  const canRender = selected.size > 0 && tenant.trim().length >= 3;
  const canDeploy =
    !!rendered &&
    !deploying &&
    rendered.format === "bicep-parameters" &&
    gateReport?.deploy_allowed !== false;

  return (
    <section className="grid grid-cols-1 lg:grid-cols-[1fr_28rem] gap-4">
      <div>
        <header className="mb-3">
          <h1 className="text-2xl font-bold">Deploy Wizard</h1>
          <p className="text-sm text-gray-600">
            Pick the practices, services, scenarios, and agents to deploy. Selections roll up:
            select a practice and every service beneath it is included; expand to deselect
            specifics. Output is either a <code className="text-xs">docker-compose.yml</code>
            {" "}(laptop substrate) or a Bicep parameter file (cloud).
          </p>
        </header>

        {loading && <p>Loading catalog…</p>}
        {error && (
          <p className="text-sm text-red-700 border border-red-200 bg-red-50 rounded p-2 mb-2">
            {error}
          </p>
        )}
        {!loading && tree.length > 0 && (
          <TreeView nodes={tree} selectedIds={selected} onChange={setSelected} />
        )}
      </div>

      <aside className="border rounded p-3 bg-gray-50 h-fit sticky top-2 space-y-3">
        <h2 className="font-bold">Deployment</h2>

        <div>
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
          <p className="text-[11px] text-gray-500 mt-1">{VARIANT_NOTES[primaryVariant]}</p>
        </div>

        <div>
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
          <p className="text-[11px] text-gray-500 mt-1">{SUBSTRATE_NOTES[substrate]}</p>
        </div>

        <div>
          <label className="block text-sm mb-1">Use case</label>
          <select
            value={useCaseId}
            onChange={(e) => setUseCaseId(e.target.value)}
            className="w-full border rounded px-2 py-1 text-sm"
          >
            <option value="">— none —</option>
            {useCases.map((uc) => (
              <option key={uc.use_case_id} value={uc.use_case_id}>
                {uc.use_case_id}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm mb-1">Tenant slug</label>
          <input
            value={tenant}
            onChange={(e) => setTenant(e.target.value)}
            className="w-full border rounded px-2 py-1 text-sm"
            placeholder="contoso-prod"
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Wave</label>
          <select
            value={wave}
            onChange={(e) => setWave(e.target.value as any)}
            className="w-full border rounded px-2 py-1 text-sm"
            disabled={substrate === "laptop"}
          >
            <option value="w1">W1 — Foundation</option>
            <option value="w2">W2 — Pilot</option>
            <option value="w3">W3 — Scale & Fuse</option>
          </select>
        </div>

        <div>
          <label className="block text-sm mb-1">Operator (UPN)</label>
          <input
            value={operator}
            onChange={(e) => setOperator(e.target.value)}
            className="w-full border rounded px-2 py-1 text-sm"
            placeholder="operator@labtenant.onmicrosoft.com"
          />
        </div>

        <div className="text-sm border-t pt-2">
          <div className="font-medium mb-1">Selection</div>
          <ul className="text-gray-700 text-xs">
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
            ? "1. Render docker-compose.yml"
            : "1. Render Bicep parameters"}
        </button>

        {rendered && (
          <div className="border-t pt-3 space-y-2">
            <div className="text-sm font-medium">
              Format: <code className="text-xs">{rendered.format}</code>
            </div>
            <details>
              <summary className="text-xs cursor-pointer">Rendered output</summary>
              <pre className="text-xs bg-white border rounded p-2 overflow-auto max-h-48 mt-1">
                {rendered.format === "docker-compose"
                  ? rendered.compose_yaml
                  : JSON.stringify(rendered.parameters, null, 2)}
              </pre>
            </details>

            {gateReport && (
              <div className={`text-xs border rounded p-2 ${STATUS_COLOR[gateReport.overall_status]}`}>
                <div className="font-medium">
                  Security Gates: {gateReport.overall_status.toUpperCase()}
                  {" · "}deploy_allowed: {String(gateReport.deploy_allowed)}
                </div>
                {gateReport.red_gates.length > 0 && (
                  <div className="mt-1">
                    Red: {gateReport.red_gates.join(", ")}
                  </div>
                )}
                <details className="mt-1">
                  <summary className="cursor-pointer">All 15 gates</summary>
                  <ul className="mt-1 text-[11px]">
                    {gateReport.gates.map((g) => (
                      <li key={g.gate_id} className="py-0.5">
                        <span className={`inline-block px-1 rounded ${STATUS_COLOR[g.status]}`}>
                          {g.status}
                        </span>{" "}
                        <code>{g.gate_id}</code> {g.title}
                      </li>
                    ))}
                  </ul>
                </details>
              </div>
            )}

            {rendered.format === "bicep-parameters" && (
              <>
                <label className="flex items-center gap-2 text-xs cursor-pointer">
                  <input
                    type="checkbox"
                    checked={confirmDestructive}
                    onChange={(e) => setConfirmDestructive(e.target.checked)}
                  />
                  I have reviewed the diff and confirm destructive changes (if any)
                </label>

                <button
                  type="button"
                  disabled={!canDeploy}
                  onClick={onDeploy}
                  className="w-full bg-green-700 text-white rounded px-3 py-2 text-sm disabled:bg-gray-300"
                >
                  {deploying
                    ? "2. Deploying…"
                    : `2. Deploy via az (${substrate})`}
                </button>
                <p className="text-[11px] text-gray-500">
                  Calls <code>POST /api/deployments</code> · server runs PSG check →
                  what-if → apply via <code>apex_wizard.bicep_runner</code>. In mock
                  mode the runner returns synthetic results; in real mode it shells
                  out to <code>az deployment group create</code>.
                </p>
              </>
            )}

            {deployment && (
              <div className={`text-xs border rounded p-2 ${
                deployment.status === "succeeded"
                  ? STATUS_COLOR.green
                  : deployment.status === "failed"
                  ? STATUS_COLOR.red
                  : STATUS_COLOR.yellow
              }`}>
                <div className="font-medium">
                  Deployment: {deployment.status.toUpperCase()}
                </div>
                <div>id: <code className="text-[10px]">{deployment.id}</code></div>
                {deployment.audit_row_id && (
                  <div>audit row: <code className="text-[10px]">{deployment.audit_row_id}</code></div>
                )}
                {deployment.bicep_what_if_summary && (
                  <div>
                    what-if: {JSON.stringify(deployment.bicep_what_if_summary.counts)}
                    {" · "}mode: {deployment.bicep_what_if_summary.mode}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </aside>
    </section>
  );
}
