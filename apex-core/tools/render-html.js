/**
 * Render a self-contained HTML report from a buildReport() result.
 *
 * Uses APEX Core Part 9 design tokens (dark theme default with light-theme
 * toggle). Fonts loaded from Google Fonts via <link> tags in <head>. All
 * styles and script inlined so the file is portable (attach to PR, email, or
 * drop into the edition site).
 *
 * Semantic colors (Part 9.2): teal = pass, amber = MINOR drift / warning,
 * crimson = MAJOR drift / critical, slate = info / low severity.
 *
 * @param {object} report  Result of buildReport().
 * @returns {string}  Complete HTML document.
 */
export function renderHtml(report) {
  const {
    generated_utc,
    edition_code = '—',
    status = 'pass',
    summary = { critical: 0, warning: 0, info: 0 },
    findings = []
  } = report;

  const statusColor =
    status === 'fail' ? 'crimson' :
    status === 'warn' ? 'amber' :
    'teal';

  const findingsHtml = findings.length === 0
    ? `<p class="muted">No findings. Manifest conforms to the Core v1.2 contract.</p>`
    : `<ul class="findings">
${findings.map(renderFinding).join('\n')}
</ul>`;

  return `<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>APEX validate · ${escapeHtml(edition_code)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
<style>
:root[data-theme="dark"] {
  --bg-void: #060a12;
  --bg-surface: #0b111e;
  --bg-card: #121a2c;
  --bg-card-hi: #1a2339;
  --line: #1e2a44;
  --line-hi: #2f3f5f;
  --text: #e7ecf7;
  --text-dim: #8a97b2;
  --text-mute: #56627c;
  --amber: #f5a623;
  --teal: #2dd4bf;
  --crimson: #ef4444;
  --slate: #64748b;
  --gold: #d4a244;
  --indigo: #7c83de;
}
:root[data-theme="light"] {
  --bg-void: #f4efe3;
  --bg-surface: #ebe4d3;
  --bg-card: #ffffff;
  --bg-card-hi: #faf5e9;
  --line: #dbd1b9;
  --line-hi: #b8aa8c;
  --text: #1a1f2e;
  --text-dim: #4a5060;
  --text-mute: #847d68;
  --amber: #8f5a0c;
  --teal: #0d7d70;
  --crimson: #a81616;
  --slate: #525b6e;
  --gold: #8a6508;
  --indigo: #3e4894;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg-void);
  color: var(--text);
  font-family: 'Instrument Sans', system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.55;
  transition: background-color 280ms ease-out, color 280ms ease-out;
}
main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 48px;
}
@media (max-width: 960px) { main { padding: 28px; } }
header.masthead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 32px;
}
h1 {
  font-family: 'Fraunces', serif;
  font-weight: 600;
  font-size: 34px;
  margin: 0;
  letter-spacing: -0.01em;
}
h2 {
  font-family: 'Fraunces', serif;
  font-weight: 600;
  font-size: 22px;
  margin: 32px 0 12px;
}
.wordmark-sub {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--text-mute);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-top: 4px;
}
.theme-toggle {
  background: var(--bg-card);
  color: var(--text);
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 8px 16px;
  cursor: pointer;
  font: inherit;
  font-size: 13px;
  transition: background-color 150ms, border-color 150ms;
}
.theme-toggle:hover { border-color: var(--line-hi); }
.summary-card {
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 24px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 24px;
  align-items: center;
}
.status-chip {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.06em;
  padding: 8px 16px;
  border-radius: 6px;
  text-transform: uppercase;
  background: color-mix(in srgb, var(--chip) 14%, transparent);
  color: var(--chip);
  border: 1px solid color-mix(in srgb, var(--chip) 40%, transparent);
}
.status-chip.teal { --chip: var(--teal); }
.status-chip.amber { --chip: var(--amber); }
.status-chip.crimson { --chip: var(--crimson); }
.counts { display: flex; gap: 24px; }
.count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--text-dim);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.count strong {
  display: block;
  font-family: 'Fraunces', serif;
  font-size: 28px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 2px;
  letter-spacing: -0.01em;
}
.count.critical strong { color: var(--crimson); }
.count.warning strong { color: var(--amber); }
.count.info strong { color: var(--slate); }
.meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--text-mute);
  text-align: right;
}
.findings {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.finding {
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-left: 3px solid var(--dot);
  border-radius: 8px;
  padding: 14px 18px;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 16px;
  align-items: start;
}
.finding.critical { --dot: var(--crimson); }
.finding.warning  { --dot: var(--amber); }
.finding.info     { --dot: var(--slate); }
.finding .rule {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 4px 8px;
  border-radius: 4px;
  background: color-mix(in srgb, var(--dot) 14%, transparent);
  color: var(--dot);
  white-space: nowrap;
}
.finding .body .path {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--text-dim);
  margin-bottom: 4px;
}
.finding .body .message {
  color: var(--text);
}
.muted { color: var(--text-mute); font-style: italic; }
footer {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--text-mute);
  letter-spacing: 0.04em;
  display: flex;
  justify-content: space-between;
}
</style>
</head>
<body>
<main>
  <header class="masthead">
    <div>
      <h1>APEX · ${escapeHtml(edition_code)} validation report</h1>
      <span class="wordmark-sub">L2 edition manifest · Core v1.2 contract</span>
    </div>
    <button class="theme-toggle" type="button" aria-label="Toggle color theme">◐ Theme</button>
  </header>

  <section class="summary-card">
    <div class="status-chip ${statusColor}">${escapeHtml(status)}</div>
    <div class="counts">
      <div class="count critical"><strong>${summary.critical ?? 0}</strong>Critical</div>
      <div class="count warning"><strong>${summary.warning ?? 0}</strong>Warning</div>
      <div class="count info"><strong>${summary.info ?? 0}</strong>Info</div>
    </div>
    <div class="meta">
      <div>${escapeHtml(generated_utc ?? '')}</div>
      <div>${findings.length} total finding${findings.length === 1 ? '' : 's'}</div>
    </div>
  </section>

  <h2>Findings</h2>
  ${findingsHtml}

  <footer>
    <span>APEX Core v1.2 · schema-manifest-contract v1.0</span>
    <span>Generated by apex-validate</span>
  </footer>
</main>

<script>
(function () {
  const key = 'apex-theme';
  const root = document.documentElement;
  const stored = localStorage.getItem(key);
  if (stored === 'light' || stored === 'dark') {
    root.dataset.theme = stored;
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    root.dataset.theme = 'light';
  }
  const btn = document.querySelector('.theme-toggle');
  if (btn) {
    btn.addEventListener('click', () => {
      const next = root.dataset.theme === 'light' ? 'dark' : 'light';
      root.dataset.theme = next;
      localStorage.setItem(key, next);
    });
  }
})();
</script>
</body>
</html>`;
}

function renderFinding(f) {
  const severity = f.severity || 'info';
  return `  <li class="finding ${escapeHtml(severity)}">
    <span class="rule">${escapeHtml(f.rule ?? '')}</span>
    <div class="body">
      <div class="path">${escapeHtml(f.path ?? '')}</div>
      <div class="message">${escapeHtml(f.message ?? '')}</div>
    </div>
  </li>`;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
