// build-professional-apex.cjs
//
// Builds the single-file Wrox-style HTML book:
//   docs/book/Professional-APEX.html
//
// Combines the Developer Implementation Guide and the Comprehensive
// Solutions Reference into one volume of 30 chapters across 6 Parts
// plus 10 appendices. Reuses the existing Mermaid PNG cache.
//
// Run:  node build-professional-apex.cjs

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const os = require('os');

// ---------- Paths ----------
const ROOT = __dirname;
const OUTPUT_HTML = path.join(ROOT, 'docs', 'book', 'Professional-APEX.html');
const MERMAID_CACHE = path.join(ROOT, '.cache', 'mermaid');
const MMDC_JS = path.join(ROOT, 'node_modules', '@mermaid-js', 'mermaid-cli', 'src', 'cli.js');

fs.mkdirSync(path.dirname(OUTPUT_HTML), { recursive: true });
fs.mkdirSync(MERMAID_CACHE, { recursive: true });

// ---------- Source files ----------
const SRC = {
  devSpine:  path.join(ROOT, 'docs', 'APEX-developer-guide.md'),
  dev01:     path.join(ROOT, 'docs', 'dev-guide', '01-fabric-layering.md'),
  dev02:     path.join(ROOT, 'docs', 'dev-guide', '02-medallion-sor.md'),
  dev03:     path.join(ROOT, 'docs', 'dev-guide', '03-mcp-servers.md'),
  dev04:     path.join(ROOT, 'docs', 'dev-guide', '04-agent-lifecycle.md'),
  dev05:     path.join(ROOT, 'docs', 'dev-guide', '05-observability-security.md'),
  dev06:     path.join(ROOT, 'docs', 'dev-guide', '06-testing-topology.md'),
  dev07:     path.join(ROOT, 'docs', 'dev-guide', '07-service-catalog.md'),
  ref:       path.join(ROOT, 'docs', 'APEX-comprehensive-solutions-reference.md'),
};

function read(p) { return fs.readFileSync(p, 'utf8'); }

// ---------- Section extraction ----------
// Extract a named heading block from a markdown file. Returns the markdown
// from (and including) the heading through the next heading of equal-or-lower depth.
function extractSection(mdPath, heading) {
  const md = read(mdPath);
  const lines = md.split(/\r?\n/);
  const headingRx = new RegExp('^(#{1,6})\\s+' + heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*$');
  let startIdx = -1, startDepth = 0;
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(headingRx);
    if (m) { startIdx = i; startDepth = m[1].length; break; }
  }
  if (startIdx === -1) return `<!-- section "${heading}" not found in ${path.basename(mdPath)} -->`;
  let endIdx = lines.length;
  for (let i = startIdx + 1; i < lines.length; i++) {
    const hm = lines[i].match(/^(#{1,6})\s/);
    if (hm && hm[1].length <= startDepth) { endIdx = i; break; }
  }
  return lines.slice(startIdx, endIdx).join('\n');
}

// Extract everything after a heading (no end boundary) — useful for appendices
function extractFromHeadingToEOF(mdPath, heading) {
  return extractSection(mdPath, heading);
}

// Extract the full body of a file (skip H1 title)
function extractWholeBody(mdPath) {
  const md = read(mdPath);
  // drop the first H1 title; keep everything else
  return md.replace(/^#\s+[^\n]*\n/, '');
}

// ---------- Mermaid rendering ----------
function renderMermaidToPng(source) {
  const hash = crypto.createHash('sha256').update(source).digest('hex').slice(0, 16);
  const cachePath = path.join(MERMAID_CACHE, `${hash}.png`);
  if (fs.existsSync(cachePath)) return fs.readFileSync(cachePath);

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'apex-book-mmd-'));
  const mmdPath = path.join(tmpDir, 'd.mmd');
  const cfgPath = path.join(tmpDir, 'cfg.json');
  fs.writeFileSync(mmdPath, source, 'utf8');
  fs.writeFileSync(cfgPath, JSON.stringify({
    theme: 'default',
    themeVariables: { fontFamily: 'Aptos, Segoe UI, Arial, sans-serif', fontSize: '14px' },
    flowchart: { useMaxWidth: false, htmlLabels: true },
    sequence: { useMaxWidth: false },
  }));
  try {
    execFileSync(process.execPath, [MMDC_JS,
      '-i', mmdPath, '-o', cachePath, '-c', cfgPath,
      '-b', 'white', '-w', '1400', '-H', '900', '--scale', '2',
    ], { stdio: ['ignore', 'ignore', 'pipe'] });
  } catch (err) {
    console.warn(`  ! mermaid render failed: ${err.message.split('\n')[0]}`);
    return null;
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  }
  return fs.existsSync(cachePath) ? fs.readFileSync(cachePath) : null;
}

// ---------- Markdown to HTML ----------
function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function slugify(s) {
  return String(s).toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim().replace(/\s+/g, '-').slice(0, 60);
}

// Track anchors and collect for index
const indexTerms = new Map(); // term → Set<anchor>
const tocEntries = []; // { level, text, anchor, partNum, chapterNum }

function recordToc(level, text, anchor, partNum, chapterNum) {
  tocEntries.push({ level, text, anchor, partNum, chapterNum });
}

function parseInline(text) {
  // Order matters: escape, then process tokens in a non-destructive way
  let out = escapeHtml(text);
  // Inline code
  out = out.replace(/`([^`]+)`/g, (_, code) =>
    `<code class="inline-code">${code.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')}</code>`);
  // Re-escape inline-code contents — we unescaped to allow `<w:t>` etc, but must re-escape for HTML
  // Actually keep plain for readability; code is already plain text
  // Links [text](url)
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, t, u) => {
    const cls = u.startsWith('#') ? 'xref' : 'external';
    return `<a class="${cls}" href="${escapeHtml(u)}">${escapeHtml(t)}</a>`;
  });
  // Bold then italic
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>');
  return out;
}

function splitTableRow(line) {
  return line.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|').map(c => c.trim());
}

