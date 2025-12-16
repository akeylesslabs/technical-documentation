/**
 * Akeyless Tech Docs - markdownlint custom rules (AKY###)
 *
 * Intended for use with markdownlint-cli2 via:
 *   customRules:
 *     - ./markdownlint/custom-rules.js
 *
 * Notes:
 * - Most rules ignore fenced/indented code blocks and inline code spans.
 * - Some style rules are heuristic (Oxford comma, third-person voice, etc.).
 */

"use strict";

/** Collect 1-based line numbers that are inside code blocks (fenced or indented). */
function getCodeBlockLineSet(tokens) {
  const codeLines = new Set();
  for (const t of tokens || []) {
    // markdown-it provides "map" for block tokens as [startLine0, endLine0Exclusive]
    if ((t.type === "fence" || t.type === "code_block") && Array.isArray(t.map)) {
      const start = t.map[0] + 1;
      const endExclusive = t.map[1] + 1;
      for (let ln = start; ln < endExclusive; ln++) codeLines.add(ln);
    }
  }
  return codeLines;
}

function stripInlineCode(text) {
  // Remove inline code spans: `...`
  return (text || "").replace(/`[^`]*`/g, "");
}

function isHeadingLine(line) {
  // ATX heading line
  if (/^\s*#{1,6}\s+/.test(line)) return true;
  // Setext heading underline lines (very rough)
  if (/^\s*(=+|-+)\s*$/.test(line)) return true;
  return false;
}

function report(onError, lineNumber, detail, context) {
  onError({
    lineNumber,
    detail,
    context: context || undefined
  });
}

/** Extract plain text from link tokens between link_open and link_close. */
function extractLinkText(inlineToken, linkOpenIndex) {
  const children = inlineToken.children || [];
  let text = "";
  for (let i = linkOpenIndex + 1; i < children.length; i++) {
    const c = children[i];
    if (c.type === "link_close") break;
    if (c.type === "text") text += c.content;
    if (c.type === "code_inline") text += c.content; // keep literal if present
    // Ignore images inside links; they should be descriptive elsewhere.
  }
  return text.trim();
}

module.exports = [
  /**
   * AKY001: Disallow H1 (# / Setext H1)
   * Style guide: Avoid using `#` which is reserved for document titles in ReadMe. :contentReference[oaicite:1]{index=1}
   */
  {
    names: ["AKY001", "no-heading-1"],
    description: "Disallow use of level-1 headings (H1)",
    tags: ["headings", "structure", "readme"],
    function: function (params, onError) {
      const tokens = params.tokens || [];
      for (const t of tokens) {
        if (t.type === "heading_open" && t.tag === "h1") {
          report(onError, t.lineNumber, "Level-1 headings (H1) are not allowed.");
        }
      }
    }
  },

  /**
   * AKY002: Heading hierarchy must start at H2 and not skip levels
   * Style guide: Use `##` for sections, `###` for subsections, etc. :contentReference[oaicite:2]{index=2}
   */
  {
    names: ["AKY002", "heading-hierarchy-starts-at-h2"],
    description: "Require headings to start at H2 and follow a logical hierarchy without skipping levels",
    tags: ["headings", "accessibility", "structure"],
    function: function (params, onError) {
      const tokens = (params.tokens || []).filter(t => t.type === "heading_open");
      if (tokens.length === 0) return;

      // First heading must be h2 (guide reserves h1 for ReadMe title handling).
      const first = tokens[0];
      if (first.tag !== "h2") {
        report(onError, first.lineNumber, "First heading must be level 2 (##).", `Found: <${first.tag}>`);
      }

      // No skipping levels (e.g., h2 -> h4).
      let prevLevel = null;
      for (const t of tokens) {
        const level = parseInt(String(t.tag).replace(/^h/, ""), 10);
        if (!Number.isFinite(level)) continue;
        if (prevLevel !== null && level > prevLevel + 1) {
          report(onError, t.lineNumber, "Heading levels must not skip (e.g., ## then ###, not ####).", `h${prevLevel} -> h${level}`);
        }
        prevLevel = level;
      }
    }
  },

  /**
   * AKY003: Disallow bold-only lines that look like pseudo-headings
   * Style guide: Do not use bolded text when a heading is intended. :contentReference[oaicite:3]{index=3}
   */
  {
    names: ["AKY003", "no-bold-pseudo-heading"],
    description: "Disallow paragraphs/lines that are only bold text, which often indicates a misused heading",
    tags: ["headings", "style"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;

        const raw = lines[i];
        const line = stripInlineCode(raw).trim();

        // Ignore actual headings and list items; focus on standalone “**Heading**” lines.
        if (isHeadingLine(line) || /^(\*|-|\d+\.)\s+/.test(line)) continue;

        // Standalone bold text line (common pseudo-heading pattern)
        if (/^(?:\*\*[^*].*[^*]\*\*|__[^_].*[^_]__)$/.test(line)) {
          report(onError, ln, "Avoid using bold text as a heading; use a proper markdown heading (##, ###, ...).", line);
        }
      }
    }
  },

  /**
   * AKY004: Require fenced code blocks to specify a language
   * Style guide: Use triple backticks with language identifiers. :contentReference[oaicite:4]{index=4}
   */
  {
    names: ["AKY004", "fenced-code-language-required"],
    description: "Require fenced code blocks to specify a language identifier",
    tags: ["code", "style"],
    function: function (params, onError) {
      const tokens = params.tokens || [];
      for (const t of tokens) {
        if (t.type === "fence") {
          const info = (t.info || "").trim();
          if (!info) {
            report(onError, t.lineNumber, "Fenced code blocks must include a language identifier (e.g., ```bash).");
          }
        }
      }
    }
  },

  /**
   * AKY005: Link text must be descriptive (stricter than generic checks)
   * Style guide: Use descriptive link text instead of "click here." :contentReference[oaicite:5]{index=5}
   */
  {
    names: ["AKY005", "no-generic-link-text"],
    description: "Disallow generic link text like 'click here' and require descriptive labels",
    tags: ["links", "accessibility"],
    function: function (params, onError) {
      const banned = new Set([
        "click here",
        "here",
        "this link",
        "link",
        "learn more",
        "more"
      ]);

      const tokens = params.tokens || [];
      for (const t of tokens) {
        if (t.type !== "inline" || !Array.isArray(t.children)) continue;
        const children = t.children;

        for (let i = 0; i < children.length; i++) {
          const c = children[i];
          if (c.type === "link_open") {
            const linkText = extractLinkText(t, i);
            const normalized = linkText.toLowerCase().replace(/\s+/g, " ").trim();
            if (banned.has(normalized)) {
              report(onError, t.lineNumber, "Link text should be descriptive; avoid generic phrases like 'click here'.", linkText);
            }
          }
        }
      }
    }
  },

  /**
   * AKY006: Disallow Latin abbreviations/phrases in prose (e.g., e.g., i.e., ad hoc)
   * Style guide: Avoid Latin phrases and abbreviations. :contentReference[oaicite:6]{index=6}
   */
  {
    names: ["AKY006", "no-latin-abbreviations"],
    description: "Disallow Latin abbreviations and phrases (e.g., i.e., e.g., ad hoc) in prose",
    tags: ["language", "style", "localization"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];
      const re = /\b(e\.g\.|i\.e\.|ad hoc)\b/gi;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;

        const text = stripInlineCode(lines[i]);
        const m = text.match(re);
        if (m) {
          report(onError, ln, "Avoid Latin abbreviations/phrases; rewrite using plain language.", m[0]);
        }
      }
    }
  },

  /**
   * AKY007: Prefer third-person voice (heuristic; skipped for Quickstarts)
   * Style guide: Prefer third-person; Quickstarts are exempt. :contentReference[oaicite:7]{index=7}
   */
  {
    names: ["AKY007", "prefer-third-person-voice"],
    description: "Flag first/second-person voice in prose (heuristic). Skips files whose path includes 'quickstart'.",
    tags: ["tone", "style"],
    function: function (params, onError) {
      const name = (params.name || "").toLowerCase();
      if (name.includes("quickstart")) return;

      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      // Heuristic pronouns; tune as needed.
      const re = /\b(i|we|you|your|yours|our|ours|my|mine|us)\b/gi;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        const text = stripInlineCode(lines[i]);
        const m = text.match(re);
        if (m) {
          report(onError, ln, "Prefer third-person voice where practical (Quickstarts exempt).", m[0]);
        }
      }
    }
  },

  /**
   * AKY008: Enforce Oxford comma (heuristic)
   * Style guide: Use the serial (Oxford) comma. :contentReference[oaicite:8]{index=8}
   */
  {
    names: ["AKY008", "oxford-comma"],
    description: "Flag likely missing Oxford commas in lists of three or more items (heuristic)",
    tags: ["punctuation", "style"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      // Example flagged: "A, B and C" (no comma before and/or)
      const re = /(\b[^,]+),\s+([^,]+)\s+(and|or)\s+([^,.;:!?]+)\b/i;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        const text = stripInlineCode(lines[i]);
        const m = text.match(re);
        if (m && !/,(\s+)(and|or)\b/i.test(m[0])) {
          report(onError, ln, "Use the Oxford comma in series of three or more items.", m[0].trim());
        }
      }
    }
  },

  /**
   * AKY009: Disallow ampersands in sentences (allow in headings)
   * Style guide: Avoid '&' in sentences; acceptable in headings. :contentReference[oaicite:9]{index=9}
   */
  {
    names: ["AKY009", "no-ampersand-in-sentences"],
    description: "Disallow '&' in paragraph text; allow in headings",
    tags: ["punctuation", "style"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;

        const raw = lines[i];
        if (isHeadingLine(raw)) continue;

        const text = stripInlineCode(raw);
        if (text.includes("&")) {
          report(onError, ln, "Avoid using '&' in sentences; rewrite using 'and' (ampersands allowed in headings).", raw.trim());
        }
      }
    }
  },

  /**
   * AKY010: Enforce ISO 8601 date format (YYYY-MM-DD)
   * Style guide: Dates must be YYYY-MM-DD. :contentReference[oaicite:10]{index=10}
   */
  {
    names: ["AKY010", "iso-date-format"],
    description: "Flag dates not using ISO 8601 format (YYYY-MM-DD)",
    tags: ["consistency", "style"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      const mmddyyyy = /\b\d{1,2}[\/-]\d{1,2}[\/-]\d{2,4}\b/;
      const monthName = /\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b/i;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        const text = stripInlineCode(lines[i]);

        // Flag common numeric formats (MM/DD/YYYY, DD-MM-YYYY, etc.)
        const m1 = text.match(mmddyyyy);
        if (m1 && !/\b\d{4}-\d{2}-\d{2}\b/.test(m1[0])) {
          report(onError, ln, "Use ISO 8601 dates: YYYY-MM-DD.", m1[0]);
        }

        // Flag month-name date styles (e.g., "Dec 16, 2025")
        if (monthName.test(text) && /\b\d{1,2}\b/.test(text) && /\b\d{4}\b/.test(text)) {
          // Avoid double-reporting if it already contains an ISO date.
          if (!/\b\d{4}-\d{2}-\d{2}\b/.test(text)) {
            report(onError, ln, "Prefer ISO 8601 dates (YYYY-MM-DD) instead of month-name formats.", text.trim());
          }
        }
      }
    }
  },

  /**
   * AKY011: Use numerals for numbers (heuristic, limited dictionary)
   * Style guide: Use numerals for all numbers. :contentReference[oaicite:11]{index=11}
   */
  {
    names: ["AKY011", "numerals-for-numbers"],
    description: "Flag spelled-out small numbers in prose (heuristic)",
    tags: ["consistency", "localization"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      // Conservative list to reduce false positives.
      const re = /\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b/gi;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        const text = stripInlineCode(lines[i]);
        const m = text.match(re);
        if (m) {
          report(onError, ln, "Use numerals for numbers (e.g., '3 files' not 'three files').", m[0]);
        }
      }
    }
  },

  /**
   * AKY012: Enforce SI unit formatting:
   * - Space between value and unit (e.g., "10 GB", "12 ms")
   * - Correct capitalization (e.g., "GB" not "gb")
   * Style guide: Units guidance and casing distinctions. :contentReference[oaicite:12]{index=12}
   */
  {
    names: ["AKY012", "si-unit-format"],
    description: "Enforce space and capitalization for common SI units (heuristic)",
    tags: ["consistency", "style"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      // Missing space: "10GB", "12ms", etc.
      const missingSpace = /\b(\d+)(KB|MB|GB|TB|ms|s|Mb|Gb|Tb|Kb|B|b)\b/g;

      // Bad casing: "10 gb", "10gb", etc.
      const badCasing = /\b\d+\s*(kb|mb|gb|tb|ms|secs?|msec|gbs?)\b/gi;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        const text = stripInlineCode(lines[i]);

        const m1 = text.match(missingSpace);
        if (m1) {
          report(onError, ln, "Put a space between the number and unit (e.g., '10 GB', '12 ms').", m1[0]);
        }

        const m2 = text.match(badCasing);
        if (m2) {
          report(onError, ln, "Use correct unit capitalization (e.g., 'GB' not 'gb').", m2[0]);
        }
      }
    }
  },

  /**
   * AKY014: Require meaningful alt text for images
   * Style guide: Provide alt-text for images. :contentReference[oaicite:13]{index=13}
   */
  {
    names: ["AKY014", "image-alt-text-meaningful"],
    description: "Require non-empty, meaningful alt text for images",
    tags: ["accessibility", "images"],
    function: function (params, onError) {
      const tokens = params.tokens || [];
      for (const t of tokens) {
        if (t.type !== "inline" || !Array.isArray(t.children)) continue;
        for (const c of t.children) {
          if (c.type === "image") {
            const alt = (c.content || "").trim();
            const normalized = alt.toLowerCase();
            if (!alt || alt.length < 3 || normalized === "image" || normalized === "screenshot") {
              report(onError, t.lineNumber, "Images must have meaningful alt text (not empty or generic).", alt || "(empty)");
            }
          }
        }
      }
    }
  },

  /**
   * AKY015: Disallow inline HTML except <details>/<summary>
   * Style guide: Custom HTML should generally be avoided, but <details> is acceptable. :contentReference[oaicite:14]{index=14}
   */
  {
    names: ["AKY015", "html-only-details-summary"],
    description: "Allow only <details> and <summary> HTML tags; flag other HTML",
    tags: ["html", "readme", "style"],
    function: function (params, onError) {
      const tokens = params.tokens || [];
      const allowed = new Set(["details", "summary"]);

      for (const t of tokens) {
        if (t.type !== "html_block" && t.type !== "html_inline") continue;
        const html = String(t.content || "");

        // Find all tags like <tag ...> or </tag>
        const tagMatches = html.matchAll(/<\/?\s*([a-zA-Z0-9-]+)/g);
        for (const m of tagMatches) {
          const tag = (m[1] || "").toLowerCase();
          if (tag && !allowed.has(tag)) {
            report(onError, t.lineNumber, "Avoid custom HTML; only <details> and <summary> are allowed.", `<${tag}>`);
            break;
          }
        }
      }
    }
  }
];
