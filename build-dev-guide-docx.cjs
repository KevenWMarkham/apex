// Render the APEX Developer Guide markdown sources to a SINGLE combined .docx.
// Concatenates the spine (docs/APEX-developer-guide.md) followed by the 7
// companions (docs/dev-guide/01..07) with a title page and page breaks
// between sections. Output: docs/APEX-developer-implementation-guide.docx
//
// Run:   node build-dev-guide-docx.cjs
//
// Markdown coverage (80% case):
//   - H1..H4 (# ## ### ####)
//   - Paragraphs with inline **bold**, *italic*, `code`, [text](url)
//   - Fenced code blocks ```lang ... ```
//   - Tables (pipe-delimited, with separator row)
//   - Blockquotes (>)
//   - Unordered lists (-, *)
//   - Horizontal rules (---)
//   - Mermaid blocks are rendered as fenced code with a "(Mermaid diagram — see source)" note

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, ExternalHyperlink, PageBreak
} = require('docx');

// ------------------------------------------------------------------
// Config — files to combine, in order
// ------------------------------------------------------------------
const FILES = [
  { md: 'docs/APEX-developer-guide.md',                sectionTitle: 'Part I — Spine' },
  { md: 'docs/dev-guide/01-fabric-layering.md',        sectionTitle: 'Part II — Companion 01: Fabric Layering' },
  { md: 'docs/dev-guide/02-medallion-sor.md',          sectionTitle: 'Part III — Companion 02: Medallion & SOR Integration' },
  { md: 'docs/dev-guide/03-mcp-servers.md',            sectionTitle: 'Part IV — Companion 03: MCP Servers & Tooling' },
  { md: 'docs/dev-guide/04-agent-lifecycle.md',        sectionTitle: 'Part V — Companion 04: Agent & Orchestration Lifecycle + HITL' },
  { md: 'docs/dev-guide/05-observability-security.md', sectionTitle: 'Part VI — Companion 05: Observability & Security' },
  { md: 'docs/dev-guide/06-testing-topology.md',       sectionTitle: 'Part VII — Companion 06: Testing & Environment Topology' },
  { md: 'docs/dev-guide/07-service-catalog.md',        sectionTitle: 'Part VIII — Companion 07: Service Catalog' },
];

const OUTPUT_DOCX = 'docs/APEX-developer-implementation-guide.docx';
const GUIDE_TITLE = 'APEX Developer Implementation Guide';

// ------------------------------------------------------------------
// Styling
// ------------------------------------------------------------------
const NAVY = '1A2339';
const TEAL = '2DD4BF';
const DIM  = '64748B';
const FAINT_BORDER = { style: BorderStyle.SINGLE, size: 4, color: 'B8B8B8' };
const HEADER_SHADING = { fill: NAVY, type: ShadingType.CLEAR, color: 'auto' };
const CELL_MARGINS = { top: 100, bottom: 100, left: 140, right: 140 };

// Font stack — Aptos is Microsoft 365's default as of 2023 (replaces Calibri).
// It renders cleanly, looks modern/humanist like popular Google Fonts (Inter /
// Source Sans / Roboto), and ships with any recent Office install. On older
// Office, Word substitutes to Calibri automatically.
const FONT_BODY = 'Aptos';
const FONT_DISPLAY = 'Aptos Display';     // heavier cut, used for big headings/titles
const FONT_CODE = 'Cascadia Mono';         // modern Microsoft monospace (Windows 11 default)

// ------------------------------------------------------------------
// Inline parser — returns an array of TextRun | ExternalHyperlink
// Handles: **bold**, *italic*, `code`, [text](url)
// ------------------------------------------------------------------
function parseInline(text) {
  const runs = [];
  // Combined regex: hyperlink | code | bold | italic | plain
  const re = /(\[[^\]]+\]\([^)]+\))|(`[^`]+`)|(\*\*[^*]+\*\*)|(\*[^*]+\*)/g;
  let last = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) {
      runs.push(new TextRun({ text: text.slice(last, m.index) }));
    }
    const tok = m[0];
    if (tok.startsWith('[')) {
      const linkMatch = tok.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      if (linkMatch) {
        runs.push(new ExternalHyperlink({
          link: linkMatch[2],
          children: [new TextRun({ text: linkMatch[1], style: 'Hyperlink', color: '0563C1', underline: {} })]
        }));
      }
    } else if (tok.startsWith('`')) {
      runs.push(new TextRun({ text: tok.slice(1, -1), font: FONT_CODE, size: 18, color: '2B2B2B' }));
    } else if (tok.startsWith('**')) {
      runs.push(new TextRun({ text: tok.slice(2, -2), bold: true }));
    } else if (tok.startsWith('*')) {
      runs.push(new TextRun({ text: tok.slice(1, -1), italics: true }));
    }
    last = m.index + tok.length;
  }
  if (last < text.length) {
    runs.push(new TextRun({ text: text.slice(last) }));
  }
  if (runs.length === 0) {
    runs.push(new TextRun({ text }));
  }
  return runs;
}

