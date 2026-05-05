// Render the APEX Comprehensive Solutions Reference (single markdown source)
// to one .docx using the same Aptos/Cascadia typography and Mermaid-to-PNG
// pipeline as build-dev-guide-docx.cjs.
//
// Input:  docs/reference/APEX-comprehensive-solutions-reference.md
// Output: docs/reference/APEX-comprehensive-solutions-reference.docx
//
// Run:   node build-reference-docx.cjs

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const os = require('os');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, ExternalHyperlink, PageBreak, ImageRun
} = require('docx');

// -------- Config --------
const INPUT_MD   = 'docs/reference/APEX-comprehensive-solutions-reference.md';
const OUTPUT_DOCX = 'docs/reference/APEX-comprehensive-solutions-reference.docx';
const GUIDE_TITLE = 'APEX Comprehensive Solutions Reference';
const GUIDE_SUBTITLE = 'Reinventing Enterprise Decision-Making on Microsoft';

// -------- Styling --------
const NAVY = '1A2339';
const TEAL = '2DD4BF';
const DIM  = '64748B';
const FAINT_BORDER = { style: BorderStyle.SINGLE, size: 4, color: 'B8B8B8' };
const HEADER_SHADING = { fill: NAVY, type: ShadingType.CLEAR, color: 'auto' };
const CELL_MARGINS = { top: 100, bottom: 100, left: 140, right: 140 };
const FONT_BODY = 'Aptos';
const FONT_DISPLAY = 'Aptos Display';
const FONT_CODE = 'Cascadia Mono';

// -------- Mermaid cache --------
const MERMAID_CACHE = path.join(__dirname, '.cache', 'mermaid');
fs.mkdirSync(MERMAID_CACHE, { recursive: true });
const MMDC_JS = path.join(__dirname, 'node_modules', '@mermaid-js', 'mermaid-cli', 'src', 'cli.js');

function renderMermaidToPng(source) {
  const hash = crypto.createHash('sha256').update(source).digest('hex').slice(0, 16);
  const cachePath = path.join(MERMAID_CACHE, `${hash}.png`);
  if (!fs.existsSync(cachePath)) {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'apex-mmd-'));
    const mmdPath = path.join(tmpDir, 'd.mmd');
    const cfgPath = path.join(tmpDir, 'cfg.json');
    fs.writeFileSync(mmdPath, source, 'utf8');
    fs.writeFileSync(cfgPath, JSON.stringify({
      theme: 'default',
      themeVariables: { fontFamily: 'Aptos, Segoe UI, Arial, sans-serif', fontSize: '14px' },
      flowchart: { useMaxWidth: false, htmlLabels: true },
      sequence:  { useMaxWidth: false },
      stateDiagram: { useMaxWidth: false },
    }));
    try {
      execFileSync(process.execPath, [MMDC_JS,
        '-i', mmdPath, '-o', cachePath, '-c', cfgPath,
        '-b', 'white', '-w', '1600', '-H', '1200', '--scale', '2',
      ], { stdio: ['ignore', 'ignore', 'pipe'] });
    } catch (err) {
      const stderr = err.stderr ? err.stderr.toString().split('\n').slice(0, 3).join(' | ') : err.message.split('\n')[0];
      console.warn(`    ! mermaid render failed for ${hash} (${stderr})`);
      return null;
    } finally {
      try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (_) {}
    }
  }
  if (!fs.existsSync(cachePath)) return null;
  const buf = fs.readFileSync(cachePath);
  return { buffer: buf, widthPx: buf.readUInt32BE(16), heightPx: buf.readUInt32BE(20) };
}

function mermaidParagraph(source) {
  const rendered = renderMermaidToPng(source);
  if (!rendered) return null;
  const pageWidthPx = 640;
  const maxHeightPx = 880;
  let { widthPx, heightPx, buffer } = rendered;
  let displayW = Math.min(widthPx, pageWidthPx);
  let displayH = Math.round((heightPx / widthPx) * displayW);
  if (displayH > maxHeightPx) {
    displayW = Math.round((displayW / displayH) * maxHeightPx);
    displayH = maxHeightPx;
  }
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 160 },
    children: [new ImageRun({ data: buffer, type: 'png',
      transformation: { width: displayW, height: displayH } })],
  });
}

