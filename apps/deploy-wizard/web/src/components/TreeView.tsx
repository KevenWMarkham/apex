import { useMemo, useState } from "react";

export type BuildStatus =
  | "planned"
  | "scaffolded"
  | "implemented"
  | "deployed"
  | "pilot"
  | "ga";

export type TreeNode = {
  id: string;
  kind: "practice" | "service" | "scenario" | "agent";
  label: string;
  children: TreeNode[];
  // optional metadata used in tooltips / detail panes
  service_code?: string;
  industry?: string;
  domain?: string;
  domains?: string[];
  scenario_id?: string;
  role?: string;
  description?: string;
  hitl_gate?: boolean;
  kpi?: string;
  scenario_count?: number;
  service_count?: number;
  status?: BuildStatus;
  has_plan?: boolean;
};

const STATUS_BADGE: Record<BuildStatus, { label: string; className: string }> = {
  planned:     { label: "planned",     className: "text-gray-700 bg-gray-100 border-gray-300" },
  scaffolded:  { label: "scaffolded",  className: "text-cyan-700 bg-cyan-50 border-cyan-200" },
  implemented: { label: "built",       className: "text-indigo-700 bg-indigo-50 border-indigo-200" },
  deployed:    { label: "deployed",    className: "text-green-700 bg-green-50 border-green-200" },
  pilot:       { label: "pilot",       className: "text-amber-700 bg-amber-50 border-amber-200" },
  ga:          { label: "GA",          className: "text-emerald-700 bg-emerald-50 border-emerald-300 font-semibold" },
};

type Props = {
  nodes: TreeNode[];
  selectedIds: Set<string>;
  onChange: (next: Set<string>) => void;
};

/** Collect the ids of `node` and every descendant. */
function collectIds(node: TreeNode, out: string[] = []): string[] {
  out.push(node.id);
  node.children.forEach((c) => collectIds(c, out));
  return out;
}

/** Tri-state for a node based on selectedIds:
 *  - "all"      → node + every descendant in selectedIds
 *  - "partial"  → some descendants in selectedIds
 *  - "none"     → none in selectedIds
 *  Leaf nodes are "all" or "none".
 */
function nodeState(node: TreeNode, selected: Set<string>): "all" | "partial" | "none" {
  const ids = collectIds(node);
  const hits = ids.filter((id) => selected.has(id));
  if (hits.length === 0) return "none";
  if (hits.length === ids.length) return "all";
  return "partial";
}

const KIND_BADGE: Record<TreeNode["kind"], string> = {
  practice: "Practice",
  service: "Service",
  scenario: "Scenario",
  agent: "Agent",
};

const KIND_COLOR: Record<TreeNode["kind"], string> = {
  practice: "text-blue-700 bg-blue-50 border-blue-200",
  service: "text-purple-700 bg-purple-50 border-purple-200",
  scenario: "text-emerald-700 bg-emerald-50 border-emerald-200",
  agent: "text-amber-700 bg-amber-50 border-amber-200",
};

function Row({
  node,
  depth,
  selected,
  onChange,
  expanded,
  toggleExpanded,
}: {
  node: TreeNode;
  depth: number;
  selected: Set<string>;
  onChange: (next: Set<string>) => void;
  expanded: Set<string>;
  toggleExpanded: (id: string) => void;
}) {
  const state = nodeState(node, selected);
  const hasChildren = node.children.length > 0;
  const isOpen = expanded.has(node.id);

  const onToggleSelect = () => {
    const next = new Set(selected);
    const ids = collectIds(node);
    if (state === "all") {
      ids.forEach((id) => next.delete(id));
    } else {
      ids.forEach((id) => next.add(id));
    }
    onChange(next);
  };

  const sub =
    node.kind === "practice"
      ? `${node.service_count ?? node.children.length} service${
          (node.children.length ?? 0) === 1 ? "" : "s"
        }`
      : node.kind === "service"
      ? `${node.scenario_count ?? node.children.length} scenario${
          (node.children.length ?? 0) === 1 ? "" : "s"
        }${node.domains?.length ? ` · ${node.domains.join(", ")}` : ""}`
      : node.kind === "scenario"
      ? node.kpi || node.domain || ""
      : node.description || (node.hitl_gate ? "HITL gate" : "");

  return (
    <li>
      <div
        className="flex items-center gap-2 py-1 hover:bg-gray-50 rounded px-1"
        style={{ paddingLeft: depth * 16 }}
      >
        {hasChildren ? (
          <button
            type="button"
            onClick={() => toggleExpanded(node.id)}
            className="w-4 text-gray-500 hover:text-gray-900"
            aria-label={isOpen ? "Collapse" : "Expand"}
          >
            {isOpen ? "▾" : "▸"}
          </button>
        ) : (
          <span className="w-4" />
        )}

        <input
          type="checkbox"
          checked={state === "all"}
          ref={(el) => {
            if (el) el.indeterminate = state === "partial";
          }}
          onChange={onToggleSelect}
          className="cursor-pointer"
        />

        <span
          className={`text-xs px-1.5 py-0.5 rounded border ${KIND_COLOR[node.kind]}`}
        >
          {KIND_BADGE[node.kind]}
        </span>

        <span className="font-mono text-sm text-gray-900">{node.label}</span>

        {node.status && node.kind !== "practice" && (
          <span
            className={`text-[10px] uppercase tracking-wide px-1.5 py-0.5 rounded border ${STATUS_BADGE[node.status].className}`}
            title={`Build status: ${node.status}`}
          >
            {STATUS_BADGE[node.status].label}
          </span>
        )}

        {sub && <span className="text-xs text-gray-500 truncate">— {sub}</span>}
      </div>

      {hasChildren && isOpen && (
        <ul>
          {node.children.map((c) => (
            <Row
              key={c.id}
              node={c}
              depth={depth + 1}
              selected={selected}
              onChange={onChange}
              expanded={expanded}
              toggleExpanded={toggleExpanded}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

export default function TreeView({ nodes, selectedIds, onChange }: Props) {
  const [expanded, setExpanded] = useState<Set<string>>(
    () => new Set(nodes.map((n) => n.id))
  );

  const toggleExpanded = (id: string) => {
    const next = new Set(expanded);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setExpanded(next);
  };

  const counts = useMemo(() => {
    const c = { practice: 0, service: 0, scenario: 0, agent: 0 };
    selectedIds.forEach((id) => {
      const kind = id.split(":")[0] as TreeNode["kind"];
      if (c[kind] !== undefined) c[kind]++;
    });
    return c;
  }, [selectedIds]);

  return (
    <div className="border rounded p-2 bg-white">
      <div className="flex items-center justify-between border-b pb-2 mb-2 text-sm">
        <span className="font-medium">Catalog</span>
        <span className="text-gray-600">
          Selected: {counts.practice}P · {counts.service}S · {counts.scenario}sc · {counts.agent}A
        </span>
      </div>
      <ul>
        {nodes.map((n) => (
          <Row
            key={n.id}
            node={n}
            depth={0}
            selected={selectedIds}
            onChange={onChange}
            expanded={expanded}
            toggleExpanded={toggleExpanded}
          />
        ))}
      </ul>
    </div>
  );
}