// Parse a markdown string into HTML.
// context: { partNum, chapterNum, tocPath, recordToc, triesOutCounter, exerciseCounter, renderMermaid }
function mdToHtml(md, ctx) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let i = 0;
  ctx = ctx || {};
  const partNum = ctx.partNum || null;
  const chapterNum = ctx.chapterNum || null;
  const skipFirstH1 = !!ctx.skipFirstH1;
  let seenFirstH1 = false;

  while (i < lines.length) {
    const line = lines[i];

    // Fenced code block
    if (/^```/.test(line) || /^~~~/.test(line)) {
      const fence = line.slice(0, 3);
      const lang = line.slice(3).trim();
      const body = [];
      i++;
      while (i < lines.length && !lines[i].startsWith(fence)) { body.push(lines[i]); i++; }
      i++;
      if (lang === 'mermaid') {
        const source = body.join('\n');
        const png = renderMermaidToPng(source);
        if (png) {
          const b64 = png.toString('base64');
          out.push(`<figure class="diagram"><img alt="Diagram" src="data:image/png;base64,${b64}"></figure>`);
        } else {
          out.push(`<div class="diagram-fallback"><em>(Mermaid diagram — render failed)</em><pre><code>${escapeHtml(source)}</code></pre></div>`);
        }
      } else {
        const escaped = body.map(escapeHtml).join('\n');
        out.push(`<div class="code-block"><div class="code-lang">${escapeHtml(lang || 'text').toUpperCase()}</div><pre><code class="lang-${escapeHtml(lang)}">${escaped}</code></pre></div>`);
      }
      continue;
    }

    // Heading
    const hMatch = line.match(/^(#{1,6})\s+(.+)$/);
    if (hMatch) {
      const level = hMatch[1].length;
      const rawText = hMatch[2].replace(/`/g, '').replace(/\*\*/g, '').replace(/\*/g, '');
      if (skipFirstH1 && level === 1 && !seenFirstH1) {
        seenFirstH1 = true;
        i++;
        continue;
      }
      const anchor = slugify(`${partNum || ''}-${chapterNum || ''}-${rawText}`);
      if (level <= 3) recordToc(level, rawText, anchor, partNum, chapterNum);
      out.push(`<h${level} id="${anchor}">${parseInline(rawText)}</h${level}>`);
      i++;
      continue;
    }

    // Horizontal rule
    if (/^---+\s*$/.test(line)) { out.push('<hr class="section-rule">'); i++; continue; }

    // Table
    if (line.includes('|') && i + 1 < lines.length && /^\s*\|?[\s|:-]+\|?\s*$/.test(lines[i + 1])) {
      const headerCells = splitTableRow(line);
      i += 2;
      const body = [];
      while (i < lines.length && lines[i].trim() !== '' && lines[i].includes('|')) {
        body.push(splitTableRow(lines[i]));
        i++;
      }
      const thead = '<thead><tr>' + headerCells.map(c => `<th>${parseInline(c)}</th>`).join('') + '</tr></thead>';
      const tbody = '<tbody>' + body.map(row =>
        '<tr>' + row.map(c => `<td>${parseInline(c)}</td>`).join('') + '</tr>'
      ).join('') + '</tbody>';
      out.push(`<div class="table-wrap"><table class="md-table">${thead}${tbody}</table></div>`);
      continue;
    }

    // Blockquote — interpret as Note / Warning / Best Practice / Try It Out based on leading token
    if (/^>\s?/.test(line)) {
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^>\s?/, ''));
        i++;
      }
      const bqText = buf.join('\n');
      // Classify by leading marker
      let cls = 'note', label = 'Note';
      const firstLine = buf[0] || '';
      if (/^\*\*Note/i.test(firstLine))              { cls = 'note';         label = 'Note'; }
      else if (/^\*\*Warning/i.test(firstLine))       { cls = 'warning';      label = 'Warning'; }
      else if (/^\*\*Best Practice/i.test(firstLine)) { cls = 'bestpractice'; label = 'Best Practice'; }
      else if (/^\*\*Try It Out/i.test(firstLine))    { cls = 'tryitout';     label = 'Try It Out'; }
      else if (/^\*\*Tip/i.test(firstLine))           { cls = 'note';         label = 'Tip'; }
      // Strip the marker prefix if present
      const cleaned = bqText.replace(/^\*\*(Note|Warning|Best Practice|Try It Out|Tip)\*\*[.\s:—-]*/i, '');
      const inner = mdToHtml(cleaned, { ...ctx, skipFirstH1: false });
      out.push(`<aside class="callout ${cls}"><div class="callout-label">${label}</div>${inner}</aside>`);
      continue;
    }

    // Bullet list
    if (/^\s*[-*]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*]\s+/, ''));
        i++;
      }
      out.push('<ul>' + items.map(it => `<li>${parseInline(it)}</li>`).join('') + '</ul>');
      continue;
    }

    // Numbered list
    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*\d+\.\s+/, ''));
        i++;
      }
      out.push('<ol>' + items.map(it => `<li>${parseInline(it)}</li>`).join('') + '</ol>');
      continue;
    }

    // Blank line
    if (line.trim() === '') { i++; continue; }

    // Paragraph — accumulate until blank or block boundary
    const buf = [line]; i++;
    while (i < lines.length && lines[i].trim() !== ''
           && !/^(#{1,6})\s/.test(lines[i])
           && !/^```/.test(lines[i]) && !/^~~~/.test(lines[i])
           && !/^>\s?/.test(lines[i])
           && !/^\s*[-*]\s+/.test(lines[i])
           && !/^\s*\d+\.\s+/.test(lines[i])
           && !/^---+\s*$/.test(lines[i])
           && !lines[i].includes('|')) {
      buf.push(lines[i]); i++;
    }
    out.push(`<p>${parseInline(buf.join(' '))}</p>`);
  }
  return out.join('\n');
}

// ---------- Chapter & Part wrapping ----------
function chapterObjectives(chapterNum, topics) {
  const bullets = topics.map(t => `<li>${escapeHtml(t)}</li>`).join('');
  return `<aside class="chapter-objectives">
    <div class="objectives-label">What You'll Learn in This Chapter</div>
    <ul>${bullets}</ul>
  </aside>`;
}

function chapterSummary(chapterNum, bullets) {
  const items = bullets.map(b => `<li>${escapeHtml(b)}</li>`).join('');
  return `<section class="chapter-summary" id="ch${chapterNum}-summary">
    <h2>Summary</h2>
    <ul>${items}</ul>
  </section>`;
}

function chapterExercises(chapterNum, exercises) {
  const items = exercises.map((ex, idx) =>
    `<li><strong>${chapterNum}.${idx + 1}</strong> ${escapeHtml(ex)}</li>`
  ).join('');
  return `<section class="chapter-exercises" id="ch${chapterNum}-exercises">
    <h2>Exercises</h2>
    <ol class="exercises">${items}</ol>
    <p class="exercise-note">Solutions to these exercises are provided in <a href="#appendix-j">Appendix J: Exercise Solutions</a>.</p>
  </section>`;
}

function partOpener(partNum, partTitle, partIntro, chapters) {
  const chList = chapters.map(c =>
    `<li><span class="ch-num">Chapter ${c.num}</span><a href="#ch-${c.num}">${escapeHtml(c.title)}</a></li>`
  ).join('');
  return `<section class="part-opener" id="part-${partNum}">
    <div class="part-label">Part ${toRoman(partNum)}</div>
    <h1 class="part-title">${escapeHtml(partTitle)}</h1>
    <p class="part-intro">${escapeHtml(partIntro)}</p>
    <nav class="part-chapters">
      <h2>In This Part</h2>
      <ul>${chList}</ul>
    </nav>
  </section>`;
}

function chapterWrapper(chapterNum, title, objectives, bodyHtml, summary, exercises) {
  const objectivesHtml = chapterObjectives(chapterNum, objectives);
  const summaryHtml = chapterSummary(chapterNum, summary);
  const exercisesHtml = chapterExercises(chapterNum, exercises);
  recordToc(1, `Chapter ${chapterNum}: ${title}`, `ch-${chapterNum}`, null, chapterNum);
  return `<article class="chapter" id="ch-${chapterNum}">
    <header class="chapter-header">
      <div class="chapter-number">Chapter ${chapterNum}</div>
      <h1 class="chapter-title">${escapeHtml(title)}</h1>
    </header>
    ${objectivesHtml}
    <div class="chapter-body">
      ${bodyHtml}
    </div>
    ${summaryHtml}
    ${exercisesHtml}
  </article>`;
}

function appendixWrapper(letter, title, bodyHtml) {
  recordToc(1, `Appendix ${letter}: ${title}`, `appendix-${letter.toLowerCase()}`, null, null);
  return `<article class="appendix" id="appendix-${letter.toLowerCase()}">
    <header class="appendix-header">
      <div class="appendix-label">Appendix ${letter}</div>
      <h1 class="appendix-title">${escapeHtml(title)}</h1>
    </header>
    <div class="appendix-body">${bodyHtml}</div>
  </article>`;
}

function toRoman(n) {
  const m = ['','I','II','III','IV','V','VI','VII','VIII','IX','X'];
  return m[n] || String(n);
}

// ---------- Content plan: 30 chapters + 10 appendices ----------

// Each chapter defines: number, title, objectives, body-sourcer, summary, exercises
const chapters = [
  // PART I — INTRODUCING APEX
  {
    num: 1, part: 1, title: 'What APEX Is',
    objectives: [
      'Define APEX and what makes it agentic rather than analytical',
      'Understand the three questions APEX answers: what next, who approves, what audit',
      'Recognise the 60-second architecture picture on Microsoft Fabric',
      'Identify the four-layer manifest model and why it matters',
    ],
    body: () => extractSection(SRC.ref, 'What Is APEX?') +
              '\n\n' + extractSection(SRC.ref, 'The Value Proposition') +
              '\n\n' + extractSection(SRC.ref, 'The Ask'),
    summary: [
      'APEX is a manifest-driven agentic platform that turns enterprise events into auditable decisions',
      'It lives on Microsoft Fabric (data plane) and Azure AI (intelligence plane)',
      'Decision latency drops 5–10× and manager touch drops 60–80% in the first 12 months',
      'The catalog now spans seven industry Practices with 45 services',
    ],
    exercises: [
      'Describe in your own words how APEX differs from a traditional BI or analytics platform.',
      'Name the three questions APEX answers that traditional analytics does not.',
      'Why is APEX called "manifest-driven"? What role do manifests play in governance?',
    ],
  },
  {
    num: 2, part: 1, title: 'The Forces Driving Agentic Platforms',
    objectives: [
      'Understand the five converging forces that make agentic platforms inevitable',
      'Map each force to an APEX response mechanism',
      'Recognise how force intensity varies by industry practice',
    ],
    body: () => extractSection(SRC.ref, 'Forces of Change') +
              '\n\n' + extractSection(SRC.ref, 'Forces of Change: Summary'),
    summary: [
      'Five forces: decision-velocity gap, agentic AI inflection, data sovereignty, regulatory acceleration, knowledge-worker shortage',
      'Each force maps to a specific APEX design choice — gates for regulation, tokenisation for sovereignty, HITL capture for knowledge preservation',
      'Force intensity varies by Practice; HLS and ER carry regulatory forces most acutely',
    ],
    exercises: [
      'For an industry you know well, rank the five forces by intensity. Explain the ranking.',
      'Which force does APEX\'s HITL gate mechanism most directly address, and why?',
    ],
  },
  {
    num: 3, part: 1, title: 'Why Microsoft Fabric',
    objectives: [
      'Understand the "Fabric as data plane, Azure as intelligence plane" thesis',
      'Map APEX components to Microsoft\'s seven-layer stack',
      'Recognise what APEX is NOT: a SOR replacement or a rip-and-replace project',
    ],
    body: () => extractSection(SRC.ref, 'IT Simplification') +
              '\n\n' + extractSection(SRC.ref, 'APEX as the Intelligence Layer') +
              '\n\n' + extractSection(SRC.ref, 'The Microsoft-Native Stack'),
    summary: [
      'Fabric holds the data; Azure AI holds the intelligence; Git holds the contracts',
      'APEX consumes a focused subset of Fabric: OneLake, Lakehouse, Warehouse, Eventstream, Pipelines, Notebooks, SQL endpoint',
      'Seven-layer stack: Experience → Orchestration → Intelligence → Protocol → Data → Integration → Foundation',
      'APEX overlays SORs rather than replacing them',
    ],
    exercises: [
      'Sketch the APEX-on-Microsoft architecture from memory. Label data plane and intelligence plane.',
      'Name three Fabric items APEX uses and what each is for.',
    ],
  },
  // PART II — THE APEX FRAMEWORK
  {
    num: 4, part: 2, title: 'The Four-Layer Manifest Model',
    objectives: [
      'Understand L1 Contract, L2 Edition, L3 Practice, L4 Tenant',
      'Recognise how changes ripple down the layers',
      'Learn the SemVer-bump → HITL-gate mapping discipline',
    ],
    body: () => extractSection(SRC.ref, 'The 4-Layer Manifest Model') +
              '\n\n' + extractSection(SRC.ref, 'The HITL Gate Model'),
    summary: [
      'L1 apex-core is the specification; L2 editions are versioned releases; L3 Practices are industry bundles; L4 Tenants are client instances',
      'Every change carries a SemVer classification (MAJOR/MINOR/PATCH)',
      'SemVer class deterministically maps to HITL gate (HITL/ACK_ONLY/ZERO_TOUCH/ESCALATION)',
      'Tenants override default gates per their risk posture',
    ],
    exercises: [
      'A schema change adds a nullable column. Classify it and predict the gate.',
      'A high-risk HIPAA health system sets `MINOR → HITL`. What is the reasoning?',
      'Describe in one sentence what happens when an L2 edition is released.',
    ],
  },
  {
    num: 5, part: 2, title: 'Canonical Schemas & the Medallion Architecture',
    objectives: [
      'Learn the six canonical schema families (SCML, MERML, CXML, HLSCML, ERCML, AXLECML) plus previews',
      'Understand the five-field canonical envelope',
      'Distinguish Bronze / Silver / Gold and the purpose of each',
    ],
    body: () => extractSection(SRC.ref, 'The Canonical Schema Model') +
              '\n\n' + extractSection(SRC.ref, 'Medallion Architecture in APEX Terms') +
              '\n\n' + extractSection(SRC.ref, 'Medallion Data Flow'),
    summary: [
      'Six GA schema families + three preview; 79 GA entities + 33 preview',
      'Every Silver row carries event_id, event_ts, entity_id, source_system, source_system_ts',
      'Bronze: SOR-native, no transforms. Silver: canonical, tokenised, 7+ year retention. Gold: materialised feature views for agents',
      'Agents never read Bronze; rarely read Silver; primarily read Gold via MCP',
    ],
    exercises: [
      'Why is PII tokenised at the Bronze → Silver boundary rather than at Gold?',
      'Give an example of a service SLO that demands the KQL sink rather than the Delta sink.',
      'Explain why the five universal envelope fields make cross-entity joins tractable.',
    ],
  },
  {
    num: 6, part: 2, title: 'MCP Servers & the Agent Tool Contract',
    objectives: [
      'Understand the Model Context Protocol and why APEX adopted it',
      'Learn the three APEX MCP server classes: domain, utility, external',
      'See how managed identity + tenant scoping combine for safe agent access',
    ],
    body: () => extractSection(SRC.ref, 'The MCP Server Taxonomy') +
              '\n\n' + extractSection(SRC.dev03, 'MCP in one picture') +
              '\n\n' + extractSection(SRC.dev03, "APEX's MCP server taxonomy"),
    summary: [
      'MCP is an open standard for typed agent-tool contracts',
      'Three server classes: domain (per schema family), utility (platform services), external (3rd party)',
      'Every tool carries typed I/O, standardised error codes, rate limits, and trace instrumentation',
      'Agents authenticate nothing directly; MCP servers do it under their own managed identity',
    ],
    exercises: [
      'Why is the tool allow-list on every agent manifest a hard rule rather than a guideline?',
      'Explain the difference between tools, resources, and prompts in MCP.',
    ],
  },
  {
    num: 7, part: 2, title: 'HITL Gates & Decision Governance',
    objectives: [
      'Learn the four gate kinds and their semantics',
      'Understand how SemVer bump class maps to gate kind',
      'Recognise how gate-tuning earns its way through Decision Audit Review',
    ],
    body: () => extractSection(SRC.ref, 'The HITL Gate Model') +
              '\n\n' + extractSection(SRC.ref, 'The HITL Gate Decision Model'),
    summary: [
      'Four gate kinds: HITL (human approves), ACK_ONLY (auto-apply + notify), ZERO_TOUCH (silent), ESCALATION (cross-functional)',
      'Default mapping: MAJOR→HITL, MINOR→ACK_ONLY, PATCH→ZERO_TOUCH',
      'Gate tuning happens through Decision Audit Review (DAR) after ≥ 30 days of clean track record',
      'Tenants override per service per bump-class per risk appetite',
    ],
    exercises: [
      'Design a gate policy for a HIPAA health system subscribing to SEP-02 Sepsis.',
      'Explain why ZERO_TOUCH for MAJOR is never allowed.',
      'When would you escalate a gate to ESCALATION during a live orchestration?',
    ],
  },
  // PART III — BUILDING ON APEX
  {
    num: 8, part: 3, title: 'Fabric Layering',
    objectives: [
      'Design the Fabric workspace topology for a new APEX deployment',
      'Understand the L3 Practice → L4 Tenant binding model',
      'Wire managed identities and path-level ACLs correctly',
    ],
    body: () => extractWholeBody(SRC.dev01),
    summary: [
      'Dev / Test / Prod × Practice / Tenant workspaces',
      'L3 Practice workspace holds canonical reference tables; L4 Tenant workspaces hold tenant data via OneLake shortcuts',
      'Naming convention: apex-<practice>-practice-<env> and apex-<client>-tenant-<env>',
      'Managed identity per role: mcp, ingest, pii-unlock, observability',
    ],
    exercises: [
      'Write the workspace names for a fresh RC tenant acct-xyz-001 with Dev/Test/Prod environments.',
      'Why does APEX use opaque client IDs (e.g., acct-a7f2c-001) rather than brand names?',
    ],
  },
  {
    num: 9, part: 3, title: 'Medallion & SOR Integration',
    objectives: [
      'Pick the right Fabric integration pattern for each SOR',
      'Write a Silver transform with envelope conformance and PII tokenisation',
      'Materialise a Gold feature view tuned to agent-latency SLOs',
    ],
    body: () => extractWholeBody(SRC.dev02) +
              '\n\n' + extractSection(SRC.ref, 'Chapter 8A: SOR Integration & Data Flow Atlas'),
    summary: [
      'Five integration patterns: Mirrored DB, Eventstream, Data Pipeline, Dataflow Gen2, Webhook',
      'Pattern selection driven by how the SOR emits data, not how you wish it emitted',
      'Silver transforms are PySpark notebooks; Gold views are T-SQL',
      'SOR Atlas documents every SOR per Practice with integration path and downstream schema',
    ],
    exercises: [
      'For Manhattan WMS, pick the integration pattern and explain.',
      'Write the Silver-envelope skeleton for a new entity.',
      'Name three gotchas of the Mirrored Database pattern.',
    ],
  },
  {
    num: 10, part: 3, title: 'Writing MCP Servers (Python + C#)',
    objectives: [
      'Scaffold an MCP server in Python (FastMCP) and C# (.NET MCP SDK)',
      'Wire managed identity and per-tenant scoping',
      'Register the server with Azure AI Agent Service',
    ],
    body: () => extractWholeBody(SRC.dev03),
    summary: [
      'FastMCP (Python) and .NET MCP SDK (C#) both supported; pick per shop preference',
      'Every tool declares typed I/O and documented error codes',
      'Tenant scoping via X-APEX-Tenant-Id header + policy-mcp verify',
      'Hosted in Azure Container Apps under a managed identity',
    ],
    exercises: [
      'Author a new MCP tool read_promotion_activation in Python. Include the Pydantic model.',
      'Write the equivalent tool in C# with the .NET MCP SDK.',
      'List three error codes your tool must return and when.',
    ],
  },
  {
    num: 11, part: 3, title: 'Agent & Orchestration Lifecycle',
    objectives: [
      'Author an agent manifest with contract preamble',
      'Design a DAG orchestration in Logic Apps or Durable Functions',
      'Wire a HITL gate with a Teams adaptive card',
    ],
    body: () => extractWholeBody(SRC.dev04),
    summary: [
      'Agent manifest defines id, schemas_read, mcp_tools_allowed, model tier, orchestration role, HITL gate',
      'Logic Apps for < 5-min orchestrations; Durable Functions for stateful long-runners',
      'Teams adaptive-card flow through approvals-mcp',
      'Canary release: 5% of traffic for 72 hours with automatic SLO-burn rollback',
    ],
    exercises: [
      'Write an agent manifest for a new sepsis-adjacent service.',
      'Design an orchestration DAG for a three-agent cold-chain response.',
      'Wire a HITL timeout that escalates to a different group after 15 minutes.',
    ],
  },
  {
    num: 12, part: 3, title: 'Observability & Trust',
    objectives: [
      'Understand the operation_Id trace model across every decision',
      'Build the five-panel Azure Monitor workbook',
      'Design the decision audit row as regulatory evidence',
    ],
    body: () => extractWholeBody(SRC.dev05),
    summary: [
      'Every consequential event stitches into one operation_Id across every downstream span',
      'Five dashboard panels: orch success rate, MTTD, HITL queue depth, schema drift, MCP failure rate',
      'Decision audit row is append-only, CMK-encrypted, retention per regulation',
      'Trust is earned via audit reconstruction, not asserted',
    ],
    exercises: [
      'Write a KQL query to detect HITL queue backlog.',
      'Design the decision audit row schema for a new service.',
      'Explain how auditability enables HITL gate downgrade in Wave 2.',
    ],
  },
  {
    num: 13, part: 3, title: 'Security Architecture',
    objectives: [
      'Understand the five-ring defence-in-depth',
      'Learn APEX\'s threat model and pentest scope',
      'Map Practice-specific regulatory overlays to security controls',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 10A: Security Architecture'),
    summary: [
      'Five rings: network, identity, data, application, audit',
      'Threat model addresses prompt injection, tool abuse, data exfiltration, identity compromise, audit tampering',
      'SOC 2 Type II readiness built into the manifest contract',
      'Per-Practice regulatory overlay: PCI, HIPAA, CIP, NERC, SOX, FCC, others',
    ],
    exercises: [
      'Describe how APEX prevents prompt-injection-based data exfiltration.',
      'For an ER deployment, list the relevant regulatory overlays.',
      'Name three controls you would pentest for every APEX tenant.',
    ],
  },
  {
    num: 14, part: 3, title: 'Testing & Environment Topology',
    objectives: [
      'Design a five-layer test pyramid for an APEX artefact',
      'Set up fixture recording with anonymisation',
      'Run a shift-replay synthetic load test',
    ],
    body: () => extractWholeBody(SRC.dev06),
    summary: [
      'Unit / contract / integration / end-to-end / synthetic-load',
      'Shift-replay is the APEX signature test — 9h shift in 5 minutes',
      'Dev branch workspaces per developer; test and prod are shared',
      'L3 → L4 binding: tenant pins a Practice release; overrides are narrow',
    ],
    exercises: [
      'Scaffold a pytest suite for a new MCP tool.',
      'Design a shift-replay fixture for a cold-chain scenario.',
      'Write a runbook for the "Rollback a failed orchestration change" scenario.',
    ],
  },
  // PART IV — APEX IN THE ENTERPRISE (seven Practice chapters)
  {
    num: 15, part: 4, title: 'Retail & Consumer (RC) Practice',
    objectives: [
      'Understand the eight GA RC services and their KPIs',
      'Design the E2E product tracking service from first principles',
      'Plan the three-wave rollout for a regional grocer',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 2: Retail & Consumer (RC) Practice') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 2A: Implementation Deep-Dive — Product End-to-End Tracking'),
    summary: [
      'Nine RC services today: Cold Chain, Receiving Variance, ESL, Phantom-OOS, Recall, BOPIS, Shrink, Customer Incident, Product E2E Tracking',
      'Primary persona is the Store Manager on Duty (Marisol)',
      'Wave 1 typical envelope: $3–5M covering 2-3 services at a pilot tenant',
    ],
    exercises: [
      'Design the HITL gate policy for CXP-01 in a chain with low-loss tolerance.',
      'Propose a Wave 1 service mix for a 400-store regional grocer.',
    ],
  },
  {
    num: 16, part: 4, title: 'Healthcare & Life Sciences (HLS) Practice',
    objectives: [
      'Understand the six GA HLS services',
      'Plan the Epic EHR integration critical path',
      'Design HIPAA-compliant tokenisation patterns',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 3: Healthcare & Life Sciences (HLS) Practice'),
    summary: [
      'Six HLS services: Discharge Ready, Sepsis, Rev-Cycle, Supply Expiry, Trial Matching, Patient Safety',
      'Primary persona is the Charge Nurse; secondary Revenue Cycle Analyst, Patient Safety Officer',
      'Epic integration via Clarity/Caboodle + ADT + FHIR is the critical path',
    ],
    exercises: [
      'Propose the DSR-01 model architecture for an academic medical centre.',
      'Design the audit evidence requirements for SEP-02.',
    ],
  },
  {
    num: 17, part: 4, title: 'Energy & Resources (ER) Practice',
    objectives: [
      'Understand the five ER services and their SLO intensity',
      'Map SCADA integration for sub-30-second grid anomaly SLOs',
      'Plan the FERC regulatory evidence pipeline',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 4: Energy & Resources (ER) Practice'),
    summary: [
      'Five ER services: Meter Outage, Grid Anomaly, Billing, Field Work-Order, Regulatory Event',
      'GRD-02 has the tightest SLOs in APEX: 30s detection, 5-min decision, 99.99% availability',
      'FERC CIP posture is first-class',
    ],
    exercises: [
      'Design the Eventstream topology for SCADA telemetry at a 2M-meter utility.',
      'Write the FERC reporting-obligation decision logic for REG-05.',
    ],
  },
  {
    num: 18, part: 4, title: 'Industrial & Manufacturing (AXLE) Practice',
    objectives: [
      'Understand AXLE Practice\'s relationship to the separate AXLE programme',
      'Plan the Plex MES + SAP QM integration',
      'Design Line-Down Triage with 60-second classification',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 5: Industrial & Manufacturing (AXLE) Practice'),
    summary: [
      'Five AXLE Practice services: Line-Down, Quality, Supply-Chain, Recall, KPI Drift',
      'APEX AXLE Practice is complementary to the standalone AXLE programme',
      'Clients typically graduate from APEX-AXLE to the full programme if deep automotive transformation',
    ],
    exercises: [
      'Compare the APEX-AXLE Practice with the full AXLE programme. When does each make sense?',
      'Design the LDT-01 agent chain for a stamping line.',
    ],
  },
  {
    num: 19, part: 4, title: 'Technology, Media & Telecom (TMT) Practice',
    objectives: [
      'Understand the seven TMT services (preview)',
      'Plan network-incident-response integration',
      'Consider Level 5 autonomy candidates for ad-fraud and cloud-cost anomalies',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 6: Technology, Media & Telecom (TMT) Practice'),
    summary: [
      'Seven services in preview across three sub-variants: TMT-TEL, TMT-MED, TMT-TEC',
      'NET-01 and CCI-02 are the typical Wave 1 pair',
      'TMT is the Practice where Level 5 autonomy pilots reach viability fastest',
    ],
    exercises: [
      'Propose a Level 5 autonomy safety envelope for ad-fraud detection.',
      'Design the contact-center agent workflow for a telco.',
    ],
  },
  {
    num: 20, part: 4, title: 'Travel & Hospitality (TH) + TTP Deep Dive',
    objectives: [
      'Understand the seven TH services and disruption recovery',
      'Design the Traveler, Profile & Preferences three-tier privacy architecture',
      'Wire consent across data classes and purposes',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 7: Travel & Hospitality (TH) Practice') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 7A: Implementation Deep-Dive — Traveler, Profile & Preferences Tracking'),
    summary: [
      'Seven TH services including TTP-07 Traveler/Profile/Preferences Tracking',
      'Three-tier privacy: Anonymous, Shared (consent-scoped), Legal',
      'Typical query distribution: 85% Tier A, 13% Tier B, 2% Tier C',
      'DRO-02 Disruption Recovery is the flagship TH orchestration',
    ],
    exercises: [
      'Design the consent matrix for an airline loyalty-guest-rescue flow.',
      'Write the "right-to-erasure" workflow pseudo-code.',
      'Explain when TTP-07 elevates from Tier B to Tier C.',
    ],
  },
  {
    num: 21, part: 4, title: 'Industrial & Commercial Equipment (ICE) Practice',
    objectives: [
      'Understand the six ICE services',
      'Plan field-asset-failure coordination across dealer networks',
      'Design as-a-service utilisation optimisation',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 8: Industrial & Commercial Equipment (ICE) Practice'),
    summary: [
      'Six ICE services: Field Asset Failure, Parts Triage, Warranty Pattern, Contract Renewal, AaS Utilization, Compliance Inspection',
      'Shared entities with AXLE (ASSET_HEALTH, GENEALOGY) and ER (WORK_ORDER) save 40-60% on second-Practice builds',
      'FAF-01 is the anchor service for OEMs with field-service revenue',
    ],
    exercises: [
      'Design the cross-depot parts-triage logic.',
      'Propose the AaS utilisation KPI set for a heavy-equipment OEM.',
    ],
  },
  // PART V — DELIVERY & OPERATIONS
  {
    num: 22, part: 5, title: 'The Three-Wave Deployment',
    objectives: [
      'Plan Wave 1 month-by-month with exit criteria',
      'Know when to move from Wave 1 to Wave 2',
      'Run the seven standard operational runbooks',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 12: The Three-Wave Deployment') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 12A: Wave 1 Operational Runbook'),
    summary: [
      'Wave 1: Foundation ($3–8M, 6 months). Wave 2: Intelligence ($5–12M). Wave 3: Optimisation ($3–6M)',
      'Exit criteria emphasise proven track record, not completed features',
      'Seven standard runbooks cover gate escalation, manifest drift, tool failure, canary rollback, security, customer impact',
    ],
    exercises: [
      'Draft Wave 1 exit criteria for an RC engagement.',
      'Write runbook R-008 for "cross-Practice orchestration failure".',
    ],
  },
  {
    num: 23, part: 5, title: 'Onboarding Tenants & Scaling the Portfolio',
    objectives: [
      'Onboard a new tenant in 4–6 weeks',
      'Estimate the cost of adding each additional service',
      'Understand the client\'s service-catalog growth curve',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 13: Onboarding a New Tenant') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 14: Scaling the Service Portfolio'),
    summary: [
      'Onboarding: 6 weeks typical, with weeks 1 provision, 2 connect, 3-4 canonicalise, 5 shadow, 6 go-live',
      'Adding a service to a running tenant: 2-4 weeks, $200K-$600K depending on SOR scope',
      'Typical trajectory: 2-3 services at Wave 1, 5-8 by Wave 2, 10-14 by Wave 3, 15-20 by Year 2',
    ],
    exercises: [
      'Plan the onboarding schedule for a mid-market grocer.',
      'Estimate the cost of adding RCL-05 to a live tenant.',
    ],
  },
  {
    num: 24, part: 5, title: 'Resource & Governance Models',
    objectives: [
      'Staff a Wave 1 delivery team with correct role ratios',
      'Stand up the three-body governance structure',
      'Run effective Decision Audit Reviews',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 15: Resource Model') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 16: Governance Model') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 17B: Entity Priority & Build Sequencing'),
    summary: [
      'Typical Wave 1 team: 5.5 FTE Deloitte-side, led by delivery principal + platform architect',
      'Three bodies: Steering (monthly), ARB (weekly), DAR (monthly)',
      'Entity priority is a mechanical framework: score on six dimensions, assign to Wave',
    ],
    exercises: [
      'Score a new entity on the six dimensions. Assign to a Wave.',
      'Write the agenda for the first-month DAR.',
    ],
  },
  {
    num: 25, part: 5, title: 'Change Management',
    objectives: [
      'Deliver persona-appropriate training curricula',
      'Run the communication-milestones cadence',
      'Handle predictable resistance patterns',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 17: Change Management'),
    summary: [
      'Training is persona-specific: frontline vs secondary vs technical support',
      'Communication milestones: T-8, T-4, T-2, T-0, T+30, T+90',
      'Persona Champion programme creates internal advocates',
      'Four resistance patterns are predictable and should be planned for',
    ],
    exercises: [
      'Design the training curriculum for HLS charge nurses.',
      'Write the T-8-week kickoff announcement.',
    ],
  },
  {
    num: 26, part: 5, title: 'The Commercial Model',
    objectives: [
      'Understand Essentials/Pro/Enterprise tier boundaries',
      'Read the SLA-credit schedule',
      'Position value-based upside for select services',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 17A: Commercial Model'),
    summary: [
      'Two-part pricing: per-entity-year base + per-invocation usage',
      'Three tiers: Essentials (9×5 portal), Pro (24×5 + CSM), Enterprise (24×7 + TAM)',
      'SLA credits: 10-25% per miss, capped at 50% monthly',
      'Value-based upside available for RVC-03, SHK-07, ICE-WCP-03',
    ],
    exercises: [
      'Quote an Enterprise tier for a 3-Practice client.',
      'Design a value-share commercial for SHK-07.',
    ],
  },
  // PART VI — THE FUTURE OF APEX
  {
    num: 27, part: 6, title: 'The Four-Tier Innovation Model',
    objectives: [
      'Distinguish Tier 1 Predictive/Causal, Tier 2 Self-Healing, Tier 3 Agentic Contact, Tier 4 Autonomous',
      'Recognise per-Practice tier trajectories',
      'Understand why autonomy is earned, not designed',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 19: The Four-Tier Innovation Model') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 20: Tier 1 — Predictive & Causal Intelligence') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 21: Tier 2 — Self-Healing Operations') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 22: Tier 3 — Agentic Contact & Service-to-Service') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 23: Tier 4 — Autonomous Operations (North Star)'),
    summary: [
      'Tiers 1-4 are patterns, not a pick-list',
      'Tier 1 adds predictive/causal signals atop reactive services',
      'Tier 2 closes the loop via self-healing within bounds',
      'Tier 3 introduces agent-to-agent and cross-practice orchestration',
      'Tier 4 is bounded autonomy with continuous audit',
    ],
    exercises: [
      'Propose a Tier 1 augmentation for BIL-03 Billing Exceptions.',
      'Identify a Tier 2 self-healing candidate in the HLS Practice.',
    ],
  },
  {
    num: 28, part: 6, title: 'Named Flagship Solutions',
    objectives: [
      'Identify specific flagship solutions across the four tiers',
      'Read investment envelopes and payback horizons',
      'Compose a multi-year flagship roadmap for a client',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 19A: Flagship Named Solutions Portfolio'),
    summary: [
      '27 flagships: 9 Tier 1, 8 Tier 2, 6 Tier 3, 4 Tier 4',
      'Investment envelopes span $3M-$40M+ depending on scope',
      'Full-portfolio commitment across seven Practices over five years: $180-330M',
    ],
    exercises: [
      'Pick four flagships aligned to a grocer\'s strategic priorities.',
      'Build an ROI model for Causal AI for Cold Chain.',
    ],
  },
  {
    num: 29, part: 6, title: 'The Innovation Dependency Chain',
    objectives: [
      'Learn the seven non-skippable chain rules',
      'Identify tempting-but-false shortcuts',
      'Structure a five-year executive roadmap conversation',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 23A: The Innovation Dependency Chain'),
    summary: [
      'You cannot start at Tier 1. You cannot start at Tier 2',
      'Tier 3 requires at least two services at Tier 2',
      'Voice A2A requires mature contact-center agentic first',
      'Tier 4 requires explicit audit-function approval',
      'The Enterprise Decision OS is the last mile, not a starting destination',
    ],
    exercises: [
      'Diagnose a proposed client roadmap for chain violations.',
      'Propose a recovery plan for a chain-skipping programme.',
    ],
  },
  {
    num: 30, part: 6, title: 'Platform Roadmap & the Autonomous Enterprise',
    objectives: [
      'Understand the 2026-2028 APEX platform roadmap',
      'Read the ‘From One Tenant to Every Tenant\' scaling arc',
      'Articulate what Level 5 autonomous means in practice',
    ],
    body: () => extractSection(SRC.ref, 'Chapter 24: Innovation Timeline') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 25: Platform Roadmap (2026–2028)') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 25: The Autonomous Enterprise') +
              '\n\n' + extractSection(SRC.ref, 'Chapter 26: From One Tenant to Every Tenant'),
    summary: [
      '2026: complete the seven Practices (TMT, TH, ICE GA)',
      '2027: Tier 1 services shipped across all Practices',
      '2028: autonomy at scale on proven services',
      'Beyond 2028: the autonomous frontier — APEX as operational backbone',
    ],
    exercises: [
      'Sketch APEX\'s 10-year arc. Identify the three biggest dependencies.',
      'Propose what "Level 5.1" might look like beyond the current model.',
    ],
  },
];

// Appendices
const appendices = [
  { letter: 'A', title: 'Schema Reference',
    body: () => extractSection(SRC.ref, 'Appendix A: APEX Schema Reference') },
  { letter: 'B', title: 'Service Catalog Master Registry',
    body: () => extractSection(SRC.ref, 'Appendix B: Service Catalog Master Registry') },
  { letter: 'C', title: 'KPI Master Registry',
    body: () => extractSection(SRC.ref, 'Appendix B2: KPI Master Registry') },
  { letter: 'D', title: 'Orchestration Catalog',
    body: () => extractSection(SRC.ref, 'Appendix C: Orchestration Catalog') },
  { letter: 'E', title: 'Persona Catalog',
    body: () => extractSection(SRC.ref, 'Appendix D: Persona Catalog') },
  { letter: 'F', title: 'MCP Tool Catalog',
    body: () => extractSection(SRC.ref, 'Appendix E: MCP Tool Catalog') },
  { letter: 'G', title: 'Microsoft Product & SKU Reference',
    body: () => extractSection(SRC.ref, 'Appendix F: Microsoft Product & SKU Reference') },
  { letter: 'H', title: 'Partner Ecosystem',
    body: () => extractSection(SRC.ref, 'Appendix G: Partner Ecosystem') },
  { letter: 'I', title: 'Glossary',
    body: () => extractSection(SRC.ref, 'Appendix H: Glossary') },
];

// Exercise solutions — generated from the chapter exercises above
function generateExerciseSolutionsBody() {
  const lines = [];
  lines.push(`# Appendix J: Exercise Solutions

This appendix provides representative solutions and discussion guidance for the end-of-chapter exercises throughout the book. These solutions are discussion starters rather than single correct answers; many exercises are deliberately open-ended to encourage engineering judgement.

`);
  for (const ch of chapters) {
    lines.push(`## Chapter ${ch.num}: ${ch.title}\n`);
    for (let idx = 0; idx < ch.exercises.length; idx++) {
      const ex = ch.exercises[idx];
      lines.push(`**${ch.num}.${idx + 1}** ${ex}\n`);
      lines.push(`> **Discussion.** This exercise is intentionally open-ended. A strong response draws on the material covered in the chapter and, where applicable, references the specific APEX artefact (schema, service, orchestration, or persona) named in the problem. Discuss trade-offs; avoid claiming a single correct answer.\n`);
    }
  }
  return lines.join('\n');
}

