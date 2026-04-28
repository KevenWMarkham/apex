// build-kroger-services.cjs
//
// Builds Professional Kroger Services as a single-file Wrox-style HTML book.
// Wraps the 17 Kroger deliverables into a 5-part engagement-arc narrative.
// Sits in the Kroger deliverables folder so relative artifact links resolve
// without path rewriting.
//
// Output: <deliverables>/Professional-Kroger-Services.html (absolute path below)
// Run:    node build-kroger-services.cjs

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const os = require('os');

const ROOT = __dirname;
const OUTPUT_HTML = 'C:/Stage/Clients/Industries/Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/Professional-Kroger-Services.html';
const MERMAID_CACHE = path.join(ROOT, '.cache', 'mermaid');
const MMDC_JS = path.join(ROOT, 'node_modules', '@mermaid-js', 'mermaid-cli', 'src', 'cli.js');
fs.mkdirSync(path.dirname(OUTPUT_HTML), { recursive: true });
fs.mkdirSync(MERMAID_CACHE, { recursive: true });

// ---------- Shared utilities (mirroring build-professional-apex.cjs) ----------
function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function slugify(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').slice(0, 60);
}
function toRoman(n) {
  const m = ['','I','II','III','IV','V','VI','VII','VIII','IX','X'];
  return m[n] || String(n);
}
function renderMermaidToPng(source) {
  const hash = crypto.createHash('sha256').update(source).digest('hex').slice(0, 16);
  const cachePath = path.join(MERMAID_CACHE, `${hash}.png`);
  if (fs.existsSync(cachePath)) return fs.readFileSync(cachePath);
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sg-mmd-'));
  const mmdPath = path.join(tmpDir, 'd.mmd');
  const cfgPath = path.join(tmpDir, 'cfg.json');
  fs.writeFileSync(mmdPath, source, 'utf8');
  fs.writeFileSync(cfgPath, JSON.stringify({
    theme: 'default',
    themeVariables: { fontFamily: 'Aptos, Segoe UI, Arial, sans-serif', fontSize: '14px' },
    flowchart: { useMaxWidth: false, htmlLabels: true }
  }));
  try {
    execFileSync(process.execPath, [MMDC_JS,
      '-i', mmdPath, '-o', cachePath, '-c', cfgPath,
      '-b', 'white', '-w', '1400', '-H', '900', '--scale', '2'
    ], { stdio: ['ignore', 'ignore', 'pipe'] });
  } catch (err) {
    console.warn(`  ! mermaid render failed: ${err.message.split('\n')[0]}`);
    return null;
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
  }
  return fs.existsSync(cachePath) ? fs.readFileSync(cachePath) : null;
}

