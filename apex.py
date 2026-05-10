"""APEX -- top-level entry point.

Run with no arguments to see the framework overview + substrate
descriptions + available commands. Run with a subcommand to do the thing:

    python apex.py                     # overview (this screen)
    python apex.py launch              # launch the deploy wizard
    python apex.py launch --real       # launch the wizard against real Azure
    python apex.py validate            # run user-acceptance validation
    python apex.py status              # show sprint + backlog snapshot

APEX (Agentic Platform for Enterprise eXecution) is Deloitte's delivery
accelerator for agentic AI on the Microsoft platform. APEX-M is the
Microsoft variant; APEX-G + APEX-A are sibling variants for Google Cloud
and AWS (Independence-compliant stubs until commissioned).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
WIZARD_LAUNCHER = REPO_ROOT / "apps" / "deploy-wizard" / "launch.py"
ACCEPTANCE_SCRIPT = REPO_ROOT / "tools" / "validate_acceptance.py"


# ---------------------------------------------------------------------------
# Overview content
# ---------------------------------------------------------------------------


OVERVIEW = r"""
==============================================================================
                    APEX -- Agentic Platform for Enterprise eXecution
                       Deloitte's delivery accelerator for AI on Microsoft
==============================================================================

WHAT APEX IS
------------
APEX is a three-layer cake:

  Layer 1 - Platform   Cloud infrastructure (Azure for APEX-M)
                       Bicep / Terraform / CloudFormation per variant
                       Identity, secrets, audit, networking, observability

  Layer 2 - Services   Industry-shaped capabilities (45+ per practice)
                       RC-E2E-03 Pricing & Revenue, RC-E2E-04 Loyalty, ...
                       Each service ships its own Bicep module + agent fleet

  Layer 3 - Agents     The agents that do the work
                       Per Microsoft Agent Framework (ADR-006) -- Sequential
                       / Concurrent / Handoff / Group Chat / Magentic.
                       Each agent has prompts, MCP tools, HITL config.

VARIANTS
--------
  APEX-M    Microsoft (Azure + M365 + Power Platform + Fabric +     SHIPPED
            Foundry + Purview + Defender + Entra)
  APEX-G    Google Cloud                                            STUB
  APEX-A    AWS                                                     STUB

APEX-G + APEX-A are Independence-compliant stubs today; lit up when a
client commissions a non-Microsoft variant.

PRACTICES
---------
Seven industry practices in the framework:

  RC      Retail & Consumer (5 featured services production-ready)   SHIPPED
  HLS     Health & Life Sciences                                     Sprint 58+
  ER      Energy & Resources                                         Sprint 60+
  AXLE    Auto, Industrial, Manufacturing                            Sprint 60+
  TH      Travel & Hospitality                                       Sprint 60+
  TMT     Tech, Media & Telecom                                      Sprint 60+
  ICE     Internal Commerce & Equipment                              Sprint 60+


SUBSTRATES -- where APEX can be deployed
========================================

APEX deploys to four substrates. The same wizard, the same code, the
same use cases -- different cloud surface + security posture per substrate.

------------------------------------------------------------------------------
[1] LAPTOP                                              Independence-clean
------------------------------------------------------------------------------
  What it is        Docker Desktop on the developer's laptop
  How it deploys    `docker-compose up` -- wizard emits docker-compose.yml
  Backend           All Microsoft SDKs MOCKED (apex-m mocks)
  Cost              $0
  Time to spin up   minutes
  Use for           Demos, developer onboarding, CI, user-acceptance
                    walk-throughs, training, prompt iteration
  Gates required    None -- synthetic personas allowed
  Identity          Mocked Entra Agent ID
  Data              In-memory mocks + Redis container
  Client data?      Never. Synthetic fixtures only.
  Wizard mode       APEX_FORCE_MOCK=true (the default)

------------------------------------------------------------------------------
[2] DEV  (Lab tenant)                                   internal Deloitte
------------------------------------------------------------------------------
  What it is        Deloitte Lab Azure subscription -- internal pre-pilot
                    validation environment
  How it deploys    `az deployment group create` against the Lab RG
  Backend           Real Microsoft SDKs against a real (but Lab) tenant
  Cost              Lab consumption -- bounded; team-charged
  Time to spin up   1-2 weeks (subscription onboarding + RBAC setup)
  Use for           Sprint validation, integration testing, smoke tests
                    against real Microsoft services pre-engagement
  Gates required    PSG-1, 2, 3, 5, 6, 9, 11, 12, 14, 15
                    (PSG-7 Customer Lockbox + PSG-8 Fabric workspace
                     IP firewall + PSG-13 Foundry Private Networking
                     are WAIVABLE on Lab)
  Identity          Real Entra Agent ID in the Lab tenant
  Data              Synthetic + sandbox-graded
  Client data?      Never. Lab tenants run synthetic and Deloitte-internal
                    data only.
  Wizard mode       APEX_FORCE_MOCK=false  -- substrate=dev