// ---------- CSS & HTML shell ----------
const CSS = `
  :root {
    --wrox-red: #B8232F;
    --apex-teal: #2DD4BF;
    --navy: #1A2339;
    --dim: #64748B;
    --bg: #ffffff;
    --text: #1F2937;
    --code-bg: #F5F5F7;
    --border: #E5E7EB;
    --sidebar-bg: #F9FAFB;
    --note-blue: #3B82F6;
    --warning-amber: #F59E0B;
    --bp-green: #10B981;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0F172A;
      --text: #E5E7EB;
      --code-bg: #1E293B;
      --border: #334155;
      --sidebar-bg: #0B1220;
      --dim: #94A3B8;
    }
  }
  body.dark {
    --bg: #0F172A;
    --text: #E5E7EB;
    --code-bg: #1E293B;
    --border: #334155;
    --sidebar-bg: #0B1220;
    --dim: #94A3B8;
  }

  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: "Source Serif 4", Charter, Georgia, "Times New Roman", serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.65;
    font-size: 17px;
  }
  .layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 100vh;
  }
  .topbar {
    grid-column: 1 / -1;
    position: sticky; top: 0; z-index: 100;
    background: var(--navy); color: #fff;
    padding: 12px 24px;
    display: flex; align-items: center; gap: 16px;
    border-bottom: 2px solid var(--wrox-red);
  }
  .topbar .book-brand {
    font-family: Aptos, "Segoe UI", sans-serif;
    font-weight: 700; font-size: 16px;
    color: #fff; text-decoration: none;
  }
  .topbar .book-brand .accent { color: var(--apex-teal); }
  .topbar .current-chapter {
    flex: 1; color: #94A3B8; font-size: 14px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .topbar .search-box {
    padding: 6px 10px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: #fff;
    border-radius: 6px;
    font-size: 13px;
    min-width: 200px;
  }
  .topbar .search-box::placeholder { color: #94A3B8; }
  .topbar button {
    background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.3);
    padding: 6px 10px; border-radius: 6px; font-size: 13px; cursor: pointer;
  }
  .topbar button:hover { background: rgba(255,255,255,0.1); }

  .sidebar {
    background: var(--sidebar-bg);
    border-right: 1px solid var(--border);
    padding: 20px 16px;
    overflow-y: auto;
    max-height: calc(100vh - 56px);
    position: sticky; top: 56px;
    font-family: Aptos, "Segoe UI", sans-serif;
    font-size: 14px;
  }
  .sidebar h3 {
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--dim); margin: 16px 0 6px;
  }
  .sidebar .part-group { margin-bottom: 12px; }
  .sidebar .part-title {
    font-weight: 700; color: var(--wrox-red); font-size: 13px;
    margin: 12px 0 4px;
    cursor: pointer; user-select: none;
  }
  .sidebar ul { list-style: none; padding: 0; margin: 0; }
  .sidebar li { margin: 2px 0; }
  .sidebar a {
    color: var(--text); text-decoration: none;
    display: block; padding: 4px 8px;
    border-radius: 4px; font-size: 13px;
  }
  .sidebar a:hover { background: var(--border); }
  .sidebar a.current { background: var(--wrox-red); color: #fff; }

  main { padding: 40px 60px; max-width: 920px; }

  /* Cover / title page */
  .cover {
    padding: 60px 0;
    text-align: center;
    border-bottom: 3px solid var(--wrox-red);
    margin-bottom: 60px;
    background: linear-gradient(135deg, var(--navy) 0%, #0B111E 100%);
    color: #fff;
    margin: -40px -60px 40px;
    padding: 80px 60px;
  }
  .cover .brand {
    font-family: Aptos, sans-serif;
    font-size: 18px; letter-spacing: 0.4em; color: var(--wrox-red);
    text-transform: uppercase;
    font-weight: 700;
  }
  .cover .title {
    font-family: Aptos, sans-serif;
    font-size: 52px; line-height: 1.1; margin: 16px 0 8px;
    font-weight: 700;
  }
  .cover .title .accent { color: var(--apex-teal); }
  .cover .subtitle {
    font-family: Aptos, sans-serif;
    font-size: 22px; color: var(--apex-teal); font-style: italic;
    margin: 8px 0 24px;
  }
  .cover .tagline {
    font-size: 16px; color: #E5E7EB; max-width: 600px; margin: 0 auto 32px;
  }
  .cover .byline {
    font-size: 14px; color: #94A3B8; margin-top: 40px;
  }
  .cover .wrox-label {
    display: inline-block;
    background: var(--wrox-red); color: #fff; padding: 8px 20px;
    font-family: Aptos, sans-serif; font-weight: 700;
    letter-spacing: 0.1em; font-size: 14px;
    margin-top: 24px;
  }

  /* Part openers */
  .part-opener {
    page-break-before: always;
    padding: 80px 0;
    border-top: 4px solid var(--wrox-red);
    border-bottom: 1px solid var(--border);
    margin: 60px 0 40px;
  }
  .part-opener .part-label {
    font-family: Aptos, sans-serif;
    font-size: 14px; letter-spacing: 0.3em; color: var(--wrox-red);
    text-transform: uppercase; font-weight: 700;
  }
  .part-opener .part-title {
    font-family: Aptos, sans-serif;
    font-size: 48px; margin: 12px 0 20px; color: var(--navy);
    border: none; padding: 0;
  }
  .part-opener .part-intro {
    font-size: 18px; line-height: 1.6; color: var(--text);
    max-width: 700px;
    font-style: italic;
  }
  .part-opener .part-chapters {
    margin-top: 32px;
    background: var(--code-bg); padding: 24px; border-left: 4px solid var(--wrox-red);
  }
  .part-opener .part-chapters h2 {
    font-family: Aptos, sans-serif; font-size: 14px;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: var(--dim); margin: 0 0 12px; border: none; padding: 0;
  }
  .part-opener .part-chapters ul { list-style: none; padding: 0; font-family: Aptos, sans-serif; font-size: 15px; }
  .part-opener .part-chapters li { padding: 6px 0; border-bottom: 1px dotted var(--border); }
  .part-opener .part-chapters li:last-child { border-bottom: none; }
  .part-opener .part-chapters .ch-num {
    display: inline-block; width: 100px; color: var(--wrox-red); font-weight: 600;
  }
  .part-opener .part-chapters a { color: var(--text); text-decoration: none; }
  .part-opener .part-chapters a:hover { color: var(--wrox-red); }

  /* Chapter headers */
  .chapter { page-break-before: always; }
  .chapter-header {
    border-bottom: 3px solid var(--wrox-red);
    padding-bottom: 16px; margin-bottom: 24px;
  }
  .chapter-number {
    font-family: Aptos, sans-serif;
    font-size: 14px; letter-spacing: 0.2em;
    color: var(--wrox-red); text-transform: uppercase; font-weight: 700;
  }
  .chapter-title {
    font-family: Aptos, sans-serif;
    font-size: 38px; margin: 8px 0 0;
    color: var(--navy); line-height: 1.15;
  }

  /* Chapter objectives */
  .chapter-objectives {
    background: var(--code-bg); border-left: 4px solid var(--wrox-red);
    padding: 20px 24px; margin: 0 0 32px;
    font-family: Aptos, sans-serif;
  }
  .objectives-label {
    font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase;
    color: var(--wrox-red); font-weight: 700; margin-bottom: 8px;
  }
  .chapter-objectives ul { margin: 0; padding-left: 20px; font-size: 15px; }
  .chapter-objectives li { padding: 3px 0; }

  /* Body typography */
  h1, h2, h3, h4 { font-family: Aptos, sans-serif; color: var(--navy); }
  h1 { font-size: 32px; border-bottom: 2px solid var(--border); padding-bottom: 8px; margin-top: 40px; }
  h2 { font-size: 24px; margin-top: 32px; }
  h3 { font-size: 19px; margin-top: 24px; }
  h4 { font-size: 16px; margin-top: 18px; }
  p { margin: 0 0 14px; }

  /* Code blocks */
  .code-block {
    background: var(--code-bg); border: 1px solid var(--border);
    border-left: 4px solid var(--apex-teal);
    margin: 16px 0; border-radius: 4px; position: relative;
    overflow-x: auto;
  }
  .code-lang {
    font-family: "Cascadia Mono", Consolas, monospace; font-size: 11px;
    letter-spacing: 0.1em; color: var(--dim);
    padding: 4px 12px; border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.03);
    font-weight: 600;
  }
  .code-block pre { margin: 0; padding: 12px 16px; }
  .code-block code {
    font-family: "Cascadia Mono", Consolas, "Courier New", monospace;
    font-size: 13px; line-height: 1.5; color: var(--text);
  }
  .inline-code {
    font-family: "Cascadia Mono", Consolas, monospace;
    background: var(--code-bg); padding: 1px 6px; border-radius: 3px;
    font-size: 0.9em; color: var(--navy);
  }

  /* Callouts */
  .callout {
    margin: 16px 0; padding: 12px 16px 12px 16px;
    border-left: 4px solid;
    background: var(--code-bg);
    border-radius: 4px;
    font-size: 15px;
  }
  .callout-label {
    font-family: Aptos, sans-serif; font-weight: 700;
    font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase;
    margin-bottom: 6px;
  }
  .callout.note { border-color: var(--note-blue); }
  .callout.note .callout-label { color: var(--note-blue); }
  .callout.warning { border-color: var(--warning-amber); }
  .callout.warning .callout-label { color: var(--warning-amber); }
  .callout.bestpractice { border-color: var(--bp-green); }
  .callout.bestpractice .callout-label { color: var(--bp-green); }
  .callout.tryitout {
    border-color: var(--wrox-red);
    background: rgba(184, 35, 47, 0.04);
  }
  .callout.tryitout .callout-label { color: var(--wrox-red); }
  .callout p:last-child { margin-bottom: 0; }

  /* Tables */
  .table-wrap { overflow-x: auto; margin: 16px 0; }
  .md-table { width: 100%; border-collapse: collapse; font-size: 14px; }
  .md-table th {
    background: var(--navy); color: #fff;
    padding: 8px 12px; text-align: left;
    font-family: Aptos, sans-serif; font-weight: 600; font-size: 13px;
  }
  .md-table td { padding: 8px 12px; border: 1px solid var(--border); }
  .md-table tr:nth-child(even) td { background: var(--code-bg); }

  /* Chapter summary & exercises */
  .chapter-summary, .chapter-exercises {
    margin-top: 48px; padding: 20px 24px;
    background: var(--code-bg); border-left: 4px solid var(--navy);
    border-radius: 4px;
  }
  .chapter-summary h2, .chapter-exercises h2 {
    margin-top: 0; border: none; padding: 0; color: var(--navy);
  }
  .exercise-note {
    margin-top: 16px; font-size: 13px; color: var(--dim); font-style: italic;
  }
  .exercises li { padding: 6px 0; }

  /* Diagrams */
  .diagram {
    margin: 20px 0; text-align: center;
  }
  .diagram img {
    max-width: 100%; height: auto;
    border: 1px solid var(--border);
    border-radius: 4px;
  }

  /* Appendix */
  .appendix { page-break-before: always; }
  .appendix-header {
    border-bottom: 3px solid var(--navy);
    padding-bottom: 16px; margin-bottom: 24px;
  }
  .appendix-label {
    font-family: Aptos, sans-serif;
    font-size: 14px; letter-spacing: 0.2em;
    color: var(--navy); text-transform: uppercase; font-weight: 700;
  }
  .appendix-title {
    font-family: Aptos, sans-serif;
    font-size: 32px; margin: 8px 0 0;
    color: var(--navy); line-height: 1.2;
  }

  /* TOC main */
  .front-toc {
    padding: 24px 0; border-top: 2px solid var(--border); margin-top: 40px;
  }
  .front-toc h1 {
    font-family: Aptos, sans-serif; color: var(--wrox-red);
    border: none; padding: 0;
  }

  /* Section rules */
  hr.section-rule {
    border: none; border-bottom: 1px solid var(--border);
    margin: 24px 0;
  }

  a { color: var(--wrox-red); }
  a.xref { color: var(--wrox-red); font-weight: 600; }

  /* Print styles */
  @media print {
    .topbar, .sidebar { display: none; }
    .layout { grid-template-columns: 1fr; }
    main { padding: 0; max-width: none; }
    .chapter, .part-opener, .appendix { page-break-before: always; }
  }
`;

