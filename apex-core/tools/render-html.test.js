import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderHtml } from './render-html.js';

const sample = {
  generated_utc: '2026-04-17T12:00:00Z',
  edition_code: 'RC',
  status: 'pass',
  summary: { critical: 0, warning: 0, info: 0 },
  findings: []
};

test('renderHtml returns a self-contained HTML document', () => {
  const html = renderHtml(sample);
  assert.match(html, /^<!doctype html>/i);
  assert.match(html, /Fraunces/);
  assert.match(html, /Instrument Sans/);
  assert.match(html, /JetBrains Mono/);
  assert.match(html, /--teal/);
  assert.match(html, /--amber/);
  assert.match(html, /--crimson/);
  assert.match(html, /\bRC\b/);
  assert.match(html, /pass/);
});

test('renderHtml surfaces critical findings in crimson', () => {
  const html = renderHtml({
    ...sample,
    status: 'fail',
    summary: { critical: 1, warning: 0, info: 0 },
    findings: [{
      severity: 'critical',
      rule: 'REQ-01',
      path: '$.edition_code',
      message: 'missing required field'
    }]
  });
  assert.match(html, /REQ-01/);
  assert.match(html, /crimson/i);
  assert.match(html, /finding critical/);
});

test('renderHtml escapes HTML in findings to prevent injection', () => {
  const html = renderHtml({
    ...sample,
    status: 'fail',
    summary: { critical: 1, warning: 0, info: 0 },
    findings: [{
      severity: 'critical',
      rule: 'X',
      path: '$',
      message: '<script>alert(1)</script>'
    }]
  });
  assert.doesNotMatch(html.replace(/<script>[\s\S]*?<\/script>/g, ''), /<script>alert/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
});

test('renderHtml handles empty findings list gracefully', () => {
  const html = renderHtml(sample);
  assert.match(html, /No findings/);
});

test('renderHtml ships a theme toggle button and persistence script', () => {
  const html = renderHtml(sample);
  assert.match(html, /class="theme-toggle"/);
  assert.match(html, /apex-theme/);
  assert.match(html, /prefers-color-scheme/);
});