// ------------------------------------------------------------------
// Block renderers
// ------------------------------------------------------------------
function heading(text, level) {
  const headingLevels = [
    HeadingLevel.HEADING_1, HeadingLevel.HEADING_2,
    HeadingLevel.HEADING_3, HeadingLevel.HEADING_4,
  ];
  const sizes = [40, 30, 24, 20]; // slightly larger so Aptos reads with authority
  return new Paragraph({
    heading: headingLevels[Math.min(level - 1, 3)],
    spacing: { before: 340 - (level - 1) * 40, after: 160 - (level - 1) * 20 },
    children: [new TextRun({
      text,
      bold: true,
      font: level <= 2 ? FONT_DISPLAY : FONT_BODY,
      size: sizes[Math.min(level - 1, 3)],
      color: level === 1 ? NAVY : '0B111E',
    })],
  });
}

function paragraph(text) {
  return new Paragraph({
    spacing: { after: 140 },
    children: parseInline(text),
  });
}

function blockquote(text) {
  return new Paragraph({
    spacing: { after: 140 },
    indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 20, color: TEAL, space: 12 } },
    children: parseInline(text).map(r => {
      if (r instanceof TextRun) {
        // can't set italics on an existing TextRun, so just leave it
      }
      return r;
    }),
  });
}

function bulletItem(text) {
  return new Paragraph({
    bullet: { level: 0 },
    spacing: { after: 60 },
    children: parseInline(text),
  });
}

function codeBlock(lines, lang) {
  // Render as a bordered single-cell table to emulate a monospace code block
  const body = lines.length === 0 ? [''] : lines;
  const para = body.map(l => new Paragraph({
    spacing: { after: 0, line: 240 },
    children: [new TextRun({
      text: l.length === 0 ? ' ' : l,
      font: FONT_CODE,
      size: 18,
      color: '1F2937',
    })],
  }));
  // Prepend a tiny language label if present
  if (lang) {
    para.unshift(new Paragraph({
      spacing: { after: 40 },
      children: [new TextRun({
        text: lang.toUpperCase(),
        font: FONT_CODE,
        size: 14,
        color: DIM,
        bold: true,
      })],
    }));
  }
  if (lang === 'mermaid') {
    para.push(new Paragraph({
      spacing: { before: 40 },
      children: [new TextRun({
        text: '(Mermaid diagram — see markdown source for rendered version)',
        italics: true,
        size: 16,
        color: DIM,
      })],
    }));
  }
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
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [new TableRow({ children: [cell] })],
  });
}

function renderTable(headerCells, bodyRows) {
  const mkCell = (text, isHeader) => new TableCell({
    margins: CELL_MARGINS,
    shading: isHeader ? HEADER_SHADING : undefined,
    borders: {
      top: FAINT_BORDER, bottom: FAINT_BORDER,
      left: FAINT_BORDER, right: FAINT_BORDER,
    },
    children: [new Paragraph({
      spacing: { after: 0 },
      children: parseInline(text).map(r => {
        if (r instanceof TextRun && isHeader) {
          // recreate with header color/bold
          return new TextRun({ text: r.options?.text || '', bold: true, color: 'FFFFFF', size: 18 });
        }
        return r;
      }),
    })],
  });
  const rows = [
    new TableRow({
      tableHeader: true,
      children: headerCells.map(c => mkCell(c, true)),
    }),
    ...bodyRows.map(cells =>
      new TableRow({ children: cells.map(c => mkCell(c, false)) })
    ),
  ];
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows,
  });
}

