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

const fs = require("fs");
const path = require("path");

function loadNamesFromFile(filePath) {
  if (!filePath) return [];
  const abs = path.isAbsolute(filePath)
    ? filePath
    : path.resolve(process.cwd(), filePath);

  if (!fs.existsSync(abs)) return [];

  const raw = fs.readFileSync(abs, "utf8");
  return raw
    .split(/\r?\n/)
    .map((l) => l.replace(/#.*/, "").trim()) // strip comments
    .filter(Boolean);
}

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

function escapeRegExp(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function getUrlFromLinkOpen(token) {
  if (!token || token.type !== "link_open") return "";
  const attrs = token.attrs || [];
  for (const [k, v] of attrs) {
    if (k === "href") return String(v || "");
  }
  return "";
}

function getQueryParamNames(url) {
  const qIndex = url.indexOf("?");
  if (qIndex === -1) return [];
  const hashIndex = url.indexOf("#", qIndex + 1);
  const query = url.slice(qIndex + 1, hashIndex === -1 ? url.length : hashIndex);
  if (!query) return [];

  return query
    .split("&")
    .map((part) => part.split("=", 1)[0])
    .map((name) => decodeURIComponent(name || "").trim())
    .filter(Boolean);
}

function stripUrls(text) {
  // Remove http/https and www URLs, including common punctuation terminators.
  // This is intentionally simple and resilient for docs linting.
  return (text || "")
    .replace(/\bhttps?:\/\/[^\s)>"']+/gi, "")
    .replace(/\bwww\.[^\s)>"']+/gi, "");
}

function stripHtmlTags(text) {
  // Remove HTML tags to avoid matching attribute values (src, width, etc.)
  return (text || "").replace(/<[^>]*>/g, "");
}

/**
 * Find Markdown links of the form [text](destination).
 *
 * This is intentionally heuristic:
 * - It avoids matching image syntax ![alt](src) by checking the preceding char.
 * - It does not attempt to fully parse nested parentheses/brackets.
 */
function findMarkdownLinks(text) {
  const s = String(text || "");
  const matches = [];
  const re = /\[[^\]\n]+\]\([^) \n]+(?:\s+"[^"]*")?\)/g; // [text](dest "title")
  let m;
  while ((m = re.exec(s)) !== null) {
    const start = m.index;
    if (start > 0 && s[start - 1] === "!") continue; // ignore images
    matches.push(m[0]);
  }
  return matches;
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
      const banned = new Set(["click here", "here", "this link", "link", "learn more", "more"]);

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
   * AKY006: Disallow Latin abbreviations/phrases in prose (expanded)
   * Style guide: Avoid Latin phrases and abbreviations.
   *
   * Notes:
   * - Skips fenced/indented code blocks and inline code spans.
   * - Case-insensitive.
   * - Tries to be resilient to dot/no-dot variants (e.g., "e.g." vs "eg").
   */
  {
    names: ["AKY006", "no-latin-abbreviations"],
    description: "Disallow Latin abbreviations and phrases (e.g., i.e., e.g., ad hoc) in prose",
    tags: ["language", "style", "localization"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      /**
       * Latin / Latin-derived abbreviations and phrases to flag.
       *
       * Why we do this:
       * - JavaScript RegExp literals do NOT support verbose mode (no newlines/comments).
       * - Maintaining one huge regex literal becomes hard to edit and error-prone.
       *
       * How it works:
       * - We store each pattern as a string (already escaped for RegExp).
       * - Then we join them with | into a single alternation group.
       * - We wrap with word boundaries (\b) so we don’t match inside other words.
       *
       * Notes on patterns:
       * - Dot/no-dot variants are supported for common abbreviations (e.g., e.g. vs eg).
       * - Flexible whitespace is allowed in abbreviations that may be typed with spaces (e.g., "a k a").
       * - Multi-word phrases are encoded with `\s+` to allow any whitespace.
       *
       * Extending:
       * - Add new entries to `latinPatterns`.
       * - Prefer explicit patterns rather than “too clever” ones to avoid false positives.
       */
      const latinPatterns = [
        // Common abbreviation forms (dot/no-dot variants)
        "e\\.?\\s?g\\.?",              // e.g., eg
        "i\\.?\\s?e\\.?",              // i.e., ie
        "etc\\.?",                     // etc, etc.
        "cf\\.?",                      // cf, cf.
        "vs\\.?",                      // vs, vs.
        "viz\\.?",                     // viz, viz.

        // Commonly misused in technical documentation, often unnecessary
        "ad\\s+hoc",                   // ad hoc
        "et\\s+al\\.?",                // et al, et al.
        "per\\s+se",                   // per se
        "de\\s+facto",                 // de facto
        "de\\s+jure",                  // de jure
        "ipso\\s+facto",               // ipso facto
        "status\\s+quo",               // status quo
        "in\\s+situ",                  // in situ
        "a\\s+priori",                 // a priori
        "a\\s+posteriori",             // a posteriori

        // Less common but still appears in docs
        "bona\\s+fide",                // bona fide
        "caveat(?:\\s+emptor)?",       // caveat, caveat emptor
        "inter\\s+alia",               // inter alia
        "mutatis\\s+mutandis",         // mutatis mutandis
        "prima\\s+facie",              // prima facie
        "pro\\s+rata",                 // pro rata
        "quid\\s+pro\\s+quo",          // quid pro quo
        "sui\\s+generis",              // sui generis
        "vice\\s+versa",               // vice versa
        "in\\s+re",                    // in re

        // Misc
        "n\\.?\\s?b\\.?",              // n.b., nb
        "ibid\\.?",                    // ibid, ibid.
        "ibidem",                      // ibidem
        "idem",                        // idem

        // Time abbreviations (optional: remove if you don’t want these)
        "a\\.?\\s?m\\.?",              // a.m., am
        "p\\.?\\s?m\\.?",              // p.m., pm

        // Also optional; used in narrative/marketing text
        "a\\.?\\s?k\\.?\\s?a\\.?"      // a.k.a., aka
      ];

      /**
       * Combine patterns into a single regex.
       *
       * The final structure is:
       *   \b(?:pattern1|pattern2|pattern3)\b
       *
       * Flags:
       * - g: global (find all matches)
       * - i: case-insensitive
       *
       * We keep `\b` word boundaries so:
       * - "etc" matches as a token
       * - but "etcetera" does NOT trigger for "etc"
       */
      const re = new RegExp(`\\b(?:${latinPatterns.join("|")})\\b`, "gi");

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;

        const text = stripInlineCode(lines[i]);
        const m = text.match(re);
        if (m) {
          report(
            onError,
            ln,
            "Avoid Latin abbreviations/phrases; rewrite using plain language.",
            m[0]
          );
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
      // Avoid matching hash/slug patterns like "522836b-Screenshot" by disallowing '-' immediately after the unit
      const missingSpace = /\b(\d+)(KB|MB|GB|TB|ms|s|Mb|Gb|Tb|Kb|B|b)\b(?!-)/g;

      // Bad casing: "10 gb", "10gb", etc.
      // Case-sensitive: only flag lowercase unit spellings
      const badCasing = /\b\d+\s*(kb|mb|gb|tb|secs?|msec)\b/g;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        let text = stripInlineCode(lines[i]);
        text = stripUrls(text);
        text = stripHtmlTags(text);

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
   * AKY013: Proper names must use correct capitalization (MD044-like), ignoring inline HTML <a>...</a>
   *
   * Configuration:
   * - names: [ "Akeyless", "Kubernetes", ... ] (required)
   * - code_blocks: boolean (default true) - ignore fenced/indented code blocks
   * - ignore_a_html_tag: boolean (default true) - ignore matches inside inline HTML anchors
   *
   * Notes:
   * - This ignores inline-code spans by default via token filtering.
   * - This intentionally only ignores HTML anchors expressed as inline HTML (<a>...</a>),
   *   not Markdown links. If you want to ignore Markdown link text too, say so and we’ll extend it.
   * - Updated: ignores text inside URLs (both visible text that contains URLs and href attributes are not evaluated).
   */
  {
    names: ["AKY013", "proper-names-capitalization-ignore-a"],
    description: "Enforce proper name capitalization (MD044-like), ignoring inline HTML <a>...</a> content and URLs",
    tags: ["spelling", "capitalization", "style"],
    function: function (params, onError) {
      const options = params.config || {};
      const namesInline = Array.isArray(options.names) ? options.names : [];
      const namesFromFile = loadNamesFromFile(options.names_file);
      const names = [...namesFromFile, ...namesInline];
      const checkCodeBlocks = options.code_blocks !== false;
      const ignoreAHtmlTag = options.ignore_a_html_tag !== false;

      if (names.length === 0) return;

      const canonicalByLower = new Map(names.map((n) => [String(n).toLowerCase(), String(n)]));

      // One combined regex for efficiency; we validate against canonical map after match.
      const alternation = names
        .map((n) => escapeRegExp(String(n)))
        .filter(Boolean)
        .join("|");

      if (!alternation) return;

      // Word-boundary-ish match; allows names with dashes as well.
      const re = new RegExp(`\\b(?:${alternation})\\b`, "gi");

      const tokens = params.tokens || [];
      const codeLines = checkCodeBlocks ? getCodeBlockLineSet(tokens) : new Set();

      for (const t of tokens) {
        if (t.type !== "inline" || !Array.isArray(t.children)) continue;

        // If the inline token itself is on a code line (rare, but can happen), skip.
        if (checkCodeBlocks && codeLines.has(t.lineNumber)) continue;

        let inAInlineHtml = false;

        for (const child of t.children) {
          // Skip inline code spans
          if (child.type === "code_inline") continue;

          // Track inline HTML <a>...</a>
          if (ignoreAHtmlTag && child.type === "html_inline") {
            const html = String(child.content || "");

            // Start tag: <a ...> or <a>
            if (/^<a(\s|>)/i.test(html)) {
              inAInlineHtml = true;
              continue;
            }

            // End tag: </a>
            if (/^<\/a\s*>/i.test(html)) {
              inAInlineHtml = false;
              continue;
            }
          }

          // Ignore any visible text while inside an inline HTML <a>...</a>
          if (ignoreAHtmlTag && inAInlineHtml) continue;

          if (child.type !== "text") continue;

          const segment = stripUrls(String(child.content || ""));
          let m;
          while ((m = re.exec(segment)) !== null) {
            const found = m[0];
            const canonical = canonicalByLower.get(String(found).toLowerCase());
            if (canonical && found !== canonical) {
              report(onError, t.lineNumber, `Proper name capitalization: use "${canonical}" instead of "${found}".`, segment.trim());
              break;
            }
          }

          // Reset lastIndex between different strings to avoid cross-string statefulness.
          re.lastIndex = 0;
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
   * AKY015: Disallow code spans/blocks being combined with Markdown links.
   *
   * Detects both:
   *  1) Inline links whose visible link text contains inline code (e.g., [`foo`](...)).
   *  2) Markdown link syntax inside fenced/indented code blocks (e.g., shown as code but actually a link).
   *
   * This rule intentionally looks for Markdown link syntax ([]()) rather than URL structures.
   */
  {
    names: ["AKY015", "no-links-in-code-or-code-in-links"],
    description: "Disallow Markdown links that include inline code, and disallow Markdown link syntax inside code blocks",
    tags: ["links", "code", "style"],
    function: function (params, onError) {
      const tokens = params.tokens || [];
      const lines = params.lines || [];
      const codeLines = getCodeBlockLineSet(tokens);

      // (2) Links inside code blocks: scan raw lines in code blocks for markdown link syntax.
      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (!codeLines.has(ln)) continue;

        const matches = findMarkdownLinks(lines[i]);
        if (matches.length > 0) {
          report(onError, ln, "Avoid Markdown link syntax inside code blocks. Use plain text or a non-linked example.", matches[0]);
        }
      }

      // (1) Inline code inside link text: use token stream for accuracy.
      for (const t of tokens) {
        if (t.type !== "inline" || !Array.isArray(t.children)) continue;
        if (codeLines.has(t.lineNumber)) continue;

        let inLink = false;
        let linkTextPreview = "";

        for (const child of t.children) {
          if (child.type === "link_open") {
            inLink = true;
            linkTextPreview = "";
            continue;
          }
          if (child.type === "link_close") {
            inLink = false;
            linkTextPreview = "";
            continue;
          }
          if (!inLink) continue;

          if (child.type === "text") {
            linkTextPreview += child.content;
            continue;
          }

          if (child.type === "code_inline") {
            const ctx = (`[${(linkTextPreview || "").trim()}${(child.content || "").trim()}]`).slice(0, 80);
            report(onError, t.lineNumber, "Avoid inline code inside Markdown link text. Use descriptive plain text for the link label.", ctx);
            break;
          }
        }
      }
    }
  },

  /**
   * AKY016: Disallow tracking query parameters in links (e.g., utm_source)
   * Rationale: URLs with tracking params are noisy and can leak analytics identifiers into docs.
   *
   * Config (optional):
   *   AKY016:
   *     tracking_parameters: ["utm_source", "utm_medium", ...]
   *     allow_parameters: ["param_to_ignore"]
   */
  {
    names: ["AKY016", "no-tracking-params-in-links"],
    description: "Disallow tracking query parameters (e.g., utm_source) in link URLs",
    tags: ["links", "style", "privacy"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const tokens = params.tokens || [];

      const cfg = params.config || {};
      const defaultTracking = [
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "utm_id", "utm_name",
        "utm_reader", "utm_viz_id", "utm_pubreferrer", "utm_swu",
        "gclid", "dclid", "gbraid", "wbraid", "fbclid", "msclkid", "yclid", "ttclid", "twclid", "igshid"
      ];

      const trackingSet = new Set(
        (Array.isArray(cfg.tracking_parameters) ? cfg.tracking_parameters : defaultTracking)
          .map((s) => String(s || "").toLowerCase())
          .filter(Boolean)
      );

      const allowSet = new Set(
        (Array.isArray(cfg.allow_parameters) ? cfg.allow_parameters : [])
          .map((s) => String(s || "").toLowerCase())
          .filter(Boolean)
      );

      for (const t of tokens) {
        if (t.type !== "inline" || !Array.isArray(t.children)) continue;
        if (codeLines.has(t.lineNumber)) continue;

        const children = t.children;
        for (const c of children) {
          if (c.type !== "link_open") continue;
          const href = getUrlFromLinkOpen(c);
          if (!href || href.indexOf("?") === -1) continue;

          const paramsFound = getQueryParamNames(href).map((p) => p.toLowerCase());
          for (const p of paramsFound) {
            if (allowSet.has(p)) continue;
            if (trackingSet.has(p)) {
              report(onError, t.lineNumber, `Remove tracking query parameters from links (found '${p}').`, href);
              break;
            }
          }
        }
      }
    }
  }
,

/**
 * AKY017: Banned terms (case-insensitive) with replacement guidance
 *
 * Rationale: Enforce preferred product/security terminology.
 *
 * Config (optional):
 *   AKY017:
 *     terms:
 *       - term: "Vaultless"
 *         replacement: "Zero-Knowledge Encryption with Patented DFC"
 *       - term: "vault-less"
 *         replacement: "Zero-Knowledge Encryption with Patented DFC"
 *       - term: "Non-human"
 *         replacement: "Workload Identity Federation"
 *
 * Notes:
 * - Searches case-insensitively.
 * - Scans normal text, Markdown link text, and link destinations (href).
 * - Scans inline and block HTML.
 * - Skips fenced/indented code blocks and inline code spans.
 */
{
  names: ["AKY017", "banned-terms"],
  description: "Disallow banned terms and provide replacement guidance",
  tags: ["terminology", "style"],
  function: function (params, onError) {
    const cfg = params.config || {};

    const defaultTerms = [
      {
        term: "Vaultless",
        replacement: "Zero-Knowledge Encryption with Patented DFC",
        example_from: "Vaultless Security with DFC",
        example_to: "Zero-Knowledge Encryption with Patented DFC"
      },
      {
        term: "vault-less",
        replacement: "Zero-Knowledge Encryption with Patented DFC",
        example_from: "Vaultless Security with DFC",
        example_to: "Zero-Knowledge Encryption with Patented DFC"
      },
      {
        term: "Non-human",
        replacement: "Workload Identity Federation",
        example_from: "Non-Human Identity Federation",
        example_to: "Workload Identity Federation"
      }
    ];

    const terms = Array.isArray(cfg.terms) && cfg.terms.length ? cfg.terms : defaultTerms;

    // Normalize + compile matchers once.
    const matchers = terms
      .map((t) => {
        const term = String((t && t.term) || "").trim();
        if (!term) return null;

        // Word boundary on ends when it makes sense; keep hyphenated terms intact.
        const hasWordCharEnds = /^[A-Za-z0-9]/.test(term) && /[A-Za-z0-9]$/.test(term);
        const pattern = hasWordCharEnds ? `\\b${escapeRegExp(term)}\\b` : escapeRegExp(term);

        return {
          term,
          replacement: String((t && t.replacement) || "").trim(),
          example_from: String((t && t.example_from) || "").trim(),
          example_to: String((t && t.example_to) || "").trim(),
          re: new RegExp(pattern, "i")
        };
      })
      .filter(Boolean);

    if (matchers.length === 0) return;

    const tokens = params.tokens || [];
    const codeLines = getCodeBlockLineSet(tokens);

    function formatDetail(m) {
      const parts = [];
      parts.push(`Banned term "${m.term}" found.`);
      if (m.replacement) parts.push(`Preferred: "${m.replacement}".`);
      if (m.example_from && m.example_to) {
        parts.push(`Example: "${m.example_from}" → "${m.example_to}".`);
      }
      return parts.join(" ");
    }

    function checkText(lineNumber, text, contextLabel) {
      if (!text) return false;
      for (const m of matchers) {
        if (m.re.test(text)) {
          report(onError, lineNumber, formatDetail(m), `${contextLabel}: ${String(text).trim()}`);
          return true;
        }
      }
      return false;
    }

    // Token-based scan: text + hrefs + html_inline + html_block
    for (const t of tokens) {
      // Skip anything on a code line.
      if (codeLines.has(t.lineNumber)) continue;

      // HTML blocks are separate tokens (html_block) and can span multiple lines.
      if (t.type === "html_block") {
        // Best-effort: attribute violations to the starting line.
        if (checkText(t.lineNumber, String(t.content || ""), "HTML")) continue;
      }

      if (t.type !== "inline" || !Array.isArray(t.children)) continue;

      for (const child of t.children) {
        // Skip inline code spans.
        if (child.type === "code_inline") continue;

        if (child.type === "text") {
          if (checkText(t.lineNumber, String(child.content || ""), "Text")) break;
          continue;
        }

        if (child.type === "html_inline") {
          if (checkText(t.lineNumber, String(child.content || ""), "HTML")) break;
          continue;
        }

        // Scan Markdown link destinations (href) as well.
        if (child.type === "link_open") {
          const href = getUrlFromLinkOpen(child);
          if (href && checkText(t.lineNumber, href, "Link URL")) break;
        }
      }
    }
  }
}
];