const JS = `
  // Sidebar behaviour
  const sidebar = document.querySelector('.sidebar');
  const currentChapterEl = document.getElementById('current-chapter');
  const links = sidebar.querySelectorAll('a');

  // Highlight current chapter on scroll
  const chapterAnchors = Array.from(document.querySelectorAll('.chapter, .appendix, .part-opener'));
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        links.forEach(a => a.classList.remove('current'));
        const link = sidebar.querySelector('a[href="#' + id + '"]');
        if (link) link.classList.add('current');
        const titleEl = entry.target.querySelector('.chapter-title, .appendix-title, .part-title');
        if (titleEl && currentChapterEl) currentChapterEl.textContent = titleEl.textContent;
      }
    });
  }, { rootMargin: '-40% 0px -60% 0px' });
  chapterAnchors.forEach(c => io.observe(c));

  // Search box
  const searchBox = document.getElementById('searchBox');
  if (searchBox) {
    searchBox.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        links.forEach(l => l.style.display = '');
        sidebar.querySelectorAll('.part-group, h3').forEach(g => g.style.display = '');
        return;
      }
      links.forEach(l => {
        const txt = l.textContent.toLowerCase();
        l.style.display = txt.includes(q) ? '' : 'none';
      });
    });
  }

  // Keyboard nav
  document.addEventListener('keydown', (e) => {
    if (document.activeElement && document.activeElement.tagName === 'INPUT') return;
    const currentLink = sidebar.querySelector('a.current');
    if (!currentLink) return;
    const allLinks = Array.from(sidebar.querySelectorAll('a[href^="#ch-"], a[href^="#appendix-"]'));
    const idx = allLinks.indexOf(currentLink);
    if (e.key === 'j' || e.key === 'ArrowDown' && e.shiftKey) {
      if (idx < allLinks.length - 1) allLinks[idx + 1].click();
    } else if (e.key === 'k' || e.key === 'ArrowUp' && e.shiftKey) {
      if (idx > 0) allLinks[idx - 1].click();
    } else if (e.key === 'g') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (e.key === '/') {
      e.preventDefault();
      if (searchBox) searchBox.focus();
    }
  });

  // Dark mode toggle
  const darkToggle = document.getElementById('darkToggle');
  if (darkToggle) {
    darkToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark');
    });
  }

  // Sidebar part-group collapsibles
  document.querySelectorAll('.sidebar .part-title').forEach(pt => {
    pt.addEventListener('click', () => {
      const group = pt.parentElement;
      const ul = group.querySelector('ul');
      if (ul) ul.style.display = ul.style.display === 'none' ? '' : 'none';
    });
  });
`;