function horizontalRule() {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 6, color: 'C0C0C5', space: 1 },
    },
    children: [new TextRun({ text: '' })],
  });
}

// ------------------------------------------------------------------
// Parser — walks markdown lines and emits docx elements
// ------------------------------------------------------------------
function parseMarkdown(md) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Code fence
    if (/^```/.test(line) || /^~~~/.test(line)) {
      const fence = line.slice(0, 3);
      const lang = line.slice(3).trim();
      const body = [];
      i++;
      while (i < lines.length && !lines[i].startsWith(fence)) {
        body.push(lines[i]);
        i++;
      }
      i++; // skip closing fence
      out.push(codeBlock(body, lang));
      continue;
    }

    // Heading
    const hMatch = line.match(/^(#{1,4})\s+(.+)$/);
    if (hMatch) {
      out.push(heading(stripInlineMarkers(hMatch[2]), hMatch[1].length));
      i++;
      continue;
    }

    // Horizontal rule
    if (/^---+\s*$/.test(line)) {
      out.push(horizontalRule());
      i++;
      continue;
    }

    // Table — header row followed by separator row
    if (line.includes('|') && i + 1 < lines.length && /^\s*\|?[\s|:-]+\|?\s*$/.test(lines[i + 1]) && lines[i + 1].includes('|')) {
      const headerCells = splitTableRow(line);
      i += 2; // skip header + separator
      const body = [];
      while (i < lines.length && lines[i].trim() !== '' && lines[i].includes('|')) {
        body.push(splitTableRow(lines[i]));
        i++;
      }
      out.push(renderTable(headerCells, body));
      out.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: '' })] }));
      continue;
    }

    // Blockquote (possibly multi-line)
    if (/^>\s?/.test(line)) {
      const bq = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        bq.push(lines[i].replace(/^>\s?/, ''));
        i++;
      }
      out.push(blockquote(bq.join(' ')));
      continue;
    }

    // Bullet list (-/*)
    if (/^\s*[-*]\s+/.test(line)) {
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        const item = lines[i].replace(/^\s*[-*]\s+/, '');
        out.push(bulletItem(item));
        i++;
      }
      continue;
    }

    // Blank line — skip
    if (line.trim() === '') {
      i++;
      continue;
    }

    // Accumulate multi-line paragraph
    const buf = [line];
    i++;
    while (i < lines.length
           && lines[i].trim() !== ''
           && !/^(#{1,4})\s/.test(lines[i])
           && !/^```/.test(lines[i])
           && !/^~~~/.test(lines[i])
           && !/^>/.test(lines[i])
           && !/^\s*[-*]\s+/.test(lines[i])
           && !/^---+\s*$/.test(lines[i])
           && !lines[i].includes('|')) {
      buf.push(lines[i]);
      i++;
    }
    out.push(paragraph(buf.join(' ')));
  }
  return out;
}

function splitTableRow(line) {
  // Strip leading/trailing pipes, then split
  return line
    .replace(/^\s*\|/, '')
    .replace(/\|\s*$/, '')
    .split('|')
    .map(c => c.trim());
}