// -------- Inline parser --------
function parseInline(text) {
  const runs = [];
  const re = /(\[[^\]]+\]\([^)]+\))|(`[^`]+`)|(\*\*[^*]+\*\*)|(\*[^*]+\*)/g;
  let last = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) runs.push(new TextRun({ text: text.slice(last, m.index) }));
    const tok = m[0];
    if (tok.startsWith('[')) {
      const lm = tok.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      if (lm) runs.push(new ExternalHyperlink({ link: lm[2],
        children: [new TextRun({ text: lm[1], style: 'Hyperlink', color: '0563C1', underline: {} })] }));
    } else if (tok.startsWith('`')) {
      runs.push(new TextRun({ text: tok.slice(1, -1), font: FONT_CODE, size: 18, color: '2B2B2B' }));
    } else if (tok.startsWith('**')) {
      runs.push(new TextRun({ text: tok.slice(2, -2), bold: true }));
    } else if (tok.startsWith('*')) {
      runs.push(new TextRun({ text: tok.slice(1, -1), italics: true }));
    }
    last = m.index + tok.length;
  }
  if (last < text.length) runs.push(new TextRun({ text: text.slice(last) }));
  if (runs.length === 0) runs.push(new TextRun({ text }));
  return runs;
}

function heading(text, level) {
  const headingLevels = [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3, HeadingLevel.HEADING_4];
  const sizes = [40, 30, 24, 20];
  return new Paragraph({
    heading: headingLevels[Math.min(level - 1, 3)],
    spacing: { before: 340 - (level - 1) * 40, after: 160 - (level - 1) * 20 },
    children: [new TextRun({ text, bold: true,
      font: level <= 2 ? FONT_DISPLAY : FONT_BODY,
      size: sizes[Math.min(level - 1, 3)],
      color: level === 1 ? NAVY : '0B111E' })],
  });
}

function paragraph(text) {
  return new Paragraph({ spacing: { after: 140 }, children: parseInline(text) });
}

function blockquote(text) {
  return new Paragraph({
    spacing: { after: 140 }, indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 20, color: TEAL, space: 12 } },
    children: parseInline(text),
  });
}

function bulletItem(text) {
  return new Paragraph({ bullet: { level: 0 }, spacing: { after: 60 }, children: parseInline(text) });
}

function codeBlock(lines, lang) {
  if (lang === 'mermaid') {
    const source = lines.join('\n');
    const rendered = mermaidParagraph(source);
    if (rendered) return rendered;
  }
  const body = lines.length === 0 ? [''] : lines;
  const para = body.map(l => new Paragraph({
    spacing: { after: 0, line: 240 },
    children: [new TextRun({ text: l.length === 0 ? ' ' : l, font: FONT_CODE, size: 18, color: '1F2937' })],
  }));
  if (lang) para.unshift(new Paragraph({ spacing: { after: 40 },
    children: [new TextRun({ text: lang.toUpperCase(), font: FONT_CODE, size: 14, color: DIM, bold: true })] }));
  const cell = new TableCell({
    margins: CELL_MARGINS,
    shading: { fill: 'F5F5F7', type: ShadingType.CLEAR, color: 'auto' },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: 'D0D0D5' },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D0D0D5' },
      left: { style: BorderStyle.SINGLE, size: 12, color: TEAL },
      right: { style: BorderStyle.SINGLE, size: 4, color: 'D0D0D5' },
    },
    children: para,
  });
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, rows: [new TableRow({ children: [cell] })] });
}

function renderTable(headerCells, bodyRows) {
  const mkCell = (text, isHeader) => new TableCell({
    margins: CELL_MARGINS,
    shading: isHeader ? HEADER_SHADING : undefined,
    borders: { top: FAINT_BORDER, bottom: FAINT_BORDER, left: FAINT_BORDER, right: FAINT_BORDER },
    children: [new Paragraph({
      spacing: { after: 0 },
      children: parseInline(text).map(r => {
        if (r instanceof TextRun && isHeader)
          return new TextRun({ text: r.options?.text || '', bold: true, color: 'FFFFFF', size: 18 });
        return r;
      }),
    })],
  });
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({ tableHeader: true, children: headerCells.map(c => mkCell(c, true)) }),
      ...bodyRows.map(cells => new TableRow({ children: cells.map(c => mkCell(c, false)) })),
    ],
  });
}

function horizontalRule() {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'C0C0C5', space: 1 } },
    children: [new TextRun({ text: '' })],
  });
}

function pageBreak() {
  return new Paragraph({ children: [new TextRun({ children: [new PageBreak()] })] });
}

function splitTableRow(line) {
  return line.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|').map(c => c.trim());
}

