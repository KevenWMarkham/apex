# APEX — Agentic Platform for Enterprise eXecution

Deloitte's delivery accelerator for agentic AI on Microsoft. APEX-M is the
Microsoft variant shipping today; APEX-G (Google Cloud) and APEX-A (AWS)
are Independence-compliant stubs until commissioned.

---

## Start here

```bash
python apex.py
```

That single command prints the framework overview, the four deploy
substrates (laptop · dev · stage · prod), the 6-step deploy UX, and the
list of subcommands. It is the canonical entry point for the framework.

### Common commands

```bash
python apex.py launch              # launch the deploy wizard (mock mode default)
python apex.py launch --real       # launch against real Azure (requires az login)
python apex.py validate            # re-run the 4 user-acceptance criteria
python apex.py status              # sprint + backlog snapshot
python apex.py --help              # argparse help
```

Once the wizard is launched, open <http://localhost:5173/wizard>.

---

## Deploy UX — wizard at a glance

The wizard at `apps/deploy-wizard/` walks an operator through:

1. **Select**   Practice → Service → Scenario → Agent in the treeview
2. **Config**   Substrate, variant (APEX-M), use case, tenant
3. **Render**   `docker-compose.yml` (laptop) or Bicep params (cloud)
4. **Review**   diff + all 15 Pre-deployment Security Gates polled inline
5. **Confirm**  tick "I have reviewed the diff" (required when destructive)
6. **Deploy**   `POST /api/deployments` → PSG check → what-if → apply → audit row

See `apps/deploy-wizard/README.md` for the full wizard reference.

---

## Substrates

| Substrate | Cost      | Spin-up    | Gates needed | Client data?  |
|---|---|---|---|---|
| laptop    | $0        | minutes    | none         | never         |
| dev (Lab) | Lab usage | 1-2 weeks  | 10 of 15     | never         |
| stage     | Client    | 2-4 weeks  | 14 of 15     | sandbox/maybe |
| prod      | Client    | Sprint 47+ | 15 of 15     | YES (live)    |

Run `python apex.py` for the long-form description of each substrate.

---

## Repo layout

```
apex.py                          # top-level entry point (start here)
apps/deploy-wizard/              # FastAPI + React deploy wizard
  README.md                        # wizard reference
  launch.py                        # one-command launcher (backend + frontend)
  api/                             # FastAPI control plane
  web/                             # React 19 + Vite frontend
apex-m/                          # Microsoft variant
  infra/bicep/                     # Layer 1 platform + Layer 2 blueprints
  src/apex_m/                      # SDK adapters, persona resolver, audit
services/                        # 7 practices · 700+ scenarios
  rc/                              # Retail & Consumer (5 featured services shipped)
  hls/  er/  axle/  th/  tmt/  ice/
packages/apex-core/              # protocol contracts, validators
docs/
  APEX - Design and Build/         # Roadmap.md, ADRs, acceptance criteria
  build-specs/                     # apex-core + apex-rc build specs
  guides/                          # solution + deployment guides
tools/
  validate_acceptance.py           # runs the 4 user-acceptance criteria
```

---

## User acceptance

Four criteria validated end-to-end in mock mode:

| ID | Criterion |
|---|---|
| A1 | Laptop substrate produces a runnable docker-compose stack |
| A2 | Cloud substrates (dev / stage / prod) produce valid Bicep parameter files |
| A3 | Operator clones `_default/` → `<client>/`, populates persona bindings, PSG-15 unlocks deploy |
| A4 | Wizard end-to-end: PSG check → what-if → deploy → audit row → drift |

Re-validate any time:

```bash
python apex.py validate
```

Full report: `docs/APEX - Design and Build/ACCEPTANCE-CRITERIA.md`

---

## Status

- 509 unit + integration tests pass
- 4 of 4 user-acceptance criteria validated (mock mode)
- 165 of 259 roadmap items retired (63%) — `python apex.py status` for live count
- Sprints 41-45 + 47.1-5 + 48 + 49 blocked on Lab Azure subscription provisioning

---

## Next

- `python apex.py` to read the framework overview
- `python apex.py launch` to drive the wizard yourself
- `python apex.py validate` to confirm the acceptance criteria still pass
- `docs/APEX - Design and Build/Roadmap.md` for the full backlog
