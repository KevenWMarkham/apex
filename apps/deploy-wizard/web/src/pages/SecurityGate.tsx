import { useEffect, useState } from "react";

const API_BASE = (import.meta as any).env?.VITE_API_URL ?? "";

type Gate = {
  gate_id: string;
  title: string;
  status: "green" | "yellow" | "red" | "unknown";
  evaluated_at: string;
  mode: string;
  rationale: string;
  remediate: string | null;
  blocking: boolean;
  metadata: Record<string, unknown>;
};

type Report = {
  tenant: string;
  overall_status: "green" | "yellow" | "red" | "unknown";
  deploy_allowed: boolean;
  red_gates: string[];
  gates: Gate[];
};

const STATUS_COLOR: Record<string, string> = {
  green: "text-green-700 bg-green-50 border-green-200",
  yellow: "text-amber-700 bg-amber-50 border-amber-200",
  red: "text-red-700 bg-red-50 border-red-200",
  unknown: "text-gray-700 bg-gray-50 border-gray-200",
};

const STATUS_BADGE: Record<string, string> = {
  green: "bg-green-600 text-white",
  yellow: "bg-amber-500 text-white",
  red: "bg-red-600 text-white",
  unknown: "bg-gray-500 text-white",
};

export default function SecurityGate() {
  const [tenant, setTenant] = useState("contoso-prod");
  const [report, setReport] = useState<Report | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [useCaseJson, setUseCaseJson] = useState(
    JSON.stringify(
      {
        use_case_id: "rc-e2e-05--bigbox-prod",
        substrate: "prod",
        personas_active: [{ id: "jamie-oconnor-store-manager" }],
        persona_principal_bindings: {
          "jamie-oconnor-store-manager": {
            binding_mode: "entra_group",
            entra_group_object_id: "8a3c1234-aaaa-bbbb-cccc-456789abcdef",
          },
        },
      },
      null,
      2,
    ),
  );

  const fetchReport = async (withContext = false) => {
    setLoading(true);
    setError(null);
    try {
      let res: Response;
      if (withContext) {
        let useCaseData: unknown = undefined;
        try {
          useCaseData = JSON.parse(useCaseJson);
        } catch (e: any) {
          throw new Error(`use_case_data JSON invalid: ${e.message}`);
        }
        res = await fetch(`${API_BASE}/api/security-gate/with-context`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ tenant, use_case_data: useCaseData }),
        });
      } else {
        res = await fetch(`${API_BASE}/api/security-gate?tenant=${encodeURIComponent(tenant)}`);
      }
      if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
      const data = (await res.json()) as Report;
      setReport(data);
    } catch (e: any) {
      setError(e.message ?? String(e));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport(false);
  }, []);

  useEffect(() => {
    if (!autoRefresh) return;
    const id = setInterval(() => fetchReport(false), 10000);
    return () => clearInterval(id);
  }, [autoRefresh, tenant]);

  return (
    <section className="space-y-4">
      <header>
        <h1 className="text-2xl font-bold">Pre-deployment Security Gate</h1>
        <p className="text-sm text-gray-600">
          Polls all 15 gates from <code>Pre-deployment-Security-Gate.md</code>. The
          wizard's deploy button is enabled only when no blocking gate is RED.
          PSG-15 (Sprint 47.6, persona-binding resolvability) requires the
          use-case data to evaluate; the others poll mock-green by default and
          swap to real-mode checks as Sprint 41–45 production-wiring lands.
        </p>
      </header>

      <div className="flex flex-wrap items-end gap-3 border rounded p-3 bg-gray-50">
        <div>
          <label className="block text-sm">Tenant slug</label>
          <input
            value={tenant}
            onChange={(e) => setTenant(e.target.value)}
            className="border rounded px-2 py-1 text-sm"
            placeholder="contoso-prod"
          />
        </div>
        <button
          onClick={() => fetchReport(false)}
          disabled={loading}
          className="bg-blue-600 text-white rounded px-3 py-1 text-sm disabled:bg-gray-300"
        >
          Poll all 15 gates
        </button>
        <button
          onClick={() => fetchReport(true)}
          disabled={loading}
          className="bg-purple-600 text-white rounded px-3 py-1 text-sm disabled:bg-gray-300"
          title="POST /api/security-gate/with-context — runs PSG-15 against the JSON below"
        >
          Poll w/ use-case context (PSG-15)
        </button>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => setAutoRefresh(e.target.checked)}
          />
          Auto-refresh every 10s
        </label>
      </div>

      {error && (
        <p className="text-sm text-red-700 border border-red-200 bg-red-50 rounded p-2">
          {error}
        </p>
      )}

      {report && (
        <div className={`border rounded p-3 ${STATUS_COLOR[report.overall_status]}`}>
          <div className="flex items-center gap-3">
            <span className={`px-2 py-0.5 rounded text-sm font-bold ${STATUS_BADGE[report.overall_status]}`}>
              {report.overall_status.toUpperCase()}
            </span>
            <span className="font-medium">tenant: {report.tenant}</span>
            <span className="text-sm">
              deploy_allowed: <code>{String(report.deploy_allowed)}</code>
            </span>
            {report.red_gates.length > 0 && (
              <span className="text-sm">
                red gates: <code>{report.red_gates.join(", ")}</code>
              </span>
            )}
          </div>
        </div>
      )}

      <details className="border rounded p-3">
        <summary className="cursor-pointer font-medium text-sm">
          Use-case data for PSG-15 evaluation (editable JSON)
        </summary>
        <textarea
          value={useCaseJson}
          onChange={(e) => setUseCaseJson(e.target.value)}
          rows={14}
          className="w-full border rounded p-2 mt-2 text-xs font-mono"
        />
        <p className="text-xs text-gray-500 mt-1">
          Edit the JSON to test PSG-15 transitions: substrate=laptop → green;
          substrate=prod without bindings → red; substrate=prod with bindings → green.
        </p>
      </details>

      {report && (
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="border-b font-medium">
              <th className="text-left p-2">Gate</th>
              <th className="text-left p-2">Title</th>
              <th className="text-left p-2">Status</th>
              <th className="text-left p-2">Mode</th>
              <th className="text-left p-2">Blocking</th>
              <th className="text-left p-2">Rationale / Remediate</th>
            </tr>
          </thead>
          <tbody>
            {report.gates.map((g) => (
              <tr key={g.gate_id} className="border-b align-top">
                <td className="p-2 font-mono text-xs">{g.gate_id}</td>
                <td className="p-2">{g.title}</td>
                <td className="p-2">
                  <span className={`px-2 py-0.5 rounded text-xs ${STATUS_BADGE[g.status]}`}>
                    {g.status}
                  </span>
                </td>
                <td className="p-2 text-xs text-gray-600">{g.mode}</td>
                <td className="p-2 text-xs">{g.blocking ? "yes" : "warn-only"}</td>
                <td className="p-2 text-xs">
                  <div>{g.rationale}</div>
                  {g.remediate && (
                    <div className="text-gray-600 mt-1">↳ {g.remediate}</div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