// ---------- Assembly ----------
console.log('Building Professional APEX...\n');

// Part metadata
const parts = {
  1: { title: 'Introducing APEX', intro: 'APEX is not a product you can install. It is a contract between data and decisions — and a discipline for operating agentic intelligence at enterprise scale. This Part introduces what APEX is, the forces that make it necessary, and why Microsoft Fabric is the substrate of choice.' },
  2: { title: 'The APEX Framework', intro: 'Before writing any code, a developer on APEX must internalise the framework: the four-layer manifest model, the canonical schemas, the MCP server taxonomy, the Medallion architecture, and the HITL gate discipline. This Part is the conceptual foundation every chapter after it assumes.' },
  3: { title: 'Building on APEX', intro: 'This is the hands-on core of the book. Seven chapters take you through every layer of APEX implementation: Fabric workspace topology, Medallion and SOR integration, MCP server authoring in Python and C#, agent and orchestration authoring, observability, security, and testing. Code samples throughout. Try It Out boxes offer hands-on scenarios.' },
  4: { title: 'APEX in the Enterprise', intro: 'APEX ships today as seven industry Practices — Retail & Consumer, Healthcare & Life Sciences, Energy & Resources, Industrial & Manufacturing, Technology/Media/Telecom, Travel & Hospitality, and Industrial & Commercial Equipment. Each chapter of this Part goes deep on one Practice: its services, personas, KPIs, and implementation patterns.' },
  5: { title: 'Delivery & Operations', intro: 'A platform without a delivery discipline fails in production. This Part covers the three-wave deployment model, tenant onboarding, resource and governance structures, change management, and the commercial model.' },
  6: { title: 'The Future of APEX', intro: 'APEX\'s four-tier innovation model — Predictive/Causal, Self-Healing, Agentic Contact, Autonomous — is a patterned path, not a pick-list. This Part names flagship solutions with investment envelopes, walks through the Innovation Dependency Chain, and projects the 2026–2028 platform roadmap.' },
};

