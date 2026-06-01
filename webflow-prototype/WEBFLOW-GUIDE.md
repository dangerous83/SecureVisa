# SecureVisa Group — Webflow Implementation Guide

A practical guide for rebuilding this static prototype (`index.html`, `styles.css`,
`script.js`) inside Webflow. The prototype is intentionally structured with
**Client-First-style class names** (`section_*`, `container-large`, `*_component`,
`*_grid`) so it maps cleanly onto Webflow's class + Style Manager model.

> **Positioning preserved.** Navigation, footer, regulator names, service/industry
> categories, contact details, and CTA flow mirror the existing securevisanow.com.
> This is a premium refinement of the same brand — not a new company.

---

## 0. How to use these files

- Open `index.html` directly in a browser to preview the full responsive design.
- Treat it as a **visual + structural reference**. You don't paste raw HTML into
  Webflow's canvas; instead you recreate the section structure using Webflow
  elements and reuse the class names below.
- `script.js` shows the exact interactions to reproduce — most can be rebuilt with
  **Webflow Interactions (IX2)**; the few that can't are listed in §5 as a small
  custom-code embed you can paste into Project Settings → Custom Code (before
  `</body>`).

---

## 1. Global setup in Webflow

**Fonts** (Project Settings → Fonts, or Google Fonts integration):
- `Sora` — headings (weights 600/700/800)
- `Inter` — body (400/500/600/700)
- `IBM Plex Mono` — labels, codes, metrics (400/500/600)

**Color swatches** (Style Manager → create these as global swatches):

| Swatch | Hex | Use |
|---|---|---|
| Navy 900 | `#060A17` | Page base / darkest sections |
| Navy 800 | `#0A1124` | Hero / command-center background |
| Navy 700 | `#0F1A33` | Panels, cards on dark |
| Blue 500 | `#2D6CF6` | Primary SecureVisa blue (CTAs, accents) |
| Blue 600 | `#1E4FD0` | Button gradient bottom |
| Cyan | `#3FC6D9` | Muted accent (gauges, checks, active states) |
| Paper | `#F5F7FB` | Light section background (Industries) |
| Ink 900 | `#0B1426` | Dark text on light |
| Text 300 | `#B7C2D8` | Body text on dark |

**Page settings → Open Graph & SEO:** copy the `<title>`, meta description, and
canonical from `index.html`. Set the favicon and a social share image.

**Container:** create a `container-large` class (max-width `1200px`, auto side
margins, `24px` horizontal padding) and reuse it inside every section. In Webflow,
build each block as **Section → `container-large` → content grid**.

---

## 2. Page structure (sections, top to bottom)

| # | Webflow Section (class) | Purpose | Key components |
|---|---|---|---|
| — | `navbar` | Sticky nav | Dropdown menus, CTA buttons, mobile burger |
| 1 | `section_home-hero` | Hero — Regulatory Command Center | `home-hero_grid` (copy + `compliance-dashboard`) |
| — | `section_strip` | Regulator coverage strip | Inline regulator list |
| 2 | `section_regulators` | Regulator Coverage Matrix | `reg_tabs` → `regulator-card` panels |
| 3 | `section_ecosystem` | Compliance Ecosystem | `eco_diagram` core + nodes |
| 4 | `section_industries` | Industry Pathways (light) | `ind_grid` → `ind_card` |
| 5 | `section_process` | Licensing Journey | `process_timeline` → `proc_step` |
| 6 | `section_why` | Why SecureVisa | `why_grid` + `why_list` |
| 7 | `section_case-proof` | Project-type outcomes | `case_grid` → `case_card` |
| 8 | `section_ebook` | eBook lead magnet | `ebook_grid` (copy + document mockup) |
| — | `section_faq` | FAQ accordion | `faq_item` (`<details>`) |
| 9 | `section_final-cta` | Final consultation CTA | `final_panel` |
| — | `footer_component` | Footer | `footer_top`, `footer_links`, `footer_bottom` |

