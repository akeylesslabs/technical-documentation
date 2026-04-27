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

function loadAllowlistSet(values, filePath) {
  const inlineValues = Array.isArray(values) ? values : [];
  return new Set(
    [...inlineValues, ...loadNamesFromFile(filePath)]
      .map((value) => String(value || "").trim())
      .filter(Boolean)
  );
}

function parseFenceInfo(info) {
  const trimmed = String(info || "").trim();
  if (!trimmed) return { language: "", tab: "" };

  const match = trimmed.match(/^(\S+)(?:\s+(.+))?$/);
  if (!match) return { language: trimmed, tab: "" };

  return {
    language: match[1],
    tab: (match[2] || "").trim()
  };
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

function report(onError, lineNumber, detail, context, fixInfo) {
  onError({
    lineNumber,
    detail,
    context: context || undefined,
    fixInfo: fixInfo || undefined
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

function removeBoldSpans(text) {
  // Removes entire bold spans (including their content).
  // This is intentionally aggressive to prevent false positives.
  return (text || "")
    .replace(/\*\*[^*]+\*\*/g, "")
    .replace(/__[^_]+__/g, "");
}

function stripBlockQuotePrefix(line) {
  let text = String(line || "");
  let prev = null;
  while (text !== prev) {
    prev = text;
    text = text.replace(/^\s*>\s?/, "");
  }
  return text;
}

function splitTableCellsLoose(line) {
  let text = stripBlockQuotePrefix(line).trim();
  if (!text || text.indexOf("|") === -1) return null;

  if (text.startsWith("|")) text = text.slice(1);
  if (text.endsWith("|")) text = text.slice(0, -1);

  const cells = [];
  let current = "";
  let escaped = false;

  for (const ch of text) {
    if (escaped) {
      current += ch;
      escaped = false;
      continue;
    }

    if (ch === "\\") {
      current += ch;
      escaped = true;
      continue;
    }

    if (ch === "|") {
      cells.push(current.trim());
      current = "";
      continue;
    }

    current += ch;
  }

  cells.push(current.trim());
  return cells;
}

function collapseExtraSpacesOutsideInlineCode(line) {
  const text = String(line || "");
  const inlineCodeRegex = /`[^`]*`/g;
  const proseDoubleSpaceRegex = /([\p{L}\p{N}][.!?;:,)]?) {2,}(?=[\p{L}\p{N}])/gu;
  let result = "";
  let cursor = 0;
  let match;

  while ((match = inlineCodeRegex.exec(text)) !== null) {
    const before = text.slice(cursor, match.index);
    result += before.replace(proseDoubleSpaceRegex, "$1 ");
    result += match[0];
    cursor = inlineCodeRegex.lastIndex;
  }

  result += text.slice(cursor).replace(proseDoubleSpaceRegex, "$1 ");
  return result;
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
   * AKY022: Validate fenced code info strings against allowlisted languages and tab labels.
   *
   * Options (in .markdownlint-cli2.yaml):
   *   AKY022:
   *     languages_file: path/to/fence-languages.txt
   *     tabs_file: path/to/fence-tabs.txt
   *     languages:
   *       - shell
   *     tabs:
   *       - Example Tab
   */
  {
    names: ["AKY022", "fenced-code-info-allowlist"],
    description: "Validate fenced code info strings against allowlisted languages and tab labels",
    tags: ["code", "style"],
    function: function (params, onError) {
      const cfg = params.config || {};
      const allowPhrases = new Set(
        (Array.isArray(cfg.allow_phrases) ? cfg.allow_phrases : [])
          .map((s) => String(s || "").trim().toLowerCase())
          .filter(Boolean)
      );
      const allowedLanguages = loadAllowlistSet(cfg.languages, cfg.languages_file);
      const allowedTabs = loadAllowlistSet(cfg.tabs, cfg.tabs_file);
      const validateTabs = allowedTabs.size > 0;

      for (const token of params.tokens || []) {
        if (token.type !== "fence") continue;

        const info = (token.info || "").trim();
        if (!info) continue;

        const { language, tab } = parseFenceInfo(info);

        if (!allowedLanguages.has(language)) {
          report(
            onError,
            token.lineNumber,
            `Unknown fenced code language identifier '${language}'. Add it to the AKY022 language allowlist if it is intentional.`,
            info
          );
          continue;
        }

        if (tab && validateTabs && !allowedTabs.has(tab)) {
          report(
            onError,
            token.lineNumber,
            `Unknown fenced code tab label '${tab}'. Add it to the AKY022 tab allowlist if it is intentional.`,
            info
          );
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
   * AKY008: Enforce Oxford comma (heuristic, sentence-scoped, clause-aware)
   *
   * Goal:
   * - Flag likely missing Oxford commas in lists of three or more items:
   *     "A, B and C"   -> suggest "A, B, and C"
   *     "A, B or C"    -> suggest "A, B, or C"
   *
   * Avoid false positives:
   * - Do NOT match when the text after the comma is a clause:
   *     "..., the Desktop application launches X and Y"
   * - Do NOT match when "and/or" joins two verbs (compound predicate):
   *     "launches X and initiates Y"
   * - Do NOT match in headings, code blocks, or inline code.
   */
  {
    names: ["AKY008", "oxford-comma"],
    description: "Flag likely missing Oxford commas in lists of three or more items (heuristic, clause-aware)",
    tags: ["punctuation", "style"],
    function: function (params, onError) {
      const codeLines = getCodeBlockLineSet(params.tokens);
      const lines = params.lines || [];

      function splitSentences(text) {
        const s = String(text || "").trim();
        if (!s) return [];
        return s
          .split(/(?<=[.!?])\s+/)
          .map(t => t.trim())
          .filter(Boolean);
      }

      // Strong indicators that the middle segment is NOT a list item.
      // These frequently introduce appositives or clauses.
      const clauseIntroducers = /^(the|a|an|this|that|these|those|which|who|whom|whose|where|when|while|because|if|since|although|as|in|on|at|for|with|by|to|from|of)\b/i;

      // A broader (but still heuristic) verb detection.
      // Instead of enumerating specific verbs, catch common verb morphology and auxiliaries.
      const auxVerbs = /\b(is|are|was|were|be|being|been|do|does|did|have|has|had|can|could|will|would|shall|should|may|might|must)\b/i;
      const verbMorphology = /\b\w+(ed|ing|ize|ises|ized|izes|ify|ifies)\b/i; // rough but effective
      const verbish = new RegExp(`${auxVerbs.source}|${verbMorphology.source}`, "i");

      const startsWithArticle = /^(the|a|an)\b/i;

      // Candidate pattern: "A, B and C" or "A, B or C"
      // Tightened constraints:
      // - A and B must not contain obvious clause punctuation
      // - B must not start like an appositive/clause (determiners, relative pronouns, prepositions)
      // - The conjunction must be standalone "and" or "or"
      // - Avoid matching if there is already an Oxford comma
      const candidate = /(^|[\s(])([^,.!?;:\n]{1,50}),\s+([^,.!?;:\n]{1,50})\s+(and|or)\s+([^,.!?;:\n]{1,80})(?=$|[)\s,.!?;:])/i;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        const raw = stripInlineCode(lines[i]);
        if (!raw) continue;

        const sentences = splitSentences(raw);

        for (const sentence of sentences) {
          // If it already has an Oxford comma, do not flag.
          if (/\b,\s+(and|or)\b/i.test(sentence)) continue;

          const m = sentence.match(candidate);
          if (!m) continue;

          const a = (m[2] || "").trim();
          const b = (m[3] || "").trim();
          const conj = (m[4] || "").trim().toLowerCase();
          const c = (m[5] || "").trim();

          // Exclude if B looks like the start of an appositive/clause
          if (clauseIntroducers.test(b)) continue;

          // Exclude if B contains verbs (likely clause)
          if (verbish.test(b)) continue;

          // Exclude if C begins with a clause introducer or looks verb-led (compound predicate)
          const cFirst = (c.split(/\s+/)[0] || "").trim();
          if (clauseIntroducers.test(cFirst)) continue;
          if (startsWithArticle.test(a) || startsWithArticle.test(b)) continue;
          if (verbish.test(cFirst)) continue;

          // Exclude some adverb-led predicates which are rarely list items
          if (/^(securely|quickly|automatically|directly|also|then|now|always|never|only)\b/i.test(c)) continue;

          // If we got here, it's likely a list missing the Oxford comma.
          report(onError, ln, `Use the Oxford comma in series of three or more items ("${a}, ${b}, ${conj} ${c}").`, sentence);
          break;
        }
      }
    }
  },

  
    /**
     * AKY009: Disallow ampersands in prose (configurable ignores)
     *
     * Purpose:
     * - Flags "&" usage so writers use "and" in prose.
     *
     * Options (in .markdownlint-cli2.yaml):
     *   AKY009:
     *     severity: error|warning|info            # Optional; markdownlint-cli2 uses "error" by default
     *     ignore_headings: true|false            # Default: true
     *     ignore_code: true|false                # Default: true  (fenced/indented code blocks + inline code spans)
     *     ignore_bold: true|false                # Default: true  (ignore "&" inside **bold** or __bold__)
     *     ignore_urls: true|false                # Default: true  (ignore "&" inside URLs)
     *
     * Notes:
     * - If ignore_urls is enabled, "&" inside URLs will NOT be flagged.
     * - If ignore_bold is enabled, "&" inside bold spans will NOT be flagged.
     * - If ignore_code is enabled, "&" inside inline code (`...`) will NOT be flagged.
     * - If ignore_headings is enabled, heading lines are skipped.
     */
    {
    names: ["AKY009", "no-ampersand-in-prose"],
    description: "Disallow '&' in prose; configurable ignores for headings, code, bold spans, and URLs",
    tags: ["punctuation", "style"],
    function: function (params, onError) {
        const cfg = params.config || {};

        // Defaults (recommended)
        const ignoreHeadings = cfg.ignore_headings !== false; // default true
        const ignoreCode = cfg.ignore_code !== false;         // default true
        const ignoreBold = cfg.ignore_bold !== false;         // default true
        const ignoreUrls = cfg.ignore_urls !== false;         // default true

        const tokens = params.tokens || [];
        const lines = params.lines || [];

        // If ignoreCode: compute code block line set
        const codeLines = ignoreCode ? getCodeBlockLineSet(tokens) : new Set();

        function stripInlineCodeSpans(text) {
        return (text || "").replace(/`[^`]*`/g, "");
        }

        function removeBoldSpans(text) {
        // Removes entire bold spans (including content) to ignore "&" inside them.
        // This is intentionally aggressive to prevent false positives.
        return (text || "")
            .replace(/\*\*[^*]+\*\*/g, "")
            .replace(/__[^_]+__/g, "");
        }

        function stripUrlsLocal(text) {
        // Prefer your existing helper if present.
        if (typeof stripUrls === "function") return stripUrls(text);

        // Fallback URL stripping:
        return (text || "")
            .replace(/\bhttps?:\/\/[^\s)>"']+/gi, "")
            .replace(/\bwww\.[^\s)>"']+/gi, "");
        }

        function isHeadingLineLocal(line) {
        // Use your existing helper if present; fallback here for safety.
        if (typeof isHeadingLine === "function") return isHeadingLine(line);
        if (/^\s*#{1,6}\s+/.test(line)) return true;
        if (/^\s*(=+|-+)\s*$/.test(line)) return true;
        return false;
        }

        for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;

        // Ignore fenced/indented code blocks
        if (ignoreCode && codeLines.has(ln)) continue;

        const raw = lines[i];

        // Ignore headings if configured
        if (ignoreHeadings && isHeadingLineLocal(raw)) continue;

        let text = raw;

        // Ignore URLs first so later stripping doesn't accidentally expose "&" again.
        if (ignoreUrls) text = stripUrlsLocal(text);

        // Ignore inline code spans if configured
        if (ignoreCode) text = stripInlineCodeSpans(text);

        // Ignore bolded text regions if configured
        if (ignoreBold) text = removeBoldSpans(text);

        // Now detect any remaining ampersands
        if (text.includes("&")) {
            report(
            onError,
            ln,
            "Avoid using '&' in prose; rewrite using 'and' (ampersands may be allowed in suppressed contexts).",
            raw.trim()
            );
        }
        }
    }
    },
 
  /**
   * AKY010: Enforce ISO 8601 date format (YYYY-MM-DD)
   * Style guide: Dates must be YYYY-MM-DD.
   *
   * Updated:
   * - Ignores dates inside URLs and file names (e.g., Screenshot_at_Nov_10_13-44-36.png).
   * - Strips HTML tags and removes href/src attribute values before evaluation.
   * - Month-name date detection requires an actual month-date pattern (avoids "may be idle" false positives).
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

      // Strip common attribute values like src="..." href='...'
      function stripHtmlAttributeValues(text) {
        return (text || "")
          .replace(/\b(?:src|href)=(".*?"|'.*?')/gi, "")
          .replace(/\b(?:src|href)=([^\s>]+)/gi, "");
      }

      // Remove filename-like tokens that include digits, months, and separators
      function stripFilenames(text) {
        return (text || "")
          .replace(
            /\b[^\s/\\]+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[^\s/\\]*\.(?:png|jpg|jpeg|gif|webp|svg|pdf)\b/gi,
            ""
          )
          .replace(
            /\b[^\s/\\]*\d{1,4}[\/_-]\d{1,2}[\/_-]\d{1,4}[^\s/\\]*\.(?:png|jpg|jpeg|gif|webp|svg|pdf)\b/gi,
            ""
          );
      }

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (codeLines.has(ln)) continue;
        if (isHeadingLine(lines[i])) continue;

        let text = stripInlineCode(lines[i]);
        text = stripUrls(text);
        text = stripHtmlTags(text);
        text = stripHtmlAttributeValues(text);
        text = stripFilenames(text);

        // Flag common numeric formats (MM/DD/YYYY, DD-MM-YYYY, etc.)
        const m1 = text.match(mmddyyyy);
        if (m1 && !/\b\d{4}-\d{2}-\d{2}\b/.test(m1[0])) {
          report(onError, ln, "Use ISO 8601 dates: YYYY-MM-DD.", m1[0]);
          continue;
        }

        // Month-name date styles like "Dec 16, 2025" or "16 Dec 2025"
        // Only match if the month name is adjacent to day+year (avoid "may be idle" false positives).
        const monthDate = new RegExp(
          String.raw`\b(?:${monthName.source})\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*|\s+)\d{4}\b`,
          "i"
        );

        const dateMonth = new RegExp(
          String.raw`\b\d{1,2}(?:st|nd|rd|th)?\s+(?:${monthName.source})(?:,\s*|\s+)\d{4}\b`,
          "i"
        );

        if ((monthDate.test(text) || dateMonth.test(text)) && !/\b\d{4}-\d{2}-\d{2}\b/.test(text)) {
          report(onError, ln, "Prefer ISO 8601 dates (YYYY-MM-DD) instead of month-name formats.", text.trim());
        }
      }
    }
  },

  /**
   * AKY011: Disallow ReadMe proprietary <Callout> tags.
   *
   * Purpose:
   * - Enforces the repository standard to use markdown blockquote callouts
   *   (for example, "> ⚠️ **Warning:**") instead of proprietary ReadMe tags.
   *
   * Behavior:
   * - Detection-only rule (no auto-fix).
   * - Flags both opening and closing Callout tags:
   *     <Callout ...>
   *     </Callout>
   * - Ignores fenced/indented code blocks and inline code spans by default.
   *
   * Options (in .markdownlint-cli2.yaml):
   *   AKY011:
   *     severity: error|warning|info   # Recommended: warning
   *     ignore_code: true|false        # Default: true
   */
  {
    names: ["AKY011", "no-readme-callout-tag"],
    description: "Disallow ReadMe proprietary <Callout> tags; use markdown blockquote callouts instead",
    tags: ["callouts", "readme", "style"],
    function: function (params, onError) {
      const cfg = params.config || {};
      const ignoreCode = cfg.ignore_code !== false; // default true

      const codeLines = ignoreCode ? getCodeBlockLineSet(params.tokens) : new Set();
      const lines = params.lines || [];
      const calloutTagPattern = /<\s*\/?\s*Callout\b/i;

      for (let i = 0; i < lines.length; i++) {
        const ln = i + 1;
        if (ignoreCode && codeLines.has(ln)) continue;

        const raw = lines[i] || "";
        const text = ignoreCode ? stripInlineCode(raw) : raw;

        if (calloutTagPattern.test(text)) {
          report(
            onError,
            ln,
            "Use markdown blockquote callouts (for example, '> ⚠️ **Warning:**') instead of ReadMe <Callout> tags.",
            raw.trim()
          );
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
  },

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
   * - Scans normal text, Markdown link text, and HTML.
   * - Does NOT scan URLs (including href destinations and visible URLs).
   * - Skips fenced/indented code blocks and inline code spans.
   */
  {
    names: ["AKY017", "banned-terms"],
    description: "Disallow banned terms and provide replacement guidance",
    tags: ["terminology", "style"],
    function: function (params, onError) {
      const cfg = params.config || {};
      const allowPhrases = new Set(
        (Array.isArray(cfg.allow_phrases) ? cfg.allow_phrases : [])
          .map((s) => String(s || "").trim().toLowerCase())
          .filter(Boolean)
      );

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
        },
        {
          term: "AWS Route 53",
          replacement: "Amazon Route 53",
          example_from: "AWS Route 53 hosted zone",
          example_to: "Amazon Route 53 hosted zone"
        }
      ];

          const terms = Array.isArray(cfg.terms) && cfg.terms.length ? cfg.terms : defaultTerms;

          // Normalize + compile matchers once.
          const matchers = terms
            .map((t) => {
              const term = String((t && t.term) || "").trim();
              if (!term) return null;

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

      /**
       * Check text for banned terms, after stripping URLs.
       * This prevents false positives in:
       * - Visible URLs in prose
       * - Inline HTML attributes that include URLs
       */
      function checkText(lineNumber, text, contextLabel) {
        if (!text) return false;

        // Remove visible URL strings so we don't match inside them.
        const cleaned = stripUrls(String(text));
        const cleanedLower = cleaned.toLowerCase();

        for (const allowed of allowPhrases) {
          if (cleanedLower.includes(allowed)) {
            return false;
          }
        }

        for (const m of matchers) {
          if (m.re.test(cleaned)) {
            report(onError, lineNumber, formatDetail(m), `${contextLabel}: ${cleaned.trim()}`);
            return true;
          }
        }
        return false;
      }

      // Token-based scan: text + html_inline + html_block
      // NOTE: We intentionally do NOT scan link destinations (href).
      for (const t of tokens) {
        // Skip anything on a code line.
        if (codeLines.has(t.lineNumber)) continue;

        // HTML blocks can span multiple lines; attribute to the starting line.
        if (t.type === "html_block") {
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

          // IMPORTANT: Do NOT scan link_open href values
          // We only want to check the visible link label, not the URL.
          if (child.type === "link_open") {
            continue;
          }
        }
      }
    }
  },

  /**
   * AKY018: Enforce canonical Markdown table separator format
   *
   * Canonical format required for separator rows:
   *   | --- | --- |
   *
   * This catches inconsistent separator styles such as:
   *   |---|---|
   *   | :--- | :--- |
   *   | ---- | ---: |
   */
  {
    names: ["AKY018", "canonical-table-separator"],
    description: "Require Markdown table separator rows to use canonical '| --- |' style without alignment colons",
    tags: ["tables", "style", "consistency"],
    function: function (params, onError) {
      const lines = params.lines || [];
      const codeLines = getCodeBlockLineSet(params.tokens);

      for (let i = 0; i < lines.length; i++) {
        const lineNumber = i + 1;
        if (codeLines.has(lineNumber)) continue;

        const raw = lines[i];
        const normalized = stripBlockQuotePrefix(raw).trim();
        if (!normalized || normalized.indexOf("|") === -1) continue;

        const cells = splitTableCellsLoose(normalized);
        if (!Array.isArray(cells) || cells.length < 2) continue;

        // Identify delimiter rows like --- / :---: / ---:
        const isDelimiterRow = cells.every((cell) => /^:?-{3,}:?$/.test(cell));
        if (!isDelimiterRow) continue;

        const expected = `| ${new Array(cells.length).fill("---").join(" | ")} |`;
        if (normalized !== expected) {
          report(
            onError,
            lineNumber,
            "Use canonical table separator row format '| --- |' without alignment colons.",
            normalized
          );
        }
      }
    }
  },

  /**
   * AKY019: Collapse repeated spaces in prose outside code
   *
   * Behavior:
   * - Auto-fixes repeated spaces between non-space characters.
   * - Ignores fenced/indented code blocks.
   * - Ignores inline code spans (`...`).
   */
  {
    names: ["AKY019", "no-extra-double-spaces"],
    description: "Disallow repeated spaces in prose outside code blocks and inline code spans",
    tags: ["whitespace", "style", "autofix"],
    function: function (params, onError) {
      const lines = params.lines || [];
      const codeLines = getCodeBlockLineSet(params.tokens);

      for (let i = 0; i < lines.length; i++) {
        const lineNumber = i + 1;
        if (codeLines.has(lineNumber)) continue;

        const maybeTableCells = splitTableCellsLoose(lines[i]);
        if (Array.isArray(maybeTableCells) && maybeTableCells.length >= 2) continue;

        const originalLine = lines[i];
        const fixedLine = collapseExtraSpacesOutsideInlineCode(originalLine);

        if (fixedLine === originalLine) continue;

        report(
          onError,
          lineNumber,
          "Collapse repeated spaces to a single space outside code spans.",
          originalLine.trim(),
          {
            editColumn: 1,
            deleteCount: originalLine.length,
            insertText: fixedLine
          }
        );
      }
    }
  },

  /**
   * AKY020: Enforce emoji-prefixed blockquote callout titles
   *
   * Required format:
   *   > [emoji] **Label:**
   *   > [emoji] **Label (Context):**
   *
   * Supported labels and emoji mapping:
   * - Note, Info => ℹ️
   * - Tip => ✅
   * - Warning => ⚠️
   * - Important => ❗
   * - Caution => 🚫
   */
  {
    names: ["AKY020", "blockquote-callout-emoji-title"],
    description: "Require blockquote callout titles to include the correct emoji before bold label",
    tags: ["callouts", "style", "consistency"],
    function: function (params, onError) {
      const lines = params.lines || [];
      const codeLines = getCodeBlockLineSet(params.tokens);

      const labelSet = ["Note", "Info", "Tip", "Warning", "Important", "Caution"];
      const labelPattern = labelSet.join("|");

      const allowedTitle = new RegExp(
        `^(ℹ️|✅|⚠️|❗|🚫)\\s+\\*\\*(?<label>${labelPattern})(?:\\s*\\([^)]*\\))?:\\*\\*(?:\\s+.*)?$`,
        "u"
      );

      const calloutTitleCandidate = new RegExp(
        `^(?:ℹ️|✅|⚠️|❗|🚫)?\\s*\\*\\*(?<label>${labelPattern})(?:\\s*\\([^)]*\\))?:\\*\\*`,
        "u"
      );

      const expectedEmojiByLabel = {
        Note: "ℹ️",
        Info: "ℹ️",
        Tip: "✅",
        Warning: "⚠️",
        Important: "❗",
        Caution: "🚫"
      };

      for (let i = 0; i < lines.length; i++) {
        const lineNumber = i + 1;
        if (codeLines.has(lineNumber)) continue;

        const raw = String(lines[i] || "");
        if (!/^\s*>/.test(raw)) continue;

        const text = stripBlockQuotePrefix(raw).trim();
        if (!text) continue;

        if (!calloutTitleCandidate.test(text)) continue;

        const allowedMatch = text.match(allowedTitle);
        if (!allowedMatch) {
          report(
            onError,
            lineNumber,
            "Include an emoji before callout titles (for example, '> ℹ️ **Note:**').",
            text
          );
          continue;
        }

        const label = allowedMatch.groups && allowedMatch.groups.label ? allowedMatch.groups.label : "";
        const actualEmoji = allowedMatch[1] || "";
        const expectedEmoji = expectedEmojiByLabel[label];

        if (expectedEmoji && actualEmoji !== expectedEmoji) {
          report(
            onError,
            lineNumber,
            `Use '${expectedEmoji}' with '**${label}:**' callouts.`,
            text
          );
        }
      }
    }
  },

  /**
   * AKY021: Disallow angle-bracket URL autolinks (<http://...> / <https://...>)
   *
   * ReadMe.com renders Markdown as MDX. The CommonMark angle-bracket autolink
   * syntax  <https://example.com>  is treated as a JSX element by the MDX parser
   * and produces a hard error:
   *   "Unexpected character `/` before local name"
   *
   * Fix: convert to a proper Markdown link — [url](url) or [descriptive text](url).
   *
   * This rule is auto-fixable: it replaces <url> with [url](url).
   */
  {
    names: ["AKY021", "no-angle-bracket-url"],
    description: "Disallow angle-bracket URL autolinks (<http://...>) — use [text](url) instead for MDX compatibility",
    tags: ["links", "mdx", "style"],
    fixable: true,
    function: function (params, onError) {
      const lines = params.lines || [];
      const codeLines = getCodeBlockLineSet(params.tokens);
      const angleUrlRe = /<(https?:\/\/[^>\s]+)>/g;

      for (let i = 0; i < lines.length; i++) {
        const lineNumber = i + 1;
        if (codeLines.has(lineNumber)) continue;

        const raw = String(lines[i] || "");
        // Mask inline code spans with spaces to preserve column positions
        const masked = raw.replace(/`[^`]*`/g, (m) => " ".repeat(m.length));

        angleUrlRe.lastIndex = 0;
        let match;
        while ((match = angleUrlRe.exec(masked)) !== null) {
          const fullMatch = match[0]; // <https://example.com>
          const url = match[1];       // https://example.com
          const col = match.index + 1;

          report(
            onError,
            lineNumber,
            `Angle-bracket URL autolinks are not MDX-compatible. Replace \`${fullMatch}\` with \`[${url}](${url})\`.`,
            fullMatch,
            {
              lineNumber,
              editColumn: col,
              deleteCount: fullMatch.length,
              insertText: `[${url}](${url})`
            }
          );
        }
      }
    }
  }
]