// -------- Markdown parser --------
function parseMarkdown(md) {
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
      out.push(codeBlock(body, lang));
      continue;
    }
    const hMatch = line.match(/^(#{1,4})\s+(.+)$/);
    if (hMatch) {
      out.push(heading(hMatch[2].replace(/`/g, '').replace(/\*\*/g, '').replace(/\*/g, ''), hMatch[1].length));
      i++; continue;
    }
    if (/^---+\s*$/.test(line)) { out.push(horizontalRule()); i++; continue; }
    if (line.includes('|') && i + 1 < lines.length && /^\s*\|?[\s|:-]+\|?\s*$/.test(lines[i + 1]) && lines[i + 1].includes('|')) {
      const headerCells = splitTableRow(line);
      i += 2;
      const body = [];
      while (i < lines.length && lines[i].trim() !== '' && lines[i].includes('|')) { body.push(splitTableRow(lines[i])); i++; }
      out.push(renderTable(headerCells, body));
      out.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: '' })] }));
      continue;
    }
    if (/^>\s?/.test(line)) {
      const bq = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) { bq.push(lines[i].replace(/^>\s?/, '')); i++; }
      out.push(blockquote(bq.join(' ')));
      continue;
    }
    if (/^\s*[-*]\s+/.test(line)) {
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        out.push(bulletItem(lines[i].replace(/^\s*[-*]\s+/, '')));
        i++;
      }
      continue;
    }
    if (line.trim() === '') { i++; continue; }
    const buf = [line]; i++;
    while (i < lines.length && lines[i].trim() !== ''
      && !/^(#{1,4})\s/.test(lines[i]) && !/^```/.test(lines[i]) && !/^~~~/.test(lines[i])
      && !/^>/.test(lines[i]) && !/^\s*[-*]\s+/.test(lines[i]) && !/^---+\s*$/.test(lines[i])
      && !lines[i].includes('|')) {
      buf.push(lines[i]); i++;
    }
    out.push(paragraph(buf.join(' ')));
  }
  return out;
}

// -------- Document assembly --------
(async () => {
  console.log('Rendering APEX Comprehensive Solutions Reference to .docx ...\n');
  try {
    const md = fs.readFileSync(path.join(__dirname, INPUT_MD), 'utf8');

    // Cover / title page
    const cover = [
      new Paragraph({ spacing: { before: 2400, after: 60 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: 'APEX', bold: true, font: FONT_DISPLAY, size: 120, color: NAVY })] }),
      new Paragraph({ spacing: { after: 240 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: GUIDE_TITLE, bold: true, font: FONT_DISPLAY, size: 48, color: TEAL })] }),
      new Paragraph({ spacing: { after: 200 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: GUIDE_SUBTITLE, italics: true, font: FONT_DISPLAY, size: 26, color: '1F2937' })] }),
      new Paragraph({ spacing: { after: 3200 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: 'A Comprehensive Solutions Reference for the Intelligent Enterprise',
          font: FONT_BODY, size: 24, color: DIM })] }),
      new Paragraph({ spacing: { after: 80 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: 'April 2026 · Version 1.0 · CONFIDENTIAL', font: FONT_BODY, size: 22, color: '1F2937' })] }),
      new Paragraph({ spacing: { after: 80 }, alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: 'Deloitte Microsoft Technology & Services Practice',
          font: FONT_BODY, size: 22, color: '1F2937' })] }),
      pageBreak(),
    ];

    const body = parseMarkdown(md);
    const elements = [...cover, ...body];

    const doc = new Document({
      creator: 'APEX Core',
      title: GUIDE_TITLE,
      description: 'APEX Comprehensive Solutions Reference',
      styles: {
        default: { document: { run: { font: FONT_BODY, size: 22 } } },
        paragraphStyles: [
          { id: 'Hyperlink', name: 'Hyperlink', basedOn: 'Normal',
            run: { font: FONT_BODY, color: '0563C1', underline: {} } },
        ],
      },
      sections: [{
        properties: { page: { margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
        headers: {
          default: new Header({ children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: GUIDE_TITLE, size: 16, color: DIM, italics: true })],
          })] }),
        },
        footers: {
          default: new Footer({ children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: 'APEX Core v1.2 · Reference v1.0 · Page ', size: 16, color: DIM }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: DIM }),
            ],
          })] }),
        },
        children: elements,
      }],
    });

    const buf = await Packer.toBuffer(doc);
    const outPath = path.join(__dirname, OUTPUT_DOCX);
    let writeErr = null;
    for (let attempt = 0; attempt < 3; attempt++) {
      try { fs.writeFileSync(outPath, buf); writeErr = null; break; }
      catch (err) {
        writeErr = err;
        if (err.code === 'EBUSY' || err.code === 'EPERM') {
          if (attempt === 0) console.warn(`    ! ${path.basename(outPath)} is open in Word. Retrying...`);
          await new Promise(r => setTimeout(r, 1200));
          continue;
        }
        throw err;
      }
    }
    if (writeErr) {
      const fallback = outPath.replace(/\.docx$/, `-${Date.now()}.docx`);
      fs.writeFileSync(fallback, buf);
      console.warn(`    ! Wrote fallback to ${path.basename(fallback)}`);
      console.log(`  ✓ ${path.basename(fallback)} (${Math.round(buf.length/1024)} KB)`);
    } else {
      console.log(`  ✓ ${path.relative(__dirname, outPath)}`);
      console.log(`    ${Math.round(buf.length/1024)} KB  ·  ${elements.length} elements`);
    }
  } catch (err) {
    console.error(`  ✗ failed — ${err.message}`);
    console.error(err.stack);
    process.exitCode = 1;
  }
  console.log('\nDone.');
})();