Use **one H1 only** (in the hero). Every other section title is an **H2**, matching
the required SEO headings:
*UAE Regulatory Authorities We Cover · SecureVisa Group Compliance Ecosystem ·
Licensing Pathways for Regulated Industries · From Business Model to Regulator
Approval · Why SecureVisa Group · Speak with a SecureVisa Compliance Expert.*

---

## 3. Signature component — the "Regulatory Command Center" (`compliance-dashboard`)

This is the bespoke hero visual and the main thing that makes the page feel like a
regulatory-tech product rather than a SaaS template. Rebuild it as a **Div Block
stack** (no images, so it stays crisp and editable):

```
compliance-dashboard
├─ dash_head        → title + live status dot + mono "SYS · LIVE"
└─ dash_body
   ├─ dash_panel  "Regulator status"   → dash_reg-grid (6 regulator chips)
   ├─ dash_split
   │   ├─ dash_panel.dash_gauge  → SVG ring gauge (Audit readiness 92%)
   │   └─ dash_panel.dash_path   → license pathway steps + progress bar
   ├─ dash_split
   │   ├─ dash_panel  "AML / KYC controls"  → toggle rows
   │   └─ dash_panel  "Cybersecurity"        → ITSEC assurance row
   └─ dash_panel "Evidence vault"            → document checklist
```

- The **gauge** is an inline SVG with two `<circle>`s. In Webflow, add it via an
  **Embed** element (copy the `<svg>` block from `index.html`). The fill animation
  is driven by `stroke-dashoffset` in `script.js`.
- Keep the **monospace labels** (IBM Plex Mono) — they carry the "audit/command
  center" credibility.