function stripInlineMarkers(text) {
  return text.replace(/`/g, '').replace(/\*\*/g, '').replace(/\*/g, '');
}

// ------------------------------------------------------------------
// Title page + section divider helpers
// ------------------------------------------------------------------
function pageBreak() {
  return new Paragraph({ children: [new TextRun({ children: [new PageBreak()] })] });
}

function titlePageElements() {
  return [
    new Paragraph({ spacing: { before: 2400, after: 120 },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: GUIDE_TITLE, bold: true, font: FONT_DISPLAY, size: 72, color: NAVY })] }),
    new Paragraph({ spacing: { after: 240 },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'Spine + 7 Companions · Combined Edition', font: FONT_DISPLAY, size: 30, color: TEAL, italics: true })] }),
    new Paragraph({ spacing: { after: 3200 },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'APEX Core v1.2 · Developer Guide v1.0 · 2026-04-18', font: FONT_BODY, size: 22, color: DIM })] }),
    new Paragraph({ spacing: { after: 120 },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'Audience: Executives · Architects · Developers', font: FONT_BODY, size: 22, color: '1F2937' })] }),
    new Paragraph({ spacing: { after: 120 },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'For Microsoft Fabric SaaS and Azure AI', font: FONT_BODY, size: 22, color: '1F2937' })] }),
    pageBreak(),
  ];
}

function tableOfContentsElements() {
  const items = FILES.map(f => ({
    title: f.sectionTitle,
    body: (() => {
      const md = fs.readFileSync(path.join(__dirname, f.md), 'utf8');
      // Pull the first H1 title from the md (first "# " line) for the TOC entry
      const m = md.match(/^#\s+(.+)$/m);
      return m ? m[1].trim() : '';
    })(),
  }));
  const els = [];
  els.push(new Paragraph({ spacing: { before: 400, after: 300 },
    alignment: AlignmentType.LEFT,
    children: [new TextRun({ text: 'Contents', bold: true, font: FONT_DISPLAY, size: 48, color: NAVY })] }));
  items.forEach((it, idx) => {
    els.push(new Paragraph({ spacing: { after: 60 },
      children: [
        new TextRun({ text: `${it.title}`, bold: true, size: 22, color: '1F2937' }),
      ] }));
    if (it.body) {
      els.push(new Paragraph({ spacing: { after: 160 },
        indent: { left: 360 },
        children: [new TextRun({ text: it.body, size: 20, color: DIM, italics: true })] }));
    }
  });
  els.push(pageBreak());
  return els;
}

function sectionDivider(title) {
  return [
    new Paragraph({ spacing: { before: 600, after: 120 },
      alignment: AlignmentType.LEFT,
      children: [new TextRun({ text: title, bold: true, font: FONT_DISPLAY, size: 44, color: TEAL })] }),
    new Paragraph({ spacing: { after: 360 },
      alignment: AlignmentType.LEFT,
      border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: NAVY, space: 12 } },
      children: [new TextRun({ text: '' })] }),
  ];
}

// ------------------------------------------------------------------
// Combined-document assembly
// ------------------------------------------------------------------
async function renderCombined() {
  const allElements = [];

  // 1. Title page
  allElements.push(...titlePageElements());

  // 2. Table of contents
  allElements.push(...tableOfContentsElements());

  // 3. Each source file, with a section-divider before it and a page break after
  for (let idx = 0; idx < FILES.length; idx++) {
    const entry = FILES[idx];
    const mdPath = path.join(__dirname, entry.md);
    const md = fs.readFileSync(mdPath, 'utf8');

    // Section divider (skip for the very first one to avoid double title)
    allElements.push(...sectionDivider(entry.sectionTitle));

    // Parse and append
    const parsed = parseMarkdown(md);
    allElements.push(...parsed);

    // Page break between parts (skip after the last)
    if (idx < FILES.length - 1) {
      allElements.push(pageBreak());
    }
  }

  const doc = new Document({
    creator: 'APEX Core',
    title: GUIDE_TITLE,
    description: 'APEX Developer Implementation Guide — spine + 7 companions, combined edition',
    styles: {
      default: {
        document: {
          run: { font: FONT_BODY, size: 22 }, // 11pt Aptos, document-wide default
        },
      },
      paragraphStyles: [
        { id: 'Hyperlink', name: 'Hyperlink', basedOn: 'Normal',
          run: { font: FONT_BODY, color: '0563C1', underline: {} } },
      ],
    },
    sections: [{
      properties: { page: { margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: GUIDE_TITLE, size: 16, color: DIM, italics: true })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: 'APEX Core v1.2 · Developer Guide v1.0 · Page ', size: 16, color: DIM }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: DIM }),
            ],
          })],
        }),
      },
      children: allElements,
    }],
  });

  const buf = await Packer.toBuffer(doc);
  const outPath = path.join(__dirname, OUTPUT_DOCX);
  fs.writeFileSync(outPath, buf);
  return { outPath, sizeKb: Math.round(buf.length / 1024), elementCount: allElements.length };
}

(async () => {
  console.log('Rendering combined APEX Developer Guide to single .docx ...\n');
  try {
    const { outPath, sizeKb, elementCount } = await renderCombined();
    console.log(`  ✓ ${path.relative(__dirname, outPath)}`);
    console.log(`    ${sizeKb} KB  ·  ${elementCount} elements  ·  ${FILES.length} source files combined`);
  } catch (err) {
    console.error(`  ✗ failed — ${err.message}`);
    console.error(err.stack);
    process.exitCode = 1;
  }
  console.log('\nDone.');
})();