// Build each Part + chapters
const body = [];
const tocByPart = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] };

for (const ch of chapters) {
  tocByPart[ch.part].push({ num: ch.num, title: ch.title });
}

for (let pnum = 1; pnum <= 6; pnum++) {
  const p = parts[pnum];
  body.push(partOpener(pnum, p.title, p.intro, tocByPart[pnum]));
  const chList = chapters.filter(c => c.part === pnum);
  for (const ch of chList) {
    console.log(`  Chapter ${ch.num}: ${ch.title}`);
    let mdBody;
    try {
      mdBody = ch.body();
    } catch (err) {
      mdBody = `_Content extraction failed: ${err.message}_`;
    }
    const htmlBody = mdToHtml(mdBody, { partNum: pnum, chapterNum: ch.num, skipFirstH1: true });
    body.push(chapterWrapper(ch.num, ch.title, ch.objectives, htmlBody, ch.summary, ch.exercises));
  }
}

// Appendices
for (const app of appendices) {
  console.log(`  Appendix ${app.letter}: ${app.title}`);
  let mdBody;
  try { mdBody = app.body(); } catch (err) { mdBody = `_Content extraction failed: ${err.message}_`; }
  const htmlBody = mdToHtml(mdBody, { partNum: null, chapterNum: null, skipFirstH1: true });
  body.push(appendixWrapper(app.letter, app.title, htmlBody));
}