- **Accessibility:** the dashboard has a full `aria-label` describing its contents
  (it's decorative-but-informative). Preserve this in Webflow's element settings.

---

## 4. Regulator matrix tabs (`reg_tabs`)

Use Webflow's native **Tabs** component:
- **Tabs Menu** → 6 Tab Links styled as `reg_tab` (VARA, SCA, DFSA, ADGM, GCGRA, CBUAE).
- **Tabs Content** → 6 Tab Panes, each containing a `regulator-card`
  (`reg_card-main` + `reg_card-side`).
- Content per regulator (mandate, who it applies to, what SecureVisa supports) is in
  `index.html` and should ideally come from a **CMS Collection** (see §7).

If you prefer to keep the custom roving-keyboard behaviour from `script.js`, use the
embed approach instead of native Tabs. Native Tabs are simpler and CMS-friendly.

---

## 5. Interactions

| Interaction | Rebuild in Webflow with… |
|---|---|
| Sticky navbar darkens on scroll | IX2: **While page scrolls** → change `navbar` background opacity, OR keep the tiny `is-scrolled` class toggle from `script.js`. |
| Card hover elevation (industries, eco, process, case) | IX2: **Hover** → move `translateY(-4px)`, raise shadow. Already in CSS `:hover`. |
| Tab switching | Native Tabs (no code). |
| FAQ single-open accordion | Native Webflow accordion (Dropdown/IX2) **or** keep the `<details>` + `data-faq` embed for SEO-clean markup. |
| Gauge fill + count-up + progress bars | **Custom code** — keep the `IntersectionObserver` block from `script.js`. Paste `script.js` (or just that block) into Project Settings → Footer Code. |
| Mobile menu | Native Webflow navbar menu; the prototype's burger logic is only for the static file. |
| Smooth anchor scrolling | Native (CSS `scroll-behavior: smooth`). |

**Motion discipline:** all transitions are 150–350ms and `prefers-reduced-motion`
is respected (`script.js` checks it; CSS has a reduced-motion block). Don't add
parallax, blob morphs, or autoplay — this is a regulated brand.

---

## 6. CTA flow (preserve exactly)

- **Primary:** Book a Regulatory Call → links to phone / booking (`tel:+97142572406`).
- **WhatsApp:** Talk to an Expert → `https://wa.me/971585179303` (set `rel="nofollow"`).
- **Download eBook** → `#ebook` / gated form.
- **Contact Us Now** → final CTA section.
- Floating **WhatsApp FAB** bottom-right (`whatsapp-fab`).

In Webflow, wire **Book a Regulatory Call** to your scheduler (Calendly/HubSpot
embed) and **Download eBook** to a Webflow **Form** that gates the PDF.

---

## 7. Recommended CMS Collections

Make the page maintainable and SEO-scalable by driving repeated blocks from CMS:

**Collection: Regulators** (powers `section_regulators` + nav + footer)
- Name (VARA), Full name, Slug, Short tag (e.g. "Virtual assets")
- Summary (rich text), Activities (multi-line / list), "SecureVisa supports" (list)
- → Each regulator also gets its own CMS **Template page** for internal linking
  (e.g. `/regulators/vara`). Link the hero dashboard chips and footer to these.

**Collection: Industries** (powers `section_industries` + nav)
- Name, Who it's for, Main regulator(s), Core requirements, Pathway CTA link
- → Template page per industry (`/industries/crypto-web3-licensing`, etc.).

**Collection: Process Steps** (powers `section_process`)
- Number, Title, Description, Order.

**Collection: Case Examples** (powers `section_case-proof`)
- Type label, Title, Description, Tags, **"Anonymized example" boolean** so the
  disclaimer label is enforced by content, never accidentally dropped.

**Collection: FAQs** (powers `section_faq` + FAQPage schema)
- Question, Answer (rich text), Order. Bind these to the on-page accordion AND to
  the FAQ JSON-LD so structured data stays in sync.

**Collection: Blog / Resources** — standard.

Internal linking: regulator pages ↔ industry pages ↔ relevant FAQs. This is the SEO
backbone (topic clusters around VARA/crypto/fintech/tokenization/forex/gaming).

---

## 8. SEO checklist (carry into Webflow)

- ✅ One `H1`; clean `H2`/`H3` hierarchy (already structured).
- ✅ Meta title & description (in `<head>` of `index.html`).
- ✅ **Structured data** — 4 JSON-LD blocks included: `Organization`/`LocalBusiness`,
  `Service`, `BreadcrumbList`, `FAQPage`. Paste these into each page's Custom Code,
  or generate the FAQ/Service ones from CMS. Validate with Google Rich Results Test.
- ✅ Descriptive `alt` / `aria-label` on the dashboard and all visuals.
- ✅ Canonical URL set.
- ✅ Mobile-first responsive (breakpoints at 1024 / 860 / 620px).
- ✅ Sticky, lightweight navbar.
- ✅ Fast CSS (single stylesheet, system-friendly fonts, no heavy images).
- Add `sitemap.xml` + `robots.txt` (Webflow auto-generates), and set per-page OG images.
- Keyword usage is natural and woven into headings/body/FAQ — **do not** keyword-stuff.

---

## 9. Compliance copywriting rules (built into the copy — keep them)

The prototype already follows these; preserve them in all future edits:

- SecureVisa is described as a **private corporate service provider**, *not* a
  government authority or regulator (see footer disclaimer).
- **No guaranteed approval.** Copy uses "supports licensing applications", "helps
  prepare regulator-ready documentation", "guides businesses through UAE regulatory
  pathways", "builds audit-ready compliance frameworks".
- **No "official partner"** claims for any regulator.
- Case studies are labelled **"Anonymized example / project-type"** — no invented
  client names or testimonials.
- Partner ecosystem (ITSEC, VerifiX, CompliX) is referenced as supporting capability,
  not as a regulatory endorsement.

---

## 10. Quick rebuild order (suggested)

1. Set fonts, swatches, `container-large`, base body styles.
2. Build `navbar` + dropdowns + mobile menu + `footer_component` (global, reusable).
3. Build the hero `compliance-dashboard` (the showpiece) — get this right first.
4. Add CMS Collections (Regulators, Industries, FAQs, Case Examples, Process Steps).
5. Build remaining sections top-to-bottom, binding to CMS where noted.
6. Add Interactions (IX2) + paste the custom-code block for the gauge/progress.
7. Wire CTAs (scheduler, WhatsApp, eBook form).
8. Add JSON-LD, finalise SEO settings, test responsive + Rich Results.

---

*Files: `index.html` (structure + content + schema), `styles.css` (design system +
components), `script.js` (tabs, accordion, mobile menu, animated metrics).*