------------------------------------------------------------------------------
[3] STAGE  (pre-prod for the engagement)                client tenant
------------------------------------------------------------------------------
  What it is        Client's pre-production Azure tenant
  How it deploys    `az deployment group create` against the client's
                    pre-prod RG
  Backend           Real Microsoft SDKs, full private networking
  Cost              Client-billed
  Time to spin up   2-4 weeks (per Sprint 47 first-client engagement)
  Use for           Integration validation under client governance,
                    client UAT, HITL persona dry-runs, 1-2 sprint
                    burn-in before prod cutover
  Gates required    All 14 standard gates (PSG-1 through PSG-14) +
                    PSG-15 persona-binding lint (must be GREEN)
  Identity          Client's Entra tenant -- bound to client groups
                    via persona_principal_bindings in the use-case YAML
  Data              Sandbox copy of production data OR fresh synthetic
  Client data?      Maybe -- per the engagement contract
  Wizard mode       APEX_FORCE_MOCK=false  -- substrate=stage

------------------------------------------------------------------------------
[4] PROD  (production)                                  client tenant
------------------------------------------------------------------------------
  What it is        Client's production Azure tenant
  How it deploys    `az deployment group create` against the client's
                    prod RG (operator-driven via wizard with explicit
                    second confirm on every destructive change)
  Backend           Real Microsoft SDKs + Customer Managed Keys (CMK)
                    + Customer Lockbox + Private Networking
  Cost              Client-billed at full SKU
  Time to spin up   Sprint 47 + W2 commercial envelope signed
  Use for           Live client operations. Daniel Chen approves real
                    markdowns. Marisol Reyes approves real cold-chain
                    decisions. The audit row writes to real Purview.
  Gates required    All 15 PSG gates GREEN + Independence consultation
                    per adapter + every Sprint 41-45 production-wired
                    protocol active
  Identity          Client's production Entra tenant
  Data              Live client data -- under strict classification
                    propagation per ADR-005 sensitivity model
  Client data?      YES -- full production data flows
  Wizard mode       APEX_FORCE_MOCK=false  -- substrate=prod


DEPLOY UX -- the wizard's 6 steps
=================================

For any substrate above, the operator does the same 6 things in the
wizard at http://localhost:5173/wizard:

  1. Select   Practice -> Service -> Scenario -> Agent in the treeview
  2. Config   Substrate, variant, use case, tenant slug, wave, operator UPN
  3. Render   Wizard emits docker-compose.yml (laptop) OR Bicep params (cloud)
              ... and auto-polls all 15 Pre-deployment Security Gates
  4. Review   Operator inspects the diff + the 15-gate panel
  5. Confirm  Tick "confirmed destructive changes" if any Delete shown
  6. Deploy   POST /api/deployments runs PSG check -> what-if -> apply
              -> stamps audit row with correlation ID

The same flow works against mock backends OR real Azure depending on
the substrate the operator picked in step 2.


COMMANDS
========

  python apex.py launch                Launch the wizard (mock mode default)
  python apex.py launch --real         Launch against real Azure
  python apex.py launch --no-frontend  Backend API only (no UI)
  python apex.py validate              Re-run user-acceptance validation
  python apex.py status                Show sprint + backlog snapshot
  python apex.py overview              Show this screen again

  python apex.py --help                argparse help