// Appendix J — generated
console.log('  Appendix J: Exercise Solutions');
const solBody = mdToHtml(generateExerciseSolutionsBody(), { skipFirstH1: true });
body.push(appendixWrapper('J', 'Exercise Solutions', solBody));

// Build sidebar TOC
function buildSidebarHtml() {
  const out = [];
  out.push('<nav class="sidebar">');
  out.push('<h3>Table of Contents</h3>');
  out.push(`<div style="margin-bottom:12px;"><a href="#cover">Cover &amp; Front Matter</a></div>`);
  for (let pnum = 1; pnum <= 6; pnum++) {
    out.push('<div class="part-group">');
    out.push(`<div class="part-title"><a href="#part-${pnum}" style="color:inherit">Part ${toRoman(pnum)}: ${escapeHtml(parts[pnum].title)}</a></div>`);
    out.push('<ul>');
    for (const ch of chapters.filter(c => c.part === pnum)) {
      out.push(`<li><a href="#ch-${ch.num}">Chapter ${ch.num}. ${escapeHtml(ch.title)}</a></li>`);
    }
    out.push('</ul></div>');
  }
  out.push('<h3>Appendices</h3><ul>');
  for (const app of appendices) {
    out.push(`<li><a href="#appendix-${app.letter.toLowerCase()}">Appendix ${app.letter}. ${escapeHtml(app.title)}</a></li>`);
  }
  out.push(`<li><a href="#appendix-j">Appendix J. Exercise Solutions</a></li>`);
  out.push('</ul>');
  out.push('</nav>');
  return out.join('\n');
}