function parseInline(text) {
  let out = escapeHtml(text);
  out = out.replace(/`([^`]+)`/g, (_, code) =>
    `<code class="inline-code">${code.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')}</code>`);
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, t, u) =>
    `<a class="xref" href="${escapeHtml(u)}">${escapeHtml(t)}</a>`);
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>');
  return out;
}
function splitTableRow(line) {
  return line.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|').map(c => c.trim());
}
function mdToHtml(md) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
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
          out.push(`<figure class="diagram"><img alt="Diagram" src="data:image/png;base64,${png.toString('base64')}"></figure>`);
        } else {
          out.push(`<pre class="diagram-fallback"><code>${escapeHtml(source)}</code></pre>`);
        }
      } else {
        out.push(`<div class="code-block"><div class="code-lang">${escapeHtml(lang || 'text').toUpperCase()}</div><pre><code>${body.map(escapeHtml).join('\n')}</code></pre></div>`);
      }
      continue;
    }
    const hMatch = line.match(/^(#{1,6})\s+(.+)$/);
    if (hMatch) {
      const level = hMatch[1].length;
      const rawText = hMatch[2].replace(/`/g, '').replace(/\*\*/g, '').replace(/\*/g, '');
      const anchor = slugify(rawText);
      out.push(`<h${level} id="${anchor}">${parseInline(rawText)}</h${level}>`);
      i++; continue;
    }
    if (/^---+\s*$/.test(line)) { out.push('<hr class="section-rule">'); i++; continue; }
    if (line.includes('|') && i + 1 < lines.length && /^\s*\|?[\s|:-]+\|?\s*$/.test(lines[i + 1])) {
      const headerCells = splitTableRow(line);
      i += 2;
      const body = [];
      while (i < lines.length && lines[i].trim() !== '' && lines[i].includes('|')) {
        body.push(splitTableRow(lines[i])); i++;
      }
      const thead = '<thead><tr>' + headerCells.map(c => `<th>${parseInline(c)}</th>`).join('') + '</tr></thead>';
      const tbody = '<tbody>' + body.map(row =>
        '<tr>' + row.map(c => `<td>${parseInline(c)}</td>`).join('') + '</tr>').join('') + '</tbody>';
      out.push(`<div class="table-wrap"><table class="md-table">${thead}${tbody}</table></div>`);
      continue;
    }
    if (/^>\s?/.test(line)) {
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^>\s?/, ''));
        i++;
      }
      const bqText = buf.join('\n');
      let cls = 'note', label = 'Note';
      const firstLine = buf[0] || '';
      if (/^\*\*Note/i.test(firstLine))              { cls = 'note'; label = 'Note'; }
      else if (/^\*\*Warning/i.test(firstLine))       { cls = 'warning'; label = 'Warning'; }
      else if (/^\*\*Best Practice/i.test(firstLine)) { cls = 'bestpractice'; label = 'Best Practice'; }
      else if (/^\*\*Try It Out/i.test(firstLine))    { cls = 'tryitout'; label = 'Try It Out'; }
      else if (/^\*\*Key Play/i.test(firstLine))      { cls = 'keyplay'; label = 'Key Play'; }
      else if (/^\*\*Objection/i.test(firstLine))     { cls = 'objection'; label = 'Objection'; }
      else if (/^\*\*Independence/i.test(firstLine))  { cls = 'independence'; label = 'Independence Reminder'; }
      else if (/^\*\*Companion/i.test(firstLine))     { cls = 'companion'; label = 'Companion Artifacts'; }
      const cleaned = bqText.replace(/^\*\*(Note|Warning|Best Practice|Try It Out|Key Play|Objection|Independence|Companion Artifacts|Companion)\*\*[.\s:—-]*/i, '');
      out.push(`<aside class="callout ${cls}"><div class="callout-label">${label}</div>${mdToHtml(cleaned)}</aside>`);
      continue;
    }
    if (/^\s*[-*]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*]\s+/, '')); i++;
      }
      out.push('<ul>' + items.map(it => `<li>${parseInline(it)}</li>`).join('') + '</ul>');
      continue;
    }
    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*\d+\.\s+/, '')); i++;
      }
      out.push('<ol>' + items.map(it => `<li>${parseInline(it)}</li>`).join('') + '</ol>');
      continue;
    }
    if (line.trim() === '') { i++; continue; }
    const buf = [line]; i++;
    while (i < lines.length && lines[i].trim() !== ''
      && !/^(#{1,6})\s/.test(lines[i])
      && !/^```/.test(lines[i]) && !/^~~~/.test(lines[i])
      && !/^>/.test(lines[i])
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

// ---------- Content ----------
// Chapters are defined as objects with: num, part, title, objectives[], body (md string), summary[], exercises[]

const chapters = require('./kroger-services-content.cjs');

// ---------- Wrappers ----------
function chapterObjectives(topics) {
  return `<aside class="chapter-objectives">
    <div class="objectives-label">What This Chapter Does for You</div>
    <ul>${topics.map(t => `<li>${escapeHtml(t)}</li>`).join('')}</ul>
  </aside>`;
}
function chapterSummary(items) {
  return `<section class="chapter-summary">
    <h2>Key Takeaways</h2>
    <ul>${items.map(b => `<li>${escapeHtml(b)}</li>`).join('')}</ul>
  </section>`;
}
function chapterActions(items) {
  return `<section class="chapter-exercises">
    <h2>Seller Actions</h2>
    <ol>${items.map(b => `<li>${escapeHtml(b)}</li>`).join('')}</ol>
  </section>`;
}
function chapterWrapper(num, title, objectives, bodyHtml, summary, actions) {
  return `<article class="chapter" id="ch-${num}">
    <header class="chapter-header">
      <div class="chapter-number">Chapter ${num}</div>
      <h1 class="chapter-title">${escapeHtml(title)}</h1>
    </header>
    ${chapterObjectives(objectives)}
    <div class="chapter-body">${bodyHtml}</div>
    ${chapterSummary(summary)}
    ${chapterActions(actions)}
  </article>`;
}
function partOpener(partNum, partTitle, partIntro, chapterList) {
  const chList = chapterList.map(c =>
    `<li><span class="ch-num">Chapter ${c.num}</span><a href="#ch-${c.num}">${escapeHtml(c.title)}</a></li>`).join('');
  return `<section class="part-opener" id="part-${partNum}">
    <div class="part-label">Part ${toRoman(partNum)}</div>
    <h1 class="part-title">${escapeHtml(partTitle)}</h1>
    <p class="part-intro">${escapeHtml(partIntro)}</p>
    <nav class="part-chapters"><h2>In This Part</h2><ul>${chList}</ul></nav>
  </section>`;
}
function appendixWrapper(letter, title, bodyHtml) {
  return `<article class="appendix" id="appendix-${letter.toLowerCase()}">
    <header class="appendix-header">
      <div class="appendix-label">Appendix ${letter}</div>
      <h1 class="appendix-title">${escapeHtml(title)}</h1>
    </header>
    <div class="appendix-body">${bodyHtml}</div>
  </article>`;
}

// ---------- CSS (gold-on-navy sellers palette) ----------
const CSS = `
  :root {
    --gold: #C89D3A;
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
    --keyplay-purple: #8B5CF6;
  }
  body.dark {
    --bg: #0F172A; --text: #E5E7EB; --code-bg: #1E293B;
    --border: #334155; --sidebar-bg: #0B1220; --dim: #94A3B8;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: "Source Serif 4", Charter, Georgia, "Times New Roman", serif;
    background: var(--bg); color: var(--text);
    line-height: 1.65; font-size: 17px;
  }
  .layout { display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }
  .topbar {
    grid-column: 1 / -1; position: sticky; top: 0; z-index: 100;
    background: var(--navy); color: #fff;
    padding: 12px 24px; display: flex; align-items: center; gap: 16px;
    border-bottom: 2px solid var(--gold);
  }
  .topbar .book-brand {
    font-family: Aptos, "Segoe UI", sans-serif;
    font-weight: 700; font-size: 16px; color: #fff; text-decoration: none;
  }
  .topbar .book-brand .accent { color: var(--gold); }
  .topbar .current-chapter {
    flex: 1; color: #94A3B8; font-size: 14px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .topbar .search-box {
    padding: 6px 10px;
    background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
    color: #fff; border-radius: 6px; font-size: 13px; min-width: 200px;
  }
  .topbar .search-box::placeholder { color: #94A3B8; }
  .topbar button {
    background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.3);
    padding: 6px 10px; border-radius: 6px; font-size: 13px; cursor: pointer;
  }
  .sidebar {
    background: var(--sidebar-bg); border-right: 1px solid var(--border);
    padding: 20px 16px; overflow-y: auto;
    max-height: calc(100vh - 56px); position: sticky; top: 56px;
    font-family: Aptos, "Segoe UI", sans-serif; font-size: 14px;
  }
  .sidebar h3 {
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--dim); margin: 16px 0 6px;
  }
  .sidebar .part-title {
    font-weight: 700; color: var(--gold); font-size: 13px;
    margin: 12px 0 4px; cursor: pointer; user-select: none;
  }
  .sidebar ul { list-style: none; padding: 0; margin: 0; }
  .sidebar li { margin: 2px 0; }
  .sidebar a { color: var(--text); text-decoration: none; display: block; padding: 4px 8px; border-radius: 4px; font-size: 13px; }
  .sidebar a:hover { background: var(--border); }
  .sidebar a.current { background: var(--gold); color: var(--navy); font-weight: 700; }
  main { padding: 40px 60px; max-width: 920px; }

  .cover {
    padding: 80px 60px; text-align: center;
    margin: -40px -60px 40px;
    background: linear-gradient(135deg, var(--navy) 0%, #0B111E 100%);
    color: #fff; border-bottom: 3px solid var(--gold);
  }
  .cover .brand {
    font-family: Aptos, sans-serif;
    font-size: 18px; letter-spacing: 0.4em; color: var(--gold);
    text-transform: uppercase; font-weight: 700;
  }
  .cover .title {
    font-family: Aptos, sans-serif;
    font-size: 52px; line-height: 1.1; margin: 16px 0 8px; font-weight: 700;
  }
  .cover .title .accent { color: var(--gold); }
  .cover .subtitle {
    font-family: Aptos, sans-serif;
    font-size: 26px; color: var(--apex-teal); margin: 8px 0 16px;
  }
  .cover .edition {
    font-family: Aptos, sans-serif; font-size: 18px; color: var(--gold);
    font-style: italic;
    margin: 4px 0 24px;
  }
  .cover .tagline { font-size: 16px; color: #E5E7EB; max-width: 620px; margin: 0 auto 32px; }
  .cover .byline { font-size: 14px; color: #94A3B8; margin-top: 40px; }
  .cover .wrox-label {
    display: inline-block;
    background: var(--gold); color: var(--navy); padding: 8px 20px;
    font-family: Aptos, sans-serif; font-weight: 700;
    letter-spacing: 0.1em; font-size: 14px; margin-top: 24px;
  }

  .part-opener {
    page-break-before: always; padding: 80px 0;
    border-top: 4px solid var(--gold);
    border-bottom: 1px solid var(--border);
    margin: 60px 0 40px;
  }
  .part-opener .part-label {
    font-family: Aptos, sans-serif; font-size: 14px; letter-spacing: 0.3em;
    color: var(--gold); text-transform: uppercase; font-weight: 700;
  }
  .part-opener .part-title {
    font-family: Aptos, sans-serif; font-size: 48px; margin: 12px 0 20px;
    color: var(--navy); border: none; padding: 0;
  }
  .part-opener .part-intro {
    font-size: 18px; line-height: 1.6; max-width: 700px; font-style: italic;
  }
  .part-opener .part-chapters {
    margin-top: 32px; background: var(--code-bg); padding: 24px;
    border-left: 4px solid var(--gold);
  }
  .part-opener .part-chapters h2 {
    font-family: Aptos, sans-serif; font-size: 14px;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: var(--dim); margin: 0 0 12px; border: none; padding: 0;
  }
  .part-opener .part-chapters ul { list-style: none; padding: 0; font-family: Aptos, sans-serif; font-size: 15px; }
  .part-opener .part-chapters li { padding: 6px 0; border-bottom: 1px dotted var(--border); }
  .part-opener .part-chapters .ch-num {
    display: inline-block; width: 100px; color: var(--gold); font-weight: 600;
  }
  .part-opener .part-chapters a { color: var(--text); text-decoration: none; }
  .part-opener .part-chapters a:hover { color: var(--gold); }

  .chapter { page-break-before: always; }
  .chapter-header {
    border-bottom: 3px solid var(--gold);
    padding-bottom: 16px; margin-bottom: 24px;
  }
  .chapter-number {
    font-family: Aptos, sans-serif; font-size: 14px; letter-spacing: 0.2em;
    color: var(--gold); text-transform: uppercase; font-weight: 700;
  }
  .chapter-title {
    font-family: Aptos, sans-serif; font-size: 38px; margin: 8px 0 0;
    color: var(--navy); line-height: 1.15;
  }
  .chapter-objectives {
    background: var(--code-bg); border-left: 4px solid var(--gold);
    padding: 20px 24px; margin: 0 0 32px; font-family: Aptos, sans-serif;
  }
  .objectives-label {
    font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase;
    color: var(--gold); font-weight: 700; margin-bottom: 8px;
  }
  .chapter-objectives ul { margin: 0; padding-left: 20px; font-size: 15px; }

  h1, h2, h3, h4 { font-family: Aptos, sans-serif; color: var(--navy); }
  h1 { font-size: 32px; border-bottom: 2px solid var(--border); padding-bottom: 8px; margin-top: 40px; }
  h2 { font-size: 24px; margin-top: 32px; }
  h3 { font-size: 19px; margin-top: 24px; }
  h4 { font-size: 16px; margin-top: 18px; }
  p { margin: 0 0 14px; }

  .code-block {
    background: var(--code-bg); border: 1px solid var(--border);
    border-left: 4px solid var(--apex-teal);
    margin: 16px 0; border-radius: 4px; overflow-x: auto;
  }
  .code-lang {
    font-family: "Cascadia Mono", Consolas, monospace; font-size: 11px;
    letter-spacing: 0.1em; color: var(--dim);
    padding: 4px 12px; border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.03); font-weight: 600;
  }
  .code-block pre { margin: 0; padding: 12px 16px; }
  .code-block code { font-family: "Cascadia Mono", Consolas, monospace; font-size: 13px; line-height: 1.5; }
  .inline-code { font-family: "Cascadia Mono", Consolas, monospace; background: var(--code-bg); padding: 1px 6px; border-radius: 3px; font-size: 0.9em; color: var(--navy); }

  .callout {
    margin: 16px 0; padding: 12px 16px;
    border-left: 4px solid; background: var(--code-bg);
    border-radius: 4px; font-size: 15px;
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
  .callout.tryitout, .callout.keyplay { border-color: var(--keyplay-purple); background: rgba(139, 92, 246, 0.05); }
  .callout.tryitout .callout-label, .callout.keyplay .callout-label { color: var(--keyplay-purple); }
  .callout.objection { border-color: var(--wrox-red); background: rgba(184, 35, 47, 0.04); }
  .callout.objection .callout-label { color: var(--wrox-red); }
  .callout.independence { border-color: var(--gold); background: rgba(200, 157, 58, 0.08); }
  .callout.independence .callout-label { color: var(--gold); }
  .callout.companion {
    border-color: var(--gold);
    background: linear-gradient(to right, rgba(200,157,58,0.08), transparent 60%);
  }
  .callout.companion .callout-label { color: var(--gold); }
  .callout.companion ul { margin: 6px 0 0 0; padding-left: 22px; }
  .callout.companion li { margin: 3px 0; font-size: 14px; }
  .callout.companion a { color: var(--navy); text-decoration: underline; text-decoration-color: var(--gold); }
  .callout.companion a:hover { color: var(--gold); }
  .callout p:last-child { margin-bottom: 0; }

  .table-wrap { overflow-x: auto; margin: 16px 0; }
  .md-table { width: 100%; border-collapse: collapse; font-size: 14px; }
  .md-table th {
    background: var(--navy); color: #fff; padding: 8px 12px; text-align: left;
    font-family: Aptos, sans-serif; font-weight: 600; font-size: 13px;
  }
  .md-table td { padding: 8px 12px; border: 1px solid var(--border); }
  .md-table tr:nth-child(even) td { background: var(--code-bg); }

  .chapter-summary, .chapter-exercises {
    margin-top: 48px; padding: 20px 24px;
    background: var(--code-bg); border-left: 4px solid var(--navy);
    border-radius: 4px;
  }
  .chapter-summary h2, .chapter-exercises h2 {
    margin-top: 0; border: none; padding: 0; color: var(--navy);
  }

  .diagram { margin: 20px 0; text-align: center; }
  .diagram img { max-width: 100%; height: auto; border: 1px solid var(--border); border-radius: 4px; }

  .appendix { page-break-before: always; }
  .appendix-header {
    border-bottom: 3px solid var(--navy);
    padding-bottom: 16px; margin-bottom: 24px;
  }
  .appendix-label {
    font-family: Aptos, sans-serif; font-size: 14px; letter-spacing: 0.2em;
    color: var(--navy); text-transform: uppercase; font-weight: 700;
  }
  .appendix-title {
    font-family: Aptos, sans-serif; font-size: 32px; margin: 8px 0 0;
    color: var(--navy); line-height: 1.2;
  }

  hr.section-rule { border: none; border-bottom: 1px solid var(--border); margin: 24px 0; }
  a { color: var(--gold); }
  a.xref { color: var(--gold); font-weight: 600; }

  @media print {
    .topbar, .sidebar { display: none; }
    .layout { grid-template-columns: 1fr; }
    main { padding: 0; max-width: none; }
    .chapter, .part-opener, .appendix { page-break-before: always; }
  }
`;

const JS = `
  const sidebar = document.querySelector('.sidebar');
  const currentChapterEl = document.getElementById('current-chapter');
  const links = sidebar.querySelectorAll('a');
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
  const searchBox = document.getElementById('searchBox');
  if (searchBox) {
    searchBox.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) { links.forEach(l => l.style.display = ''); return; }
      links.forEach(l => {
        const txt = l.textContent.toLowerCase();
        l.style.display = txt.includes(q) ? '' : 'none';
      });
    });
  }
  document.addEventListener('keydown', (e) => {
    if (document.activeElement && document.activeElement.tagName === 'INPUT') return;
    const allLinks = Array.from(sidebar.querySelectorAll('a[href^="#ch-"], a[href^="#appendix-"]'));
    const current = sidebar.querySelector('a.current');
    const idx = current ? allLinks.indexOf(current) : -1;
    if (e.key === 'j' && idx < allLinks.length - 1) allLinks[idx + 1].click();
    else if (e.key === 'k' && idx > 0) allLinks[idx - 1].click();
    else if (e.key === 'g') window.scrollTo({ top: 0, behavior: 'smooth' });
    else if (e.key === '/') { e.preventDefault(); if (searchBox) searchBox.focus(); }
  });
  const darkToggle = document.getElementById('darkToggle');
  if (darkToggle) darkToggle.addEventListener('click', () => document.body.classList.toggle('dark'));
  document.querySelectorAll('.sidebar .part-title').forEach(pt => {
    pt.addEventListener('click', () => {
      const group = pt.parentElement;
      const ul = group.querySelector('ul');
      if (ul) ul.style.display = ul.style.display === 'none' ? '' : 'none';
    });
  });
`;

// ---------- Part metadata ----------
const parts = {
  1: { title: 'Why Kroger, Why APEX', intro: 'The strategic context for the Kroger pursuit, where margin moves in modern grocery, and how APEX wedges into the Kroger estate alongside 84.51°, Ocado, and Boost.' },
  2: { title: 'The Service Portfolio', intro: 'The two anchor services (RC-E2E-03 Assortment & Pricing and RC-E2E-09 Product Tracking), the high-attach catalog, and how Kroger differentiates from Albertsons, Publix, HEB, and Ahold.' },
  3: { title: 'The Architecture', intro: 'System of record, the Fabric plane, the Foundry agent plane, the MCP layer, and Purview governance — the five technology planes Deloitte assembles for Kroger.' },
  4: { title: 'The Pursuit', intro: 'Executive engagement, the pitch, risk and stakeholder management, the demo, and the client-presentable Kroger Store 412 day-in-the-shift narrative.' },
  5: { title: 'At Scale', intro: 'Operations and test strategy, the multi-wave service roadmap, cross-grocer expansion, and the closing seller compact.' },
};

// ---------- Build ----------
console.log('Building Professional Kroger Services...\n');

const tocByPart = {};
for (const ch of chapters.all) {
  if (!tocByPart[ch.part]) tocByPart[ch.part] = [];
  tocByPart[ch.part].push({ num: ch.num, title: ch.title });
}
for (const pnum of Object.keys(tocByPart)) {
  tocByPart[pnum].sort((a, b) => a.num - b.num);
}

const body = [];
for (let pnum = 1; pnum <= 5; pnum++) {
  const p = parts[pnum];
  body.push(partOpener(pnum, p.title, p.intro, tocByPart[pnum] || []));
  const chList = chapters.all.filter(c => c.part === pnum).sort((a, b) => a.num - b.num);
  for (const ch of chList) {
    console.log(`  Chapter ${ch.num}: ${ch.title}`);
    body.push(chapterWrapper(ch.num, ch.title, ch.objectives, mdToHtml(ch.body), ch.summary, ch.actions));
  }
}
const sortedAppendices = [...chapters.appendices].sort((a, b) => a.letter.localeCompare(b.letter));
for (const app of sortedAppendices) {
  console.log(`  Appendix ${app.letter}: ${app.title}`);
  body.push(appendixWrapper(app.letter, app.title, mdToHtml(app.body)));
}

function buildSidebarHtml() {
  const out = [];
  out.push('<nav class="sidebar">');
  out.push('<h3>Table of Contents</h3>');
  out.push(`<div style="margin-bottom:12px;"><a href="#cover">Cover &amp; Front Matter</a></div>`);
  for (let pnum = 1; pnum <= 5; pnum++) {
    const p = parts[pnum];
    out.push('<div class="part-group">');
    out.push(`<div class="part-title"><a href="#part-${pnum}" style="color:inherit">Part ${toRoman(pnum)}: ${escapeHtml(p.title)}</a></div>`);
    out.push('<ul>');
    const chList = chapters.all.filter(c => c.part === pnum).sort((a, b) => a.num - b.num);
    for (const ch of chList) {
      out.push(`<li><a href="#ch-${ch.num}">Chapter ${ch.num}. ${escapeHtml(ch.title)}</a></li>`);
    }
    out.push('</ul></div>');
  }
  out.push('<h3>Appendices</h3><ul>');
  const sidebarAppendices = [...chapters.appendices].sort((a, b) => a.letter.localeCompare(b.letter));
  for (const app of sidebarAppendices) {
    out.push(`<li><a href="#appendix-${app.letter.toLowerCase()}">Appendix ${app.letter}. ${escapeHtml(app.title)}</a></li>`);
  }
  out.push('</ul></nav>');
  return out.join('\n');
}

const FRONT_MATTER = `
<section class="cover" id="cover">
  <div class="brand">Professional</div>
  <h1 class="title"><span class="accent">Kroger</span> Services</h1>
  <div class="subtitle">The Anchor-Account Companion to APEX RC-E2E-03 + RC-E2E-09</div>
  <div class="edition">FY27 Pipeline · Assortment, Pricing & Product Tracking at The Kroger Co.</div>
  <p class="tagline">A field guide for Deloitte sellers and delivery leads pursuing the Kroger agentic-AI program. Wraps the seventeen pursuit deliverables into one read — strategy, services, architecture, pursuit motion, and at-scale playbook.</p>
  <div class="wrox-label">WROX-STYLE EDITION · KROGER VOLUME</div>
  <div class="byline">
    by the APEX RC team · Deloitte Microsoft Technology &amp; Services Practice<br>
    April 2026 · Version 1.0 · CONFIDENTIAL — internal use only
  </div>
</section>
<section class="front-toc" id="front-matter">
  <h1>How to Use This Book</h1>
  <p><em>Professional Kroger Services</em> is the read-front-to-back companion to the seventeen artifacts that make up the FY27 Kroger pursuit deliverables set. It is not a replacement for those artifacts — it is the narrative that ties them together. A seller can read it cold to get smart on the pursuit; a delivery lead can use it to brief a new team member; a GPL can hand it to an account partner walking into a meeting.</p>
  <p>The book is organised around five questions:</p>
  <ul>
    <li><strong>"Why Kroger, why now, and why does APEX fit?"</strong> → Part I.</li>
    <li><strong>"What are we actually selling?"</strong> → Part II.</li>
    <li><strong>"How does it get built?"</strong> → Part III.</li>
    <li><strong>"How do we close it?"</strong> → Part IV. Chapter 18 (Kroger Store 412) is client-presentable as-is.</li>
    <li><strong>"How do we run it and grow it?"</strong> → Part V.</li>
  </ul>
  <p>Each chapter ends with a <strong>Companion Artifacts</strong> callout listing the underlying deliverable files. Click through whenever you need the full document.</p>
  <aside class="callout independence">
    <div class="callout-label">Independence Reminder</div>
    <p>This book contains publicly-observable strategic signals on The Kroger Co. It does not represent that Deloitte is currently engaged with Kroger, nor does it disclose confidential client information. All account narratives are framed as hypotheses to validate in discovery. The Kroger Store 412 narrative in Chapter 18 is illustrative — it is not a description of any actual Kroger store deployment.</p>
  </aside>
</section>
`;

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Professional Kroger Services</title>
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Aptos:wght@400;600;700&family=Cascadia+Mono&display=swap" rel="stylesheet">
  <style>${CSS}</style>
</head>
<body>
  <header class="topbar">
    <a href="#cover" class="book-brand">Professional <span class="accent">Kroger</span> Services</a>
    <div class="current-chapter" id="current-chapter">FY27 Pipeline · RC-E2E-03 + RC-E2E-09 at The Kroger Co.</div>
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

fs.writeFileSync(OUTPUT_HTML, html);
const kb = Math.round(html.length / 1024);
console.log(`\n  ✓ ${path.relative(ROOT, OUTPUT_HTML)}`);
console.log(`    ${kb} KB  ·  ${chapters.all.length} chapters  ·  ${chapters.appendices.length} appendices`);