"""


SUBSTRATE_TABLE_FOR_STATUS = """
+------------+-----------+----------------+--------------+----------------+
| Substrate  | Cost      | Spin-up        | Gates needed | Client data?   |
+------------+-----------+----------------+--------------+----------------+
| laptop     | $0        | minutes        | none         | never          |
| dev (Lab)  | Lab usage | 1-2 weeks      | 10 of 15     | never          |
| stage      | Client    | 2-4 weeks      | 14 of 15     | sandbox/maybe  |
| prod       | Client    | Sprint 47+     | 15 of 15     | YES (live)     |
+------------+-----------+----------------+--------------+----------------+
"""


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------


def cmd_overview(_args: argparse.Namespace) -> int:
    """Show the framework overview (default when no subcommand given)."""
    print(OVERVIEW)
    print(SUBSTRATE_TABLE_FOR_STATUS)
    print("Tip: run `python apex.py launch` to start the wizard.")
    return 0


def cmd_launch(args: argparse.Namespace) -> int:
    """Forward to apps/deploy-wizard/launch.py with the given flags."""
    if not WIZARD_LAUNCHER.exists():
        print(f"[error] launcher not found at {WIZARD_LAUNCHER}")
        return 1
    argv = [sys.executable, str(WIZARD_LAUNCHER)]
    if args.real:
        argv.append("--real")
    if args.no_frontend:
        argv.append("--no-frontend")
    if args.no_backend:
        argv.append("--no-backend")
    print(f"$ {' '.join(argv)}")
    proc = subprocess.run(argv, cwd=REPO_ROOT, check=False)
    return proc.returncode


def cmd_validate(_args: argparse.Namespace) -> int:
    """Re-run the user-acceptance validation."""
    if not ACCEPTANCE_SCRIPT.exists():
        print(f"[error] acceptance script not found at {ACCEPTANCE_SCRIPT}")
        return 1
    # Ensure the env has the right PYTHONPATH for editable-not-installed
    env = os.environ.copy()
    sep = ";" if os.name == "nt" else ":"
    env["PYTHONPATH"] = sep.join(filter(None, [
        str(REPO_ROOT / "apex-m" / "src"),
        str(REPO_ROOT / "packages" / "apex-core" / "src"),
        str(REPO_ROOT / "apps" / "deploy-wizard" / "api" / "src"),
        env.get("PYTHONPATH", ""),
    ]))
    proc = subprocess.run(
        [sys.executable, str(ACCEPTANCE_SCRIPT)],
        cwd=REPO_ROOT,
        env=env,
        check=False,
    )
    return proc.returncode


def cmd_status(_args: argparse.Namespace) -> int:
    """Show sprint progress + backlog retirement snapshot."""
    print("APEX -- sprint + backlog snapshot")
    print("=" * 70)

    # Backlog progress from Roadmap.md checkbox counts
    roadmap = REPO_ROOT / "docs" / "APEX - Design and Build" / "Roadmap.md"
    if roadmap.exists():
        text = roadmap.read_text(encoding="utf-8")
        import re
        done_p = len(re.findall(r"- \[x\] \*\*BL\.P\.", text))
        todo_p = len(re.findall(r"- \[ \] \*\*BL\.P\.", text))
        done_c = len(re.findall(r"- \[x\] \*\*BL\.C\.", text))
        todo_c = len(re.findall(r"- \[ \] \*\*BL\.C\.", text))
        total = done_c + done_p + todo_c + todo_p
        done = done_c + done_p
        pct = (done * 100) // total if total else 0
        print(f"  Roadmap backlog: {done} of {total} done ({pct}%)")
        print(f"    BL.C.* (foundation):  {done_c} / {done_c + todo_c}")
        print(f"    BL.P.* (planned):     {done_p} / {done_p + todo_p}")
    else:
        print("  (Roadmap.md not found)")

    # Sprint status from RC build-status YAML
    build_status = REPO_ROOT / "services" / "rc" / "_build-status.yaml"
    if build_status.exists():
        try:
            import yaml
            data = yaml.safe_load(build_status.read_text(encoding="utf-8"))
            sprints = data.get("sprints", []) if isinstance(data, dict) else []
            done = sum(
                1 for s in sprints
                if all(item.get("done") for item in s.get("items", []) or [True])
                and (s.get("items") or [])
            )
            in_progress = sum(
                1 for s in sprints
                if any(item.get("done") for item in s.get("items", []) or [])
                and not all(item.get("done") for item in s.get("items", []) or [True])
            )
            planned = sum(1 for s in sprints
                if not any(item.get("done") for item in s.get("items", []) or []))
            print()
            print(f"  RC sprints: {len(sprints)} total")
            print(f"    done:        {done}")
            print(f"    in progress: {in_progress}")
            print(f"    planned:     {planned}")
        except Exception as exc:
            print(f"  (build-status.yaml read error: {exc})")
    else:
        print("  (services/rc/_build-status.yaml not found)")

    print()
    print("  Next runnable: see docs/APEX - Design and Build/")
    print("                       Sprint-Backlog-Retirement-Map.md")
    print()
    return 0


# ---------------------------------------------------------------------------
# argparse wiring
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apex",
        description="APEX top-level entry point. Run with no args for overview.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_overview = sub.add_parser("overview", help="Framework overview + substrates")
    p_overview.set_defaults(func=cmd_overview)

    p_launch = sub.add_parser(
        "launch",
        help="Launch the deploy wizard (backend + frontend)",
    )
    p_launch.add_argument(
        "--real",
        action="store_true",
        help="Disable APEX_FORCE_MOCK; call real Azure (requires az + Lab subscription)",
    )
    p_launch.add_argument(
        "--no-frontend",
        action="store_true",
        help="Skip the Vite frontend (backend only)",
    )
    p_launch.add_argument(
        "--no-backend",
        action="store_true",
        help="Skip the FastAPI backend (frontend only)",
    )
    p_launch.set_defaults(func=cmd_launch)

    p_validate = sub.add_parser(
        "validate",
        help="Re-run the user-acceptance validation (A1-A4)",
    )
    p_validate.set_defaults(func=cmd_validate)

    p_status = sub.add_parser(
        "status",
        help="Show sprint + backlog retirement snapshot",
    )
    p_status.set_defaults(func=cmd_status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.cmd:
        return cmd_overview(args)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