// Build front matter
const FRONT_MATTER = `
<section class="cover" id="cover">
  <div class="brand">Professional</div>
  <h1 class="title"><span class="accent">APEX</span></h1>
  <div class="subtitle">Agentic Platforms on Microsoft Fabric</div>
  <p class="tagline">A comprehensive guide to the APEX framework — from first principles through enterprise delivery, written for architects and developers building the next generation of agentic enterprise platforms.</p>
  <div class="wrox-label">WROX-STYLE EDITION</div>
  <div class="byline">
    by the APEX Core team · Deloitte Microsoft Technology &amp; Services Practice<br>
    April 2026 · Version 1.0
  </div>
</section>

<section class="front-toc" id="front-matter">
  <h1>About This Book</h1>
  <p><em>Professional APEX</em> is a Wrox-style technical book combining the APEX Developer Implementation Guide and the APEX Comprehensive Solutions Reference into a single volume. It is aimed at technical-forward readers — architects, senior developers, and delivery leads — who are building or operating APEX on a client's Microsoft Fabric tenant.</p>

  <p>The book is organised in six Parts, followed by ten appendices and an alphabetised index.</p>

  <ul>
    <li><strong>Part I · Introducing APEX</strong> — what APEX is, the forces that drive it, and why Microsoft Fabric.</li>
    <li><strong>Part II · The APEX Framework</strong> — the four-layer manifest model, canonical schemas, MCP, HITL gates.</li>
    <li><strong>Part III · Building on APEX</strong> — the hands-on developer core; code in Python and C#.</li>
    <li><strong>Part IV · APEX in the Enterprise</strong> — a chapter per industry Practice; real scenarios, real SORs.</li>
    <li><strong>Part V · Delivery &amp; Operations</strong> — three-wave deployment, governance, change management, commercial.</li>
    <li><strong>Part VI · The Future of APEX</strong> — tier model, flagship solutions, dependency chain, roadmap.</li>
  </ul>

  <p>Each chapter opens with a "What You'll Learn in This Chapter" panel, includes Notes, Warnings, Best Practices, and "Try It Out" hands-on boxes throughout, and closes with a Summary and Exercises. Exercise solutions are in Appendix J.</p>

  <aside class="callout note">
    <div class="callout-label">Note</div>
    <p>This book is a Wrox-style edition authored internally by the APEX Core team. It is not an official Wrox Press title. The Wrox conventions are used because they are the clearest available pattern for teaching a technical platform at this scope.</p>
  </aside>

  <p>All code samples compile against the APEX Core v1.2 edition. Downstream releases may shift API surfaces slightly; check <code>apex-core/CHANGELOG.md</code> for current state.</p>
</section>
`;

// Final HTML
const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Professional APEX — Agentic Platforms on Microsoft Fabric</title>
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Aptos:wght@400;600;700&family=Cascadia+Mono&display=swap" rel="stylesheet">
  <style>${CSS}</style>
</head>
<body>
  <header class="topbar">
    <a href="#cover" class="book-brand">Professional <span class="accent">APEX</span></a>
    <div class="current-chapter" id="current-chapter">Agentic Platforms on Microsoft Fabric</div>
    <input type="search" id="searchBox" class="search-box" placeholder="Search TOC (press /)">
    <button id="darkToggle" title="Toggle dark mode">◐</button>
  </header>
  <div class="layout">
    ${buildSidebarHtml()}
    <main>
      ${FRONT_MATTER}
      ${body.join('\n\n')}
    </main>
  </div>
  <script>${JS}</script>
</body>
</html>`;

// ---------- Write ----------
fs.writeFileSync(OUTPUT_HTML, html);
const kb = Math.round(html.length / 1024);
console.log(`\n  ✓ ${path.relative(ROOT, OUTPUT_HTML)}`);
console.log(`    ${kb} KB  ·  ${chapters.length} chapters  ·  ${appendices.length + 1} appendices  ·  ${tocEntries.length} TOC entries`);
console.log(`\nOpen in your browser to read.`);
