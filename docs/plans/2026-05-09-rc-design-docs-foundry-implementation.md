# RC Design Docs + Foundry Runtime — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the persona/KPI/use-case registry layer, scaffold service/scenario/agent/use-case `DESIGN.md` files, hand-author the RC-E2E-03 worked example, migrate Bicep agent-fleet to Foundry Hosted Agents, surface use cases in the wizard, and cross-link the books — all on `main`.

**Architecture:** Microsoft hybrid (Path C). Foundry Hosted Agents = Layer 3. Container Apps stays for MCP servers and wizard. AVM `ai-foundry` Bicep module = Foundry IaC. Use Case is the per-client variability layer above Service. See [docs/plans/2026-05-09-rc-design-docs-foundry-design.md](2026-05-09-rc-design-docs-foundry-design.md).

**Tech Stack:** Python 3.12 (generator + FastAPI), Pydantic 2.x, PyYAML, React 19 + TS (wizard web), Bicep (IaC), Foundry Agent Service (runtime).

**Working dir:** `C:\Stage\Clients\Industries\APEX\` (main branch — no worktree).

---

## Pre-flight

**Run before starting:**

```powershell
cd C:\Stage\Clients\Industries\APEX
git status
git log --oneline -5
```

Expected: working tree shows only the `docs/plans/2026-05-09-rc-design-docs-foundry-design.md` recently committed plus any unrelated WIP from prior sessions. Recent commit: `7568fb8 docs(plan): RC design docs + Foundry-aligned runtime design`.

---

## Phase A — Registries

### Task A1: Author `services/_personas.yaml`

**Files:**
- Create: `services/_personas.yaml`

**Step 1:** Write the persona registry covering every persona named in Services Guide §18 (RC chapter). At minimum: `marisol-reyes-store-ops`, `daniel-chen-merch-director`, `jamie-oconnor-store-manager`, `rebecca-hall-returns-ops-mgr`, `maya-patel-loyalty-crm-director`. Each entry has: `label`, `role`, `level`, `org`, `hitl_authority` (list), `default_kpis` (list of KPI ids), `used_by_services` (list of service codes), `notes` (free text with §18.x reference). Schema matches design doc §6.1.

**Step 2:** Validate YAML loads:
```powershell
python -c "import yaml; d=yaml.safe_load(open(r'services/_personas.yaml',encoding='utf-8')); print(len(d), 'personas:', list(d.keys()))"
```
Expected: 5+ personas listed by id.

**Step 3:** Commit.
```powershell
git add services/_personas.yaml
git commit -m "feat(services): add framework-level persona registry"
```

---

### Task A2: Author `services/_kpis.yaml`

**Files:**
- Create: `services/_kpis.yaml`

**Step 1:** Write the KPI registry covering every KPI in Services Guide §18 RC envelopes. At minimum: `gm-pp-lift`, `doh-reduction-pct`, `markdown-to-clear-pct`, `shrink-cost-reduction-pct`, `decision-loop-time-sec`, `churn-rate-reduction-pct`, `winback-response-pp`, `ltv-lift-pct`, `oos-reduction-pct`, `sales-per-sqft-pct`, `associate-productivity-pct`, `fraud-detection-rate-pct`, `recovered-loss-usd`, `false-positive-rate-pct`. Each entry: `label`, `unit`, `formula_ref` (Gold mart column), `attribution_path`, `default_persona` (id), `used_by_services` (list).

**Step 2:** Validate:
```powershell
python -c "import yaml; d=yaml.safe_load(open(r'services/_kpis.yaml',encoding='utf-8')); print(len(d), 'kpis:', list(d.keys()))"
```
Expected: 14+ KPI ids.

**Step 3:** Commit.
```powershell
git add services/_kpis.yaml
git commit -m "feat(services): add framework-level KPI registry"
```

---

### Task A3: Loader + cross-ref validator in `apex_wizard.registry`

**Files:**
- Modify: `apps/deploy-wizard/api/src/apex_wizard/registry.py`

**Step 1:** Add `PERSONAS_PATH = SERVICES_ROOT / "_personas.yaml"` and `KPIS_PATH = SERVICES_ROOT / "_kpis.yaml"`. Add `load_personas()` and `load_kpis()` (both `@lru_cache(maxsize=1)`). Add `validate_refs(personas, kpis, use_cases) -> list[str]` returning a list of dangling-ref error strings.

**Step 2:** Add a quick smoke test inline:
```powershell
python -c "
import sys; sys.path.insert(0, r'apps/deploy-wizard/api/src')
from apex_wizard import registry
print('personas:', len(registry.load_personas()))
print('kpis:', len(registry.load_kpis()))
"
```
Expected: counts match A1 / A2.

**Step 3:** Commit.
```powershell
git add apps/deploy-wizard/api/src/apex_wizard/registry.py
git commit -m "feat(wizard-api): persona + KPI loaders with ref validator"
```

---

## Phase B — Use Case schema + default scaffolds

### Task B1: Document the use-case schema in `services/_use-case.schema.md`

**Files:**
- Create: `services/_use-case.schema.md`

**Step 1:** Write the schema documentation: every field from design doc §5.1 with type, required/optional, allowed values, example. Include a worked example for `contoso-rc-e2e-03-na-pilot`. Footer cross-links to `docs/plans/2026-05-09-rc-design-docs-foundry-design.md`.

**Step 2:** Commit.
```powershell
git add services/_use-case.schema.md
git commit -m "docs(services): document use-case YAML schema"
```

---

### Task B2: Extend generator to scaffold `use-cases/_default/use-case.yaml` per service

**Files:**
- Modify: `tools/gen_services_tree.py`

**Step 1:** Add `_default_use_case_for(service_row, frow_for_featured)` that returns a dict matching the schema, populated from xlsx + Services Guide §18 envelope. Personas + KPIs reference ids from the registries. Substrate = `lab`. Tenant + image-tag fields = `REPLACE_*` placeholders.

**Step 2:** In the per-service-code loop, write `services/{ind}/{code}/use-cases/_default/use-case.yaml` via `write_if_missing`.

**Step 3:** Run generator:
```powershell
python tools/gen_services_tree.py
```
Expected: `OK industries=7 services=38 scenarios=724 featured=36`.

**Step 4:** Verify file landed:
```powershell
Get-Content services/rc/RC-E2E-03/use-cases/_default/use-case.yaml | Select-Object -First 25
```
Expected: yaml header + service_code: RC-E2E-03 + personas list with ids matching `_personas.yaml`.

**Step 5:** Commit.
```powershell
git add tools/gen_services_tree.py services/
git commit -m "feat(generator): scaffold default use-case per service"
```

---

## Phase C — DESIGN.md scaffolding

### Task C1: Generator scaffolds service-level `DESIGN.md`

**Files:**
- Modify: `tools/gen_services_tree.py`

**Step 1:** Add `_render_service_design(svc, ind_label, services_guide_anchor)` returning a markdown body. Must include: title, overview (1 paragraph from xlsx Domain + Brief aggregated), the canonical Service Guide §18.x anchor link, table of featured scenarios, persona list (resolved from `_personas.yaml`), KPI list (resolved from `_kpis.yaml`), agent fleet (resolved from `_extras.yaml` merge), MCP tool surface, Bicep references (point to `infra/bicep/modules/service.bicep`), Foundry config block (project ref placeholder), TODO markers where hand-authoring is expected, and a "References" footer with Services Guide / Deployment Guide / Microsoft Learn / `docs/plans/` design doc links.

**Step 2:** In the per-service-code loop, write `services/{ind}/{code}/DESIGN.md` via `write_if_missing`.

**Step 3:** Run generator. Spot-check:
```powershell
python tools/gen_services_tree.py
Get-Content services/rc/RC-E2E-04/DESIGN.md | Select-Object -First 50
```
Expected: rendered markdown with RC-E2E-04 details from xlsx; footer links present.

**Step 4:** Commit.
```powershell
git add tools/gen_services_tree.py services/
git commit -m "feat(generator): scaffold service-level DESIGN.md"
```

---

### Task C2: Generator scaffolds scenario-level `DESIGN.md`

**Files:**
- Modify: `tools/gen_services_tree.py`

**Step 1:** Add `_render_scenario_design(frow, chain_24_steps, ind_slug)` rendering: title (from `Title`), the moment, solution, full 24-step chain table from `chain_24_steps`, personas active (resolved from `_personas.yaml` matching the xlsx personas string), KPI envelope (resolved from `_kpis.yaml`), HITL behavior placeholder, cross-Service notes, References footer.

**Step 2:** In the featured-scenario loop, write `scenarios/{sid}/DESIGN.md` via `write_if_missing`.

**Step 3:** Run generator + spot-check:
```powershell
python tools/gen_services_tree.py
Get-Content services/rc/RC-E2E-04/scenarios/rc-loyalty-churn-prediction-winback/DESIGN.md | Select-Object -First 60
```
Expected: rendered scenario design with 24-step table.

**Step 4:** Commit.
```powershell
git add tools/gen_services_tree.py services/
git commit -m "feat(generator): scaffold scenario-level DESIGN.md"
```

---

### Task C3: Generator scaffolds agent-level `DESIGN.md`

**Files:**
- Modify: `tools/gen_services_tree.py`

**Step 1:** Add `_render_agent_design(role_meta, scenario_meta, service_code)` rendering: title (the agent's label), role description (from `_extras.yaml` description if present, else canonical from agent registry), prompt strategy section (TODO marker with template hints), tools list (placeholder list referencing service-level MCP tool naming), schemas read/write (TODO), HITL behavior (whether `hitl_gate` is true), persona served (resolved by role → persona heuristic where possible: `decide`/`act` → operator persona; `pricing` → merchandising; etc.), Foundry hosted-agent config block (image-tag placeholder, model placeholder), References footer.

**Step 2:** In the per-role-per-scenario loop, write `agents/{role}/DESIGN.md` via `write_if_missing`.

**Step 3:** Run generator + spot-check Pricer + a default role:
```powershell
python tools/gen_services_tree.py
Get-Content services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/agents/pricing/DESIGN.md | Select-Object -First 40
Get-Content services/rc/RC-E2E-04/scenarios/rc-loyalty-churn-prediction-winback/agents/decide/DESIGN.md | Select-Object -First 40
```
Expected: both render valid markdown; The Pricer description from `_extras.yaml` flows through.

**Step 4:** Commit.
```powershell
git add tools/gen_services_tree.py services/
git commit -m "feat(generator): scaffold agent-level DESIGN.md"
```

---

### Task C4: Generator scaffolds default use-case `DESIGN.md` + centralized service `index.md`

**Files:**
- Modify: `tools/gen_services_tree.py`

**Step 1:** Add `_render_use_case_design(use_case_yaml, service_meta)` and write `services/{ind}/{code}/use-cases/_default/DESIGN.md` via `write_if_missing`.

**Step 2:** Add `_render_service_index(svc_meta)` rendering the centralized architecture-view narrative with a link table to every co-located `DESIGN.md`. Write `docs/APEX - Design and Build/services/{code}/index.md` via `write_if_missing`.

**Step 3:** Run generator + verify:
```powershell
python tools/gen_services_tree.py
ls "docs/APEX - Design and Build/services/RC-E2E-03"
ls services/rc/RC-E2E-03/use-cases/_default
```
Expected: `index.md` in centralized dir; both `use-case.yaml` and `DESIGN.md` in default dir.

**Step 4:** Commit.
```powershell
git add tools/gen_services_tree.py "docs/APEX - Design and Build/services" services
git commit -m "feat(generator): scaffold use-case DESIGN.md + centralized service index.md"
```

---

### Task C5: Generator validates persona + KPI refs; fails loud on dangling

**Files:**
- Modify: `tools/gen_services_tree.py`

**Step 1:** After all writes complete, walk every generated `use-case.yaml` and resolve `personas_active[].id` against `_personas.yaml` and `kpis_targeted[].id` against `_kpis.yaml`. Collect dangling refs.

**Step 2:** If any dangling, print to stderr and exit non-zero.

**Step 3:** Verify by introducing a deliberate dangling ref, running, observing failure:
```powershell
# (manually: edit one use-case.yaml to add a non-existent persona id)
python tools/gen_services_tree.py
# Expected: non-zero exit, dangling ref printed
# Then revert the edit.
python tools/gen_services_tree.py
# Expected: clean run.
```

**Step 4:** Commit.
```powershell
git add tools/gen_services_tree.py
git commit -m "feat(generator): validate persona + KPI refs in use-cases"
```

---

## Phase D — Hand-authored RC-E2E-03 worked example

### Task D1: Hand-author `services/rc/RC-E2E-03/DESIGN.md`

**Files:**
- Modify: `services/rc/RC-E2E-03/DESIGN.md`

**Step 1:** Replace the generated template with a rich service-level narrative covering: full envelope from Services Guide §18.1, Foundry project layout (Foundry hub × project × hosted agents), agent fleet with The Pricer's role explained per Services Guide §25.8, MCP tool surface with each tool's purpose, cross-Service consumption (rc_e2e_09.get_lot_provenance), audit-row chain per Deployment Guide §11, Bicep deploy walk-through pointing at `infra/bicep/blueprints/w2-pilot.bicep`. References footer with all Microsoft Learn URLs from §13 of design doc.

**Step 2:** Re-run generator (must skip overwrite):
```powershell
python tools/gen_services_tree.py
Get-Content services/rc/RC-E2E-03/DESIGN.md | Measure-Object -Line
```
Expected: line count > 200 (hand-authored is long); content unchanged from step 1.

**Step 3:** Commit.
```powershell
git add services/rc/RC-E2E-03/DESIGN.md
git commit -m "docs(rc): rich service DESIGN.md for RC-E2E-03 (worked example)"
```

---

### Task D2: Hand-author cold-chain scenario `DESIGN.md`

**Files:**
- Modify: `services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/DESIGN.md`

**Step 1:** Replace template with rich scenario narrative: the moment in detail (Big Box Store 100, 47 minutes, dairy case), the operator decision, all 24 steps explained with `What APEX Does`, persona binding (Marisol Reyes = operator with HITL authority on destroy/markdown), KPI realization path, Services Guide §14.3 worked-example cross-link, audit-row trace.

**Step 2:** Commit.
```powershell
git add services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/DESIGN.md
git commit -m "docs(rc): rich scenario DESIGN.md for cold-chain-excursion"
```

---

### Task D3: Hand-author The Pricer `DESIGN.md`

**Files:**
- Modify: `services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/agents/pricing/DESIGN.md`

**Step 1:** Replace template with The Pricer's full design: role per Services Guide §18.1 (Pricing Agent paragraph), prompt strategy (elasticity + competitor + floor/MAP), MCP tools (`rc_e2e_03.get_pricing_recommendation_basis`, `get_similar_pricing_decisions`), schemas read (PROML.Pricing, PROML.DiscountRule, MERML.Elasticity), HITL behavior (markdown > 30%), Year-1 → Year-3 evolution per Services Guide §25.8 (LEDGER + Redis episodic memory), Foundry hosted-agent config block (model gpt-4o-2024-11-20, agent-framework runtime), input/output JSON schema sketches.

**Step 2:** Commit.
```powershell
git add services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/agents/pricing/DESIGN.md
git commit -m "docs(rc): rich agent DESIGN.md for The Pricer"
```

---

### Task D4: Hand-author RC-E2E-03 default `use-case.yaml` + `DESIGN.md`

**Files:**
- Modify: `services/rc/RC-E2E-03/use-cases/_default/use-case.yaml`
- Modify: `services/rc/RC-E2E-03/use-cases/_default/DESIGN.md`

**Step 1:** Replace `use-case.yaml` placeholders with the canonical Services Guide §18.1 envelope rendered as a deployable use case (Marisol + Daniel as personas; GM +3.2pp / DoH −28% / MtC +41% as KPI targets; HITL thresholds from §18.1; Foundry block populated).

**Step 2:** Author the matching `DESIGN.md` narrative explaining how a client extends this `_default` to fit their data environment.

**Step 3:** Commit.
```powershell
git add services/rc/RC-E2E-03/use-cases/_default
git commit -m "docs(rc): default use case for RC-E2E-03 (canonical envelope)"
```

---

### Task D5: Hand-author centralized `docs/APEX - Design and Build/services/RC-E2E-03/index.md`

**Files:**
- Modify: `docs/APEX - Design and Build/services/RC-E2E-03/index.md`

**Step 1:** Replace template with full architectural narrative: chain (KPI ← Persona ← Use Case ← Scenario ← Service ← Agents ← Foundry ← Bicep ← Tenant) walked top-down, link table to every co-located `DESIGN.md` under `services/rc/RC-E2E-03/`, link to Services Guide §18.1 anchor, link to Deployment Guide §7 anchor for service module shape, link to RC-Build-Plan.md sprint-31/32/33 items, link to design doc.

**Step 2:** Commit.
```powershell
git add "docs/APEX - Design and Build/services/RC-E2E-03/index.md"
git commit -m "docs(rc): centralized service narrative for RC-E2E-03"
```

---

## Phase E — Bicep Foundry migration

### Task E1: Extend `platform/main.bicep` with Foundry account + project

**Files:**
- Modify: `infra/bicep/platform/main.bicep`
- Create: `infra/bicep/platform/foundry.bicep`

**Step 1:** Create `platform/foundry.bicep` that wraps the AVM module `br/public:avm/ptn/ai-ml/ai-foundry:<pinned-version>` for Foundry account + project + Standard Agent Services. Inputs: `tenant`, `location`, `tags`, `agentIdentityPrincipalId`. Outputs: `foundryAccountId`, `foundryProjectId`, `foundryProjectEndpoint`.

**Step 2:** In `platform/main.bicep`, add `module foundry 'foundry.bicep' = { ... }` and surface its outputs alongside identity / ledger / monitoring outputs.

**Step 3:** Lint:
```powershell
az bicep build --file infra/bicep/platform/main.bicep --stdout > $null 2>&1
echo "exit: $LASTEXITCODE"
```
Expected: exit 0 (no Bicep compile errors). If `az` CLI not available, skip lint and accept TODO comment.

**Step 4:** Commit.
```powershell
git add infra/bicep/platform/
git commit -m "feat(bicep): extend platform with Foundry account + project (AVM)"
```

---

### Task E2: Rewrite `agent-fleet.bicep` to deploy Foundry hosted agents

**Files:**
- Modify: `infra/bicep/modules/agent-fleet.bicep`

**Step 1:** Replace the loop over `Microsoft.App/containerApps` with a loop over `Microsoft.CognitiveServices/accounts/projects/agents` (Foundry hosted agent definitions). Same params (`tenant`, `serviceCode`, `scenarioId`, `wave`, `agentIdentityId`); add `foundryProjectId`, `agentImage` (container image tag for hosted-agent payload), `model`. Per-role config picks role from input array. Tag every resource with `apex-tenant`, `apex-service`, `apex-scenario`, `apex-agent-role`, `apex-wave` for drift detection.

**Step 2:** Lint:
```powershell
az bicep build --file infra/bicep/modules/agent-fleet.bicep --stdout > $null 2>&1
echo "exit: $LASTEXITCODE"
```
Expected: exit 0.

**Step 3:** Commit.
```powershell
git add infra/bicep/modules/agent-fleet.bicep
git commit -m "feat(bicep): agent-fleet deploys Foundry hosted agents (Path C)"
```

---

### Task E3: Adjust `service.bicep` and blueprints to thread `foundryProjectId`

**Files:**
- Modify: `infra/bicep/modules/service.bicep`
- Modify: `infra/bicep/blueprints/w2-pilot.bicep`
- Modify: `infra/bicep/blueprints/w3-scale-fuse.bicep`
- Modify: `infra/bicep/blueprints/w1-foundation.bicep`

**Step 1:** Add `foundryProjectId` param to `service.bicep`; remove `containerAppsEnvId` for the agent path (keep for MCP servers). Pass `foundryProjectId` into the agent-fleet module call.

**Step 2:** In `w2-pilot.bicep` and `w3-scale-fuse.bicep`, accept `foundryProjectId` from upstream platform output, thread to service modules.

**Step 3:** In `w1-foundation.bicep`, surface `foundryProjectId` as an output.

**Step 4:** Lint each:
```powershell
foreach ($f in @('infra/bicep/modules/service.bicep','infra/bicep/blueprints/w1-foundation.bicep','infra/bicep/blueprints/w2-pilot.bicep','infra/bicep/blueprints/w3-scale-fuse.bicep')) { az bicep build --file $f --stdout > $null 2>&1; echo "$f exit: $LASTEXITCODE" }
```
Expected: every file exits 0.

**Step 5:** Commit.
```powershell
git add infra/bicep/modules/service.bicep infra/bicep/blueprints/
git commit -m "feat(bicep): thread foundryProjectId through service + blueprints"
```

---

## Phase F — Wizard surface

### Task F1: `/api/catalog/use-cases` endpoint

**Files:**
- Modify: `apps/deploy-wizard/api/src/apex_wizard/registry.py`
- Modify: `apps/deploy-wizard/api/src/apex_wizard/catalog.py`

**Step 1:** In `registry.py`, add `load_use_cases(service_code: str | None) -> list[dict]` that reads every `services/{ind}/{code}/use-cases/*/use-case.yaml`. Cache it. Return list of dicts with each use-case's content + `service_code` + `slug` fields.

**Step 2:** In `catalog.py`, add:
```python
@router.get("/use-cases")
def list_use_cases(service: str | None = Query(default=None)) -> list[dict]:
    return registry.load_use_cases(service_code=service)
```

**Step 3:** Smoke:
```powershell
python -c "
import sys; sys.path.insert(0, r'apps/deploy-wizard/api/src')
from apex_wizard.main import app
from fastapi.testclient import TestClient
c = TestClient(app)
r = c.get('/api/catalog/use-cases?service=RC-E2E-03')
print(r.status_code, len(r.json()))
"
```
Expected: 200 + 1 (the `_default`).

**Step 4:** Commit.
```powershell
git add apps/deploy-wizard/api/src/apex_wizard/
git commit -m "feat(wizard-api): /api/catalog/use-cases endpoint"
```

---

### Task F2: Tree adds use-case node between service and scenario

**Files:**
- Modify: `apps/deploy-wizard/api/src/apex_wizard/registry.py`

**Step 1:** In `tree()`, when a service has 1+ use cases, group its scenarios under a use-case node `{id: "use-case:{slug}", kind: "use-case", label, status, children: scenario_nodes}`. If no use cases exist, fall back to current behavior (scenarios direct under service).

**Step 2:** Smoke:
```powershell
python -c "
import sys; sys.path.insert(0, r'apps/deploy-wizard/api/src')
from apex_wizard import registry
t = registry.tree(featured_only=True)
rc = next(p for p in t if p['industry']=='rc')
e203 = next(s for s in rc['children'] if s['service_code']=='RC-E2E-03')
for child in e203['children']:
    print(child['kind'], child['id'], '->', len(child.get('children',[])))
"
```
Expected: a `use-case` node containing the 2 scenarios.

**Step 3:** Commit.
```powershell
git add apps/deploy-wizard/api/src/apex_wizard/registry.py
git commit -m "feat(wizard-api): use-case node in tree between service and scenario"
```

---

### Task F3: TreeView frontend handles `kind: 'use-case'`

**Files:**
- Modify: `apps/deploy-wizard/web/src/components/TreeView.tsx`

**Step 1:** Extend `TreeNode["kind"]` union to include `"use-case"`. Add `KIND_BADGE["use-case"] = "Use Case"` and `KIND_COLOR["use-case"] = "text-orange-700 bg-orange-50 border-orange-200"`. The component is already kind-agnostic, so just the color/badge map adds.

**Step 2:** Eyeball-verify shape via the API client smoke (no compile here unless `npm` available). Note: if Node tooling not present, this is build-only verification at deploy time.

**Step 3:** Commit.
```powershell
git add apps/deploy-wizard/web/src/components/TreeView.tsx
git commit -m "feat(wizard-web): TreeView renders use-case nodes"
```

---

### Task F4: Render endpoint accepts `use_case_id` and merges overrides

**Files:**
- Modify: `apps/deploy-wizard/api/src/apex_wizard/deployments.py`

**Step 1:** Add optional `use_case_id: str | None = None` to `TreeSelection`. In `render_parameters`, if set, load the matching use-case YAML and merge: `agent_overrides` → `agentRoleOverrides`, `hitl_thresholds` → wired via Key Vault refs, `foundry.project_ref` → top-level Bicep param. Selection ids prefixed with `use-case:` are also accepted as inheritance triggers (selecting a use case inherits all its scenarios).

**Step 2:** Smoke:
```powershell
python -c "
import sys; sys.path.insert(0, r'apps/deploy-wizard/api/src')
from apex_wizard.main import app
from fastapi.testclient import TestClient
c = TestClient(app)
r = c.post('/api/deployments/render', json={
  'selected_ids': ['service:RC-E2E-03'],
  'tenant': 'contoso',
  'wave': 'w2',
  'use_case_id': 'rc-e2e-03--default'
})
print(r.status_code)
print(r.json()['summary'])
"
```
Expected: 200; summary includes use_case context.

**Step 3:** Commit.
```powershell
git add apps/deploy-wizard/api/src/apex_wizard/deployments.py
git commit -m "feat(wizard-api): render merges use-case overrides into Bicep params"
```

---

## Phase G — Book updates

### Task G1: Deployment Guide ch 1 — Layer 3 description rewrite

**Files:**
- Modify: `docs/book/Professional-APEX-Deployment-Guide.html`

**Step 1:** Find the Chapter 1 Layer 3 description block (Layer 3 paragraph + supporting cells in the SVG). Replace "Container image deployed as Container App" with the Foundry Hosted Agents narrative. Add inline link to [Foundry Hosted Agents docs](https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent) and the [Foundry baseline reference](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat).

**Step 2:** Verify HTML still parses (no broken tags):
```powershell
python -c "
import xml.etree.ElementTree as ET
import re
content = open(r'docs/book/Professional-APEX-Deployment-Guide.html', encoding='utf-8').read()
# count opens vs closes for <article>
print('article opens:', len(re.findall(r'<article\b', content)))
print('article closes:', len(re.findall(r'</article>', content)))
"
```
Expected: opens == closes.

**Step 3:** Commit.
```powershell
git add docs/book/Professional-APEX-Deployment-Guide.html
git commit -m "docs(deploy-guide): ch 1 Layer 3 = Foundry Hosted Agents (Path C)"
```

---

### Task G2: Deployment Guide ch 7 + new ch 11.5 + ch 9/10 cross-refs

**Files:**
- Modify: `docs/book/Professional-APEX-Deployment-Guide.html`

**Step 1:** In ch 7 service module skeleton, update the Bicep example to use Foundry resource types. Cite [AVM ai-foundry module](https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/ai-ml/ai-foundry).

**Step 2:** Add a new short ch 11.5 *"Layer 3 Surfacing via Foundry Agent Service"* after ch 11 — explains hosted-agent registration + M365 Copilot publishing path. Cites [Foundry Agent Service overview](https://learn.microsoft.com/azure/foundry/agents/overview).

**Step 3:** In ch 9 (HITL) and ch 10 (MCP), add inline footnotes citing the canonical Microsoft articles.

**Step 4:** Re-run open/close tag check from Task G1.

**Step 5:** Commit.
```powershell
git add docs/book/Professional-APEX-Deployment-Guide.html
git commit -m "docs(deploy-guide): ch 7 Bicep + new ch 11.5 Foundry surfacing + ch 9/10 cross-refs"
```

---

### Task G3: Services Guide ch 18 — add Use Cases sub-sections

**Files:**
- Modify: `docs/book/Professional-APEX-Services-Guide.html`

**Step 1:** Append a *"Use Cases"* sub-section to each of the 7 RC service profiles in ch 18 (`§18.1.x` through `§18.7.x`). Each lists representative use cases with persona × KPI × substrate variability. Link to `docs/APEX - Design and Build/services/{code}/index.md`.

**Step 2:** Tag-balance check.

**Step 3:** Commit.
```powershell
git add docs/book/Professional-APEX-Services-Guide.html
git commit -m "docs(services-guide): ch 18 RC services get Use Cases sub-sections"
```

---

### Task G4: Services Guide new ch 27 — Use Cases as the Variability Layer

**Files:**
- Modify: `docs/book/Professional-APEX-Services-Guide.html`

**Step 1:** Add new ch 27 explaining the persona/KPI/substrate model + the `use-case.yaml` schema. Show worked example using `services/rc/RC-E2E-03/use-cases/_default/use-case.yaml`. Note pattern repeats for HLS/ER/AXLE/TH/TMT/ICE.

**Step 2:** Tag-balance check.

**Step 3:** Commit.
```powershell
git add docs/book/Professional-APEX-Services-Guide.html
git commit -m "docs(services-guide): new ch 27 — Use Cases as the variability layer"
```

---

## Phase H — RC build plan + final wiring

### Task H1: Update `RC-Build-Plan.md` + `_build-status.yaml`

**Files:**
- Modify: `docs/APEX - Design and Build/RC-Build-Plan.md`
- Modify: `services/rc/_build-status.yaml`

**Step 1:** In `_build-status.yaml`, add to sprint-30 items: `30.7` (Provision Foundry Hub + Project per AVM module — `BL.P.91/92` + new) and `30.8` (Adopt MCP server pattern from `azmcp-foundry-aca-mi`). Add new sprint-31a (Use Case capture). Amend sprint-32 items mentioning Microsoft Agent Framework / LangGraph for hosted-agent code. Add sprint-33a items for hosted-agent registration smoke tests + M365 Copilot publishing dry-run. Mark scaffold items in sprint-31 as still done; add tasks under each that reflect the new DESIGN.md surface (one done item per service: "DESIGN.md scaffold generated" — yes, per service). 

**Step 2:** In `RC-Build-Plan.md`, mirror the YAML changes in human-readable form.

**Step 3:** Smoke:
```powershell
python -c "
import sys; sys.path.insert(0, r'apps/deploy-wizard/api/src')
from apex_wizard.main import app
from fastapi.testclient import TestClient
c = TestClient(app)
plan = c.get('/api/catalog/build-status?practice=rc').json()['practices'][0]
print('sprints:', len(plan['sprints']))
total = sum(len(s['items']) for s in plan['sprints'])
done = sum(sum(1 for i in s['items'] if i.get('done')) for s in plan['sprints'])
print(f'{done}/{total} done')
"
```
Expected: more sprints than 11; more items than 51; updated done count.

**Step 4:** Commit.
```powershell
git add "docs/APEX - Design and Build/RC-Build-Plan.md" services/rc/_build-status.yaml
git commit -m "docs(rc): build plan + status YAML updated for Foundry + use-case sprints"
```

---

### Task H2: End-to-end verification

**Files:**
- (no edits)

**Step 1:** Run all wizard endpoints in one go:
```powershell
python -c "
import sys; sys.path.insert(0, r'apps/deploy-wizard/api/src')
from apex_wizard.main import app
from fastapi.testclient import TestClient
c = TestClient(app)
print('health:', c.get('/health').json())
print('practices:', len(c.get('/api/catalog/practices').json()))
print('tree practices:', len(c.get('/api/catalog/tree?featured_only=true').json()))
print('build-status practices:', len(c.get('/api/catalog/build-status').json()['practices']))
print('use-cases (RC-E2E-03):', len(c.get('/api/catalog/use-cases?service=RC-E2E-03').json()))
r = c.post('/api/deployments/render', json={'selected_ids':['service:RC-E2E-03'],'tenant':'contoso','wave':'w2','use_case_id':'rc-e2e-03--default'})
print('render:', r.status_code, r.json()['summary'])
"
```
Expected: every endpoint OK; render returns 200 with summary referencing use case.

**Step 2:** Confirm DESIGN.md presence across the catalog:
```powershell
$count = (Get-ChildItem -Path services/rc -Recurse -Filter "DESIGN.md" | Measure-Object).Count
"DESIGN.md count under services/rc: $count"
```
Expected: per service (7) + per featured scenario (5) + per agent (~36) + per default use case (7) ≈ 55+.

**Step 3:** Commit any forgotten files (should be none if every prior task committed).
```powershell
git status --short
```
Expected: clean.

**Step 4:** No new commit if clean.

---

## Closure

After all tasks pass:

```powershell
git log --oneline -25
```

Expected: ~22 new commits since `7568fb8` (the design doc commit), all with `feat(...)` or `docs(...)` prefix.

---

## References

- Design: [`docs/plans/2026-05-09-rc-design-docs-foundry-design.md`](2026-05-09-rc-design-docs-foundry-design.md)
- Source data: [`docs/reference/APEX-Scenario-Chains.xlsx`](../reference/APEX-Scenario-Chains.xlsx)
- Existing books: [Deployment Guide](../book/Professional-APEX-Deployment-Guide.html), [Services Guide](../book/Professional-APEX-Services-Guide.html)
- Microsoft Learn: see design doc §13 for full link table

---

## Phase I — Microsoft Platform alignment (added 2026-05-09 after delta review)

> Detail: [`2026-05-09-microsoft-platform-alignment-delta.md`](2026-05-09-microsoft-platform-alignment-delta.md). These tasks are required **before** any production deployment to Azure / M365 / Power Platform.

### Task I1: Identity — Entra Agent ID adoption

**Files:**
- Modify: `infra/bicep/platform/identity.bicep` — add Entra Agent ID parent identity provisioning
- Modify: `docs/book/Professional-APEX-Deployment-Guide.html` — chapters 8 (identity), 13 (security), 9 (HITL CA)
- Create: `docs/APEX - Design and Build/agent-identity-blueprints.md` — per-service blueprint definitions

**Steps:** see delta §A items A.1–A.6. Commit per book/file. Verify Entra Agent ID provisioning lints with AVM module (when available) or document as TODO if SDK is sidecar-only.

### Task I2: Data tier — primary-workspace pattern + OneLake user identity mode

**Files:**
- Modify: `docs/book/Professional-APEX-Services-Guide.html` — ch 1 (medallion contract), ch 4 (SOR connections), ch 5 (Real-Time Hub), new §1.5 (primary-workspace pattern)
- Modify: `docs/book/Professional-APEX.html` — ch 8 (Fabric layering)
- Modify: `infra/bicep/modules/service.bicep` — workspace-identity-based output instead of SP secret
- Modify: `services/{ind}/{code}/service.yaml` (via generator) — add `workspace_pattern: primary-with-shortcuts`

**Steps:** see delta §B items B.1–B.12. Per book section, edit + re-balance HTML tags + commit. Generator update is small (one new field). Run grep for "Synapse Data Explorer" + replace.

### Task I3: Security — Purview + Defender integration

**Files:**
- Modify: `docs/book/Professional-APEX-Deployment-Guide.html` — ch 11 (audit), 13 (security), new ch 13.5 (Pre-deployment Security Gate)
- Modify: `infra/bicep/platform/main.bicep` — Defender for Cloud + Defender for AI services enablement
- Create: `infra/bicep/platform/security-baseline.bicep` — CMK, Customer Lockbox, MCSB AI Security policy assignments
- Create: `docs/APEX - Design and Build/classification-mapping.md` — APEX T1–T4 → Purview sensitivity-label crosswalk

**Steps:** see delta §C items C.1–C.9. Heavy chapter rewrites in Deployment Guide ch 11 + 13. Commit per chapter.

### Task I4: Foundry — Standard Setup with Private Networking

**Files:**
- Modify: `infra/bicep/platform/foundry.bicep` — pin AVM version, BYO Storage + AI Search + Cosmos DB + VNet, network injection at create
- Create: `infra/bicep/platform/dns.bicep` — 7 private DNS zones
- Create: `infra/bicep/platform/byo-resources.bicep` — Storage + AI Search + Cosmos with private endpoints
- Modify: `docs/book/Professional-APEX-Deployment-Guide.html` — ch 7 (service module shape), ch 11.5 (new Foundry chapter)

**Steps:** see delta §D items D.1–D.7. Bicep updates only — no new APEX runtime code. Lint each module via `az bicep build`.

### Task I5: M365 + Power Platform surfacing (optional, post-pilot)

**Files:**
- Modify: `docs/book/Professional-APEX-Deployment-Guide.html` — new ch 11.5 (Surfacing APEX in M365)
- Modify: `docs/book/Professional-APEX-Sellers-Guide.html` — surface notes per service envelope
- Create: `apps/m365-publisher/` — Microsoft 365 Agents Toolkit packaging skeleton (TBD; later sprint)

**Steps:** see delta §E items E.1–E.6. Documentation-only at this phase; M365 publishing tooling follows Wave 2 pilot success.

### Task I6: Terminology grep across all books

**Files:**
- Modify: all 6 HTML books in `docs/book/`

**Step 1:** Run a grep-replace pass per delta §F (F.1–F.6). One commit per term, one tag-balance check per book.

**Step 2:** Validate no broken anchors after rewrite.

**Step 3:** Commit per book.

### Task I7: Pre-deployment Security Gate checklist

**Files:**
- Create: `docs/APEX - Design and Build/Pre-deployment-Security-Gate.md` — operator-facing checklist
- Modify: `apps/deploy-wizard/web/src/pages/Deploy.tsx` — render the gate checklist before allowing Bicep apply

**Steps:** Operator must satisfy MCSB controls + Purview labels + Defender enabled + Entra Agent ID + CA + CMK + AI Model Security scan green. Blocks Bicep apply when any fail.

### Task I8: Open questions resolution

**Steps:** Sequence delta §H questions H.1–H.5 as Sprint 30 spike tickets — answer before Sprint 32 implementation. Each becomes a separate ADR in `docs/APEX - Design and Build/adr/`.

---

## Phase J — Reuse-not-build cleanup

Per delta §G — strip APEX over-builds where Microsoft platform GA capability supersedes:

| Drop | Replacement |
|---|---|
| `eventhouse-mcp` (planned) | Real-Time Intelligence remote MCP for Eventhouse |
| Custom embedding endpoint for The Pricer | Eventhouse `ai_embeddings` SLM plugin |
| Custom Debezium CDC parser | Eventstream DeltaFlow |
| Custom HITL alert trigger | Eventstream Activator destination |
| Bespoke agent threat detection | Defender for AI services |
| Custom audit-row HMAC infra (BL.P.84) | **Demote to overlay** — Purview Audit becomes system of record |

**Steps:** Per item, write a one-page deprecation note in `docs/APEX - Design and Build/deprecations/`, update Roadmap.md to mark the BL.P.* item as superseded, link to the Microsoft GA capability.
