#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SecureVisa Group — static multi-page site generator.
Emits branded HTML pages at the repo root with a shared header/footer.
Run:  python3 build_site.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
WA = "https://wa.me/971585179303"
TEL = "+97142572406"

# --------------------------------------------------------------------------
# Navigation model (label -> file). Dropdowns render real page links.
# --------------------------------------------------------------------------
REGULATORS = [
    ("vara",  "VARA",  "Virtual Asset Regulatory Authority"),
    ("sca",   "SCA",   "Securities & Commodities Authority"),
    ("dfsa",  "DFSA",  "Dubai Financial Services Authority"),
    ("adgm",  "ADGM",  "Abu Dhabi Global Market"),
    ("gcgra", "GCGRA", "General Commercial Gaming Regulatory Authority"),
    ("cbuae", "CBUAE", "Central Bank of the UAE"),
]
SERVICES = [
    ("nexus.html", "NEXUS Compliance Platform"),
    ("ecosystem.html", "Ecosystem"),
    ("ecosystem.html#vara", "VARA Ecosystem"),
    ("ecosystem.html#sca", "SCA Ecosystem"),
    ("real-estate-tokenization.html", "Real Estate Tokenization"),
    ("fintech-licensing.html", "FinTech"),
    ("forex-licensing.html", "Forex Exchange"),
    ("crypto-web3-licensing.html", "Crypto & Web3"),
    ("gaming-nft.html", "Gaming | NFT"),
]
INDUSTRIES_NAV = [
    ("crypto-web3-licensing.html", "Crypto & Web3 Licensing"),
    ("fintech-licensing.html", "FinTech Licensing"),
    ("tokenization-rwa.html", "Tokenization & RWA"),
    ("forex-licensing.html", "Forex Licensing"),
    ("web3-defi-licensing.html", "Web3 & DeFi Licensing"),
    ("real-estate-tokenization.html", "Real Estate Tokenization"),
]
RESOURCES = [
    ("about.html", "About Us"),
    ("blog.html", "Blog"),
    ("case-studies.html", "Case Studies"),
    ("partners.html", "Partners"),
]

WA_SVG = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" '
          'd="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.2-.7-2.7-1.1-4.4-3.8-4.5-4-.1-.2-1.1-1.4-1.1-2.7 0-1.3.7-1.9.9-2.2.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2 0 .4 0 .5l-.4.5c-.2.2-.3.4-.1.7.2.3.9 1.4 1.9 2 .8.5 1.1.6 1.4.4l.6-.7c.2-.2.4-.2.6-.1l1.8.9c.2.1.4.2.4.3.1.2.1.7-.1 1.3Z"/></svg>')


def media_backdrop(src, opacity="0.16", parallax=False):
    """Decorative low-opacity photographic wash behind a section, with a
    navy gradient scrim on top so foreground text always stays readable."""
    px = " data-parallax" if parallax else ""
    return (f'<div class="media-backdrop" aria-hidden="true"{px} style="--bg-op:{opacity}">'
            f'<img src="{src}" alt="" loading="lazy" decoding="async" /></div>')


def head(title, desc, canonical_path, breadcrumb=None):
    bc = ""
    if breadcrumb:
        items = [{"@type": "ListItem", "position": i + 1, "name": n,
                  "item": "https://www.securevisanow.com/" + (h if h != "index.html" else "")}
                 for i, (h, n) in enumerate(breadcrumb)]
        bc = ('\n  <script type="application/ld+json">'
              + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                            "itemListElement": items}) + "</script>")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#070A14" />
  <link rel="icon" type="image/png" href="assets/favicon.png" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <link rel="canonical" href="https://www.securevisanow.com/{canonical_path}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="SecureVisa Group" />
  <meta property="og:title" content="{html.escape(title)}" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css" />{bc}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""


def header(active=""):
    def cur(key):
        return " is-current" if key == active else ""
    reg_links = "\n".join(
        f'              <a href="{k}.html" role="menuitem"><strong>{c}</strong><span>{html.escape(n)}</span></a>'
        for k, c, n in REGULATORS)
    svc_links = "\n".join(
        f'              <a href="{h}" role="menuitem">{html.escape(n)}</a>' for h, n in SERVICES)
    ind_links = "\n".join(
        f'              <a href="{h}" role="menuitem">{html.escape(n)}</a>' for h, n in INDUSTRIES_NAV)
    res_links = "\n".join(
        f'              <a href="{h}" role="menuitem">{html.escape(n)}</a>' for h, n in RESOURCES)

    m_reg = "\n".join(f'      <a href="{k}.html">{c} — {html.escape(n)}</a>' for k, c, n in REGULATORS)
    m_svc = "\n".join(f'      <a href="{h}">{html.escape(n)}</a>' for h, n in SERVICES)
    m_ind = "\n".join(f'      <a href="{h}">{html.escape(n)}</a>' for h, n in INDUSTRIES_NAV)
    m_res = "\n".join(f'      <a href="{h}">{html.escape(n)}</a>' for h, n in RESOURCES)

    return f"""<header class="navbar" id="navbar" data-nav>
  <div class="container-large navbar_inner">
    <a class="navbar_brand" href="index.html" aria-label="SecureVisa Group home">
      <img src="assets/logo-white.png" alt="SecureVisa Group — UAE licensing and compliance" />
    </a>
    <nav class="navbar_menu" aria-label="Primary">
      <ul class="navbar_list">
        <li class="navbar_item has-dropdown">
          <a class="navbar_link{cur('regulators')}" href="regulators.html" aria-haspopup="true">Regulators <span class="chev" aria-hidden="true"></span></a>
          <div class="dropdown" role="menu"><div class="dropdown_grid">
{reg_links}
          </div></div>
        </li>
        <li class="navbar_item has-dropdown">
          <a class="navbar_link{cur('services')}" href="services.html" aria-haspopup="true">Services <span class="chev" aria-hidden="true"></span></a>
          <div class="dropdown" role="menu"><div class="dropdown_col">
{svc_links}
          </div></div>
        </li>
        <li class="navbar_item has-dropdown">
          <a class="navbar_link{cur('industries')}" href="industries.html" aria-haspopup="true">Industries <span class="chev" aria-hidden="true"></span></a>
          <div class="dropdown" role="menu"><div class="dropdown_col">
{ind_links}
          </div></div>
        </li>
        <li class="navbar_item">
          <a class="navbar_link navbar_link--platform{cur('nexus')}" href="nexus.html">NEXUS <span class="navbar_tag">Platform</span></a>
        </li>
        <li class="navbar_item has-dropdown">
          <a class="navbar_link{cur('resources')}" href="about.html" aria-haspopup="true">Resources <span class="chev" aria-hidden="true"></span></a>
          <div class="dropdown" role="menu"><div class="dropdown_col">
{res_links}
          </div></div>
        </li>
      </ul>
    </nav>
    <div class="navbar_actions">
      <a class="btn btn-ghost btn-sm" href="ebook.html">Download eBook</a>
      <a class="btn btn-primary btn-sm" href="contact.html">Contact Us Now</a>
    </div>
    <button class="navbar_burger" aria-label="Open menu" aria-expanded="false" data-burger><span></span><span></span><span></span></button>
  </div>
</header>

<div class="mobile-menu" data-mobile-menu hidden>
  <nav aria-label="Mobile">
    <a class="mobile-menu_feature" href="nexus.html">NEXUS — Compliance Platform</a>
    <details><summary>Regulators</summary>
{m_reg}
    </details>
    <details><summary>Services</summary>
{m_svc}
    </details>
    <details><summary>Industries</summary>
{m_ind}
    </details>
    <details><summary>Resources</summary>
{m_res}
    </details>
    <div class="mobile-menu_cta">
      <a class="btn btn-primary" href="contact.html">Book a Regulatory Call</a>
      <a class="btn btn-whatsapp" href="{WA}">WhatsApp / Talk to an Expert</a>
    </div>
  </nav>
</div>
"""


def footer():
    reg = "\n".join(f'          <a href="{k}.html">{c}</a>' for k, c, n in REGULATORS)
    svc = "\n".join(f'          <a href="{h}">{html.escape(n)}</a>' for h, n in SERVICES)
    ind = "\n".join(f'          <a href="{h}">{html.escape(n)}</a>' for h, n in INDUSTRIES_NAV)
    res = "\n".join(f'          <a href="{h}">{html.escape(n)}</a>' for h, n in RESOURCES)
    return f"""<footer class="footer_component">
  <div class="container-large">
    <div class="footer_top">
      <div class="footer_brand">
        <a href="index.html" aria-label="SecureVisa Group home"><img src="assets/logo-white.png" alt="SecureVisa Group" /></a>
        <p class="footer_tagline">Your trusted partner for regulatory compliance &amp; licensing in the UAE.</p>
        <ul class="footer_contact">
          <li><span>Phone</span><a href="tel:{TEL}">+971.4.257.2406</a></li>
          <li><span>WhatsApp</span><a href="{WA}" rel="nofollow">+971.58.517.9303</a></li>
          <li><span>Email</span><a href="mailto:hello@securevisanow.com">hello@securevisanow.com</a></li>
          <li><span>Address</span><address>Onyx Tower 1, The Greens, Dubai</address></li>
        </ul>
      </div>
      <nav class="footer_links" aria-label="Footer">
        <div class="footer_col"><h3>Regulators</h3>
{reg}
        </div>
        <div class="footer_col"><h3>Services</h3>
{svc}
        </div>
        <div class="footer_col"><h3>Industries</h3>
{ind}
        </div>
        <div class="footer_col"><h3>Resources</h3>
{res}
        </div>
      </nav>
    </div>
    <div class="footer_bottom">
      <p class="footer_copy">© 2023–2026 SVG Corporate Service Provider LLC | DED: 1217108</p>
      <nav class="footer_legal" aria-label="Legal">
        <a href="#">Terms &amp; Conditions</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Legal Disclaimer</a>
      </nav>
    </div>
    <p class="footer_disclaimer">SecureVisa Group is a private corporate service provider and is not a government authority or regulator. SecureVisa supports licensing applications and compliance preparation; it does not guarantee regulatory approval.</p>
  </div>
</footer>

<a class="whatsapp-fab" href="{WA}" rel="nofollow" aria-label="Chat with SecureVisa on WhatsApp">{WA_SVG}</a>
<script src="script.js"></script>
</body>
</html>
"""


def final_cta():
    return f"""<section class="section_final-cta" id="final-cta">
  <div class="container-large"><div class="final_panel">
    {media_backdrop("assets/media/data-flow.jpg", opacity="0.18")}
    <div class="final_grid" aria-hidden="true"></div>
    <div class="final_content" data-reveal>
      <span class="eyebrow eyebrow--light">Confidential consultation</span>
      <h2>Speak with a SecureVisa Compliance Expert</h2>
      <p>Share your licensing or compliance goals in a confidential session. SecureVisa will outline regulator requirements, expected documentation, timeline considerations, and next steps.</p>
      <div class="final_actions">
        <a class="btn btn-primary btn-lg" href="tel:{TEL}">Book a Regulatory Call</a>
        <a class="btn btn-whatsapp btn-lg" href="{WA}" rel="nofollow">WhatsApp SecureVisa Support</a>
      </div>
      <p class="final_trust">Same-day response · UAE hours · Confidential consultation · No spam</p>
    </div>
  </div></div>
</section>"""


def subhero(pill, h1, sub, crumb, stats, primary=("contact.html", "Book a Regulatory Call"),
            bg="assets/media/dubai-skyline.jpg"):
    crumb_html = " / ".join(
        (f'<a href="{h}">{html.escape(n)}</a>' if h else f'<span>{html.escape(n)}</span>')
        for h, n in crumb)
    stat_html = "\n".join(
        f'        <div class="subhero_stat" data-reveal><strong>{html.escape(s)}</strong><span>{html.escape(l)}</span></div>'
        for s, l in stats)
    return f"""<section class="section_subhero">
  {media_backdrop(bg, opacity="0.20", parallax=True)}
  <div class="container-large">
    <p class="breadcrumb">{crumb_html}</p>
    <div class="subhero_grid">
      <div class="subhero" data-reveal>
        <span class="subhero_pill">{html.escape(pill)}</span>
        <h1>{h1}</h1>
        <p>{html.escape(sub)}</p>
        <div class="subhero_actions">
          <a class="btn btn-primary btn-lg" href="{primary[0]}">{primary[1]}</a>
          <a class="btn btn-whatsapp btn-lg" href="{WA}" rel="nofollow">Talk to an Expert</a>
        </div>
      </div>
      <div class="subhero_aside">
{stat_html}
      </div>
    </div>
  </div>
</section>"""


def write(filename, title, desc, body, active="", breadcrumb=None):
    canonical = "" if filename == "index.html" else filename
    out = head(title, desc, canonical, breadcrumb) + header(active) + \
        '<main id="main">\n' + body + '\n</main>\n' + footer()
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(out)
    return filename


# ==========================================================================
# CONTENT DATA
# ==========================================================================
REG_DATA = {
    "vara": dict(
        full="Virtual Asset Regulatory Authority", tag="Virtual assets",
        blurb="Dubai's dedicated virtual assets regulator and the authority for VASPs operating in mainland Dubai, covering the full lifecycle of regulated virtual asset activity.",
        activities=["VASPs", "Crypto exchanges", "Broker-dealers", "Custody", "Lending & borrowing", "Token issuance", "Advisory"],
        supports=["Activity classification & regulator mapping", "Regulator-ready VARA application dossier", "AML/CFT & Travel Rule framework", "Cybersecurity controls baseline", "Market conduct & risk policies"],
        stats=[("VASP", "Primary activity class"), ("Dubai", "Mainland jurisdiction")],
        long="VARA regulates virtual asset activities across Dubai (excluding the DIFC financial free zone). Most crypto and Web3 operators serving the mainland market require authorisation for one or more VARA activities, each with its own rulebook covering conduct, technology, market integrity, and compliance.",
    ),
    "sca": dict(
        full="Securities & Commodities Authority", tag="Securities & tokenized assets",
        blurb="The federal regulator for capital-markets activity in the UAE, including the growing area of tokenized assets and investment services.",
        activities=["Securities", "Commodities", "Tokenized assets", "Brokerage", "Investment advisory", "Fund management"],
        supports=["SCA licensing for tokenized assets", "Brokerage & advisory readiness", "Governance & risk documentation", "Disclosure & investor-protection materials", "Ongoing reporting frameworks"],
        stats=[("Federal", "UAE-wide mandate"), ("RWA", "Tokenized assets")],
        long="The SCA oversees the UAE's securities and commodities markets at the federal level. As real-world-asset tokenization grows, the SCA framework is central to projects structuring tokenized securities, funds, and investment products outside the financial free zones.",
    ),
    "dfsa": dict(
        full="Dubai Financial Services Authority", tag="DIFC financial services",
        blurb="The independent regulator of financial services conducted in or from the Dubai International Financial Centre (DIFC) free zone.",
        activities=["DIFC financial services", "Asset management", "FinTech", "Investment tokens", "Regulated financial activity"],
        supports=["DIFC pathway assessment", "Regulatory business plan preparation", "Compliance & risk policy suite", "Fit-and-proper documentation", "Innovation Testing Licence guidance"],
        stats=[("DIFC", "Financial free zone"), ("Common law", "Independent regime")],
        long="The DFSA operates the common-law regulatory regime of the DIFC. Firms that base regulated financial activity in the DIFC — including asset managers, advisors, and fintech innovators — apply to the DFSA and must meet its prudential and conduct standards.",
    ),
    "adgm": dict(
        full="Abu Dhabi Global Market · FSRA", tag="Abu Dhabi financial services",
        blurb="Abu Dhabi's international financial centre and its Financial Services Regulatory Authority (FSRA), covering virtual assets, funds, and fintech.",
        activities=["Financial services", "Virtual assets", "Funds", "FinTech", "Multilateral trading"],
        supports=["FSRA pathway mapping", "Virtual asset & fund readiness", "Compliance gap analysis", "Cybersecurity & AML alignment", "Regulatory engagement support"],
        stats=[("ADGM", "Abu Dhabi free zone"), ("FSRA", "Regulator")],
        long="ADGM is Abu Dhabi's financial free zone, regulated by the FSRA under a common-law framework. The FSRA was an early mover on virtual asset regulation and remains a leading pathway for funds, fintech, and digital-asset businesses in the UAE.",
    ),
    "gcgra": dict(
        full="General Commercial Gaming Regulatory Authority", tag="Commercial gaming",
        blurb="The UAE federal authority for regulated commercial gaming, lottery, and internet gaming activity.",
        activities=["Gaming", "Lottery", "Internet gaming", "Commercial gaming compliance", "Responsible gaming"],
        supports=["Activity & eligibility assessment", "Responsible-gaming controls", "AML/KYC framework design", "Integrity & player-protection documentation", "Governance & reporting"],
        stats=[("Federal", "National framework"), ("New", "Emerging regime")],
        long="The GCGRA establishes a national regulatory framework for commercial gaming in the UAE. Operators entering this emerging market must demonstrate strong responsible-gaming, integrity, and anti-money-laundering controls as part of licensing.",
    ),
    "cbuae": dict(
        full="Central Bank of the UAE", tag="Banking & payments",
        blurb="The UAE's central bank, regulating banking, payments, stored value, and related financial infrastructure.",
        activities=["Banking", "Payment services", "Stored value", "Stablecoins", "Exchange", "Remittance"],
        supports=["Payment services pathway", "Stored-value & remittance readiness", "AML/CFT & risk frameworks", "Operational & cyber controls", "Safeguarding arrangements"],
        stats=[("CBUAE", "National regulator"), ("Payments", "Core mandate")],
        long="The CBUAE regulates the UAE's banking and payments system, including retail payment services, stored value facilities, and the dirham-backed payment token framework. Payments, remittance, and stablecoin businesses generally fall within its remit.",
    ),
}
REG_ORDER = ["vara", "sca", "dfsa", "adgm", "gcgra", "cbuae"]
REG_NAMES = {k: c for k, c, n in REGULATORS}

IND_DATA = {
    "crypto-web3-licensing": dict(
        name="Crypto & Web3 Licensing", pill="Industry pathway",
        who="Exchanges, VASPs, custodians, brokers, and token issuers.",
        reg="VARA · ADGM (FSRA) · DFSA",
        reqs="AML/CFT, Travel Rule, custody and key-management controls, market conduct, and cybersecurity.",
        intro="Crypto and Web3 businesses face some of the most detailed licensing expectations in the UAE. SecureVisa helps classify your activities, select the right regulator, and prepare a regulator-ready application supported by a defensible compliance and cybersecurity framework.",
        bullets=["Map token, exchange, custody, and brokerage activities to the correct authority", "Design AML/CFT and Travel Rule controls for virtual assets", "Prepare custody, key-management, and operational resilience documentation", "Build a regulator-aligned cybersecurity framework with ITSEC"],
        regs=["vara", "adgm", "dfsa"],
    ),
    "fintech-licensing": dict(
        name="FinTech & Payments Licensing", pill="Industry pathway",
        who="Payment providers, wallets, and stored-value platforms.",
        reg="CBUAE · DFSA · ADGM",
        reqs="Safeguarding, AML/KYC, governance, and operational resilience.",
        intro="FinTech and payments businesses must align to the right UAE regime — federal (CBUAE) or financial free zone (DFSA, FSRA). SecureVisa helps determine the pathway and prepare the safeguarding, governance, and AML documentation regulators expect.",
        bullets=["Determine CBUAE vs DIFC/ADGM pathway for your activity", "Prepare safeguarding and client-money arrangements", "Design KYC/KYB onboarding and monitoring", "Document governance and operational resilience"],
        regs=["cbuae", "dfsa", "adgm"],
    ),
    "tokenization-rwa": dict(
        name="Tokenization & RWA", pill="Industry pathway",
        who="Real-world-asset and tokenized investment platforms.",
        reg="SCA · ADGM · DFSA",
        reqs="Asset structuring, disclosures, investor protection, and custody.",
        intro="Tokenizing real-world assets sits at the intersection of capital-markets and virtual-asset regulation. SecureVisa helps structure the offering, identify the governing regime, and prepare disclosures and investor-protection materials.",
        bullets=["Classify the token and its underlying asset", "Map to SCA or financial-free-zone frameworks", "Prepare disclosure and offering documentation", "Address custody and investor-protection requirements"],
        regs=["sca", "adgm", "dfsa"],
    ),
    "forex-licensing": dict(
        name="Forex & Brokerage Licensing", pill="Industry pathway",
        who="Forex, CFD, and brokerage operators.",
        reg="SCA · DFSA · ADGM",
        reqs="Capital adequacy, client money, conduct, and AML/KYC.",
        intro="Forex and brokerage operators must satisfy conduct, capital, and client-money standards. SecureVisa helps map the jurisdiction and prepare the prudential and compliance documentation required for a credible application.",
        bullets=["Select the appropriate UAE jurisdiction and licence", "Prepare capital adequacy and client-money arrangements", "Design conduct and best-execution policies", "Build AML/KYC and risk frameworks"],
        regs=["sca", "dfsa", "adgm"],
    ),
    "web3-defi-licensing": dict(
        name="Web3 & DeFi Licensing", pill="Industry pathway",
        who="Web3 protocols, DeFi front-ends, and infrastructure providers.",
        reg="VARA · ADGM (FSRA)",
        reqs="Activity analysis, AML/CFT, governance, and cybersecurity.",
        intro="Web3 and DeFi business models require careful analysis of which activities are regulated and where. SecureVisa helps interpret your model against UAE frameworks and prepare a compliance and governance position that stands up to scrutiny.",
        bullets=["Analyse which on-chain activities are regulated", "Map to VARA or FSRA where applicable", "Design AML/CFT controls for decentralised models", "Document governance, risk, and cybersecurity"],
        regs=["vara", "adgm"],
    ),
    "real-estate-tokenization": dict(
        name="Real Estate Tokenization", pill="Industry pathway",
        who="Property tokenization and fractional-ownership platforms.",
        reg="SCA · VARA · DFSA",
        reqs="Asset backing, disclosures, custody, and investor safeguards.",
        intro="Real estate tokenization combines property, securities, and virtual-asset considerations. SecureVisa helps structure compliant fractional-ownership models and prepare the disclosures and safeguards regulators and investors expect.",
        bullets=["Structure the token against the underlying property", "Identify the governing UAE framework", "Prepare disclosures and investor safeguards", "Address custody and transfer-agent functions"],
        regs=["sca", "vara", "dfsa"],
    ),
    "gaming-nft": dict(
        name="Gaming | NFT", pill="Industry pathway",
        who="Commercial & internet gaming and NFT platforms.",
        reg="GCGRA · VARA",
        reqs="Responsible gaming, AML/KYC, and integrity controls.",
        intro="Gaming and NFT platforms must address responsible-gaming, integrity, and anti-money-laundering expectations. SecureVisa helps assess eligibility and prepare the controls and documentation required for this emerging UAE regime.",
        bullets=["Assess activity and eligibility under GCGRA", "Design responsible-gaming and player-protection controls", "Build AML/KYC frameworks", "Address NFT and virtual-asset overlaps with VARA"],
        regs=["gcgra", "vara"],
    ),
}

PROCESS = [
    ("01", "Business Model Assessment", "We examine your activities, jurisdiction, and structure to define what is actually being regulated."),
    ("02", "Regulator Mapping", "Your model is mapped to the correct UAE authority — VARA, SCA, DFSA, ADGM, GCGRA, or CBUAE."),
    ("03", "Compliance Gap Analysis", "We benchmark current readiness against regulator expectations and prioritise the gaps that matter."),
    ("04", "Application Dossier & Policies", "We help prepare audit-ready documentation: business plan, governance, AML/CFT, and risk policies."),
    ("05", "Submission & Regulator Response", "We support the submission and help respond to regulator queries with clear, consistent evidence."),
    ("06", "Cybersecurity, AML/KYC & Ongoing Supervision", "Post-license, we support security controls, monitoring, reporting, and ongoing obligations."),
]

FAQS = [
    ("Which UAE regulator do I need for a crypto or Web3 business?", "It depends on your activity and location. Virtual asset services in mainland Dubai are typically regulated by VARA, while ADGM (FSRA) and DIFC (DFSA) regulate virtual assets within their financial free zones. SecureVisa helps map your business model to the correct regulator before you apply."),
    ("What is a VARA license in Dubai?", "A VARA license authorises regulated virtual asset activities — such as exchange, broker-dealer, custody, lending, and advisory services — under the Dubai Virtual Assets Regulatory Authority. SecureVisa supports applicants in preparing regulator-ready documentation for the relevant VARA activity."),
    ("Does a fintech company need SCA, DFSA, ADGM, or CBUAE approval?", "It depends on the activity. Payments, stored value, and remittance generally fall under CBUAE; capital-markets and tokenized-asset activity under SCA; and financial services inside the free zones under DFSA (DIFC) or FSRA (ADGM). SecureVisa helps determine the right pathway."),
    ("What documents are required for UAE regulatory licensing?", "Requirements vary by regulator and activity but commonly include a business plan, governance and ownership structure, AML/CFT policies, risk and compliance frameworks, fit-and-proper documentation, and cybersecurity controls. SecureVisa helps prepare an audit-ready application dossier."),
    ("How does cybersecurity affect licensing approval?", "UAE regulators increasingly expect demonstrable cybersecurity governance, controls, and incident-response capability. SecureVisa, supported by ITSEC, helps build a regulator-ready cybersecurity framework aligned to licensing expectations."),
    ("What is AML/KYC compliance for regulated UAE businesses?", "AML/KYC compliance covers customer due diligence, sanctions and PEP screening, transaction monitoring, suspicious-activity reporting, and — for virtual assets — Travel Rule obligations. SecureVisa helps design and document an AML/CFT framework suited to your activity."),
    ("Can SecureVisa support both licensing and post-license compliance?", "Yes. SecureVisa supports pre-license preparation and ongoing post-license obligations, including governance, reporting, AML/KYC operations, and cybersecurity supervision."),
    ("How do I start a SecureVisa consultation?", "Book a confidential regulatory call or message the team on WhatsApp. SecureVisa will outline likely regulator requirements, expected documentation, and timeline considerations for your business model."),
]


def faq_block(items, heading="UAE Licensing & Compliance FAQs"):
    rows = "\n".join(
        f'        <details class="faq_item"><summary>{html.escape(q)}<span class="faq_icon" aria-hidden="true"></span></summary><div class="faq_a"><p>{html.escape(a)}</p></div></details>'
        for q, a in items)
    return f"""<section class="section_faq" id="faq">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Questions, answered</span><h2>{html.escape(heading)}</h2></header>
    <div class="faq_list" data-faq>
{rows}
    </div>
  </div>
</section>"""


# ==========================================================================
# PAGE BODIES
# ==========================================================================
def command_center(reveal=False):
    """The live 'Regulatory Command Center' mockup. Shared by the home hero and
    the NEXUS platform page so the product visual stays consistent."""
    rv = " data-reveal" if reveal else ""
    return f"""<div class="compliance-dashboard"{rv} role="img" aria-label="Regulatory Command Center showing regulator status for VARA, SCA, DFSA, ADGM, GCGRA and CBUAE, license pathway progress, an audit readiness score of 92 percent, AML and KYC controls, cybersecurity assurance by ITSEC, and an evidence vault documentation checklist.">
      <div class="dash_head"><div class="dash_title"><span class="dash_dot live"></span><span>Regulatory Command Center</span></div><span class="dash_mono">SYS · LIVE</span></div>
      <div class="dash_body">
        <div class="dash_panel">
          <div class="dash_panel-head"><span>Regulator status</span><span class="dash_mono">6 / 6 mapped</span></div>
          <ul class="dash_reg-grid">
            <li><span class="rg_code">VARA</span><span class="rg_state ok">Active</span></li>
            <li><span class="rg_code">SCA</span><span class="rg_state ok">Mapped</span></li>
            <li><span class="rg_code">DFSA</span><span class="rg_state ok">Mapped</span></li>
            <li><span class="rg_code">ADGM</span><span class="rg_state warn">In review</span></li>
            <li><span class="rg_code">GCGRA</span><span class="rg_state ok">Mapped</span></li>
            <li><span class="rg_code">CBUAE</span><span class="rg_state ok">Mapped</span></li>
          </ul>
        </div>
        <div class="dash_split">
          <div class="dash_panel dash_gauge">
            <div class="dash_panel-head"><span>Audit readiness</span></div>
            <div class="gauge" data-gauge="92" aria-hidden="true">
              <svg viewBox="0 0 120 120" width="118" height="118"><circle cx="60" cy="60" r="50" class="gauge_track"/><circle cx="60" cy="60" r="50" class="gauge_value" data-gauge-ring/></svg>
              <div class="gauge_num"><strong data-count="92">0</strong><span>%</span></div>
            </div>
          </div>
          <div class="dash_panel dash_path">
            <div class="dash_panel-head"><span>License pathway</span><span class="dash_mono">VARA · VASP</span></div>
            <ol class="path_steps">
              <li class="done"><span></span>Business model assessment</li>
              <li class="done"><span></span>Regulator mapping</li>
              <li class="active"><span></span>Compliance gap analysis</li>
              <li><span></span>Application dossier</li>
            </ol>
            <div class="path_bar"><i data-progress="62"></i></div>
          </div>
        </div>
        <div class="dash_split">
          <div class="dash_panel">
            <div class="dash_panel-head"><span>AML / KYC controls</span></div>
            <ul class="dash_controls">
              <li><span>CDD &amp; screening</span><b class="on">On</b></li>
              <li><span>Transaction monitoring</span><b class="on">On</b></li>
              <li><span>Travel Rule</span><b class="on">On</b></li>
            </ul>
          </div>
          <div class="dash_panel">
            <div class="dash_panel-head"><span>Cybersecurity</span><span class="dash_mono">by ITSEC</span></div>
            <div class="cyber_row"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M12 3 5 5.5V11c0 4.5 3 7.8 7 9 4-1.2 7-4.5 7-9V5.5L12 3Zm-2.2 8.4 1.6 1.6 3-3.2"/></svg><div><strong>Assured</strong><span>Controls baseline verified</span></div></div>
          </div>
        </div>
        <div class="dash_panel">
          <div class="dash_panel-head"><span>Evidence vault</span><span class="dash_mono">12 / 14 docs</span></div>
          <ul class="dash_vault">
            <li class="ok">AML/CFT policy <span>v3 · signed</span></li>
            <li class="ok">Governance &amp; ownership <span>verified</span></li>
            <li class="pending">Cyber incident plan <span>in review</span></li>
          </ul>
        </div>
      </div>
    </div>"""


# NEXUS platform modules (label, mono code, description)
NEXUS_MODULES = [
    ("Regulator Mapping Engine", "MAP", "Classify activities and map them to the right UAE authority across VARA, SCA, DFSA, ADGM, GCGRA, and CBUAE."),
    ("License Pathway Tracker", "PATH", "Live milestones from business-model assessment through dossier submission and regulator response."),
    ("AML/KYC Control Center", "AML", "CDD and sanctions screening, transaction monitoring, and Travel Rule controls in one operational view."),
    ("Cybersecurity Assurance", "CYBER", "A regulator-aligned controls baseline, testing, and incident readiness, backed by ITSEC."),
    ("Evidence Vault", "VAULT", "Versioned, audit-ready documents — policies, governance, and approvals — organised for regulator review."),
    ("Reporting & Supervision", "REPORT", "Ongoing obligations, reporting calendars, and alerts that keep the licence compliant after approval."),
]


def home_hero():
    return f"""<section class="section_home-hero" id="home-hero">
  {media_backdrop("assets/media/dubai-skyline.jpg", opacity="0.14", parallax=True)}
  <div class="hero_bg" aria-hidden="true"><div class="hero_grid"></div></div>
  <div class="container-large"><div class="home-hero_grid">
    <div class="hero_copy" data-reveal>
      <span class="badge"><span class="badge_dot"></span>UAE Regulatory Licensing · Compliance · Cybersecurity</span>
      <h1>Secure UAE Licensing, Compliance &amp; <span class="accent">Cybersecurity</span> Across Every Major Regulator</h1>
      <p class="hero_sub">SecureVisa Group helps crypto, fintech, Web3, tokenization, forex, gaming, and financial services companies navigate VARA, SCA, DFSA, ADGM, GCGRA, and CBUAE requirements with audit-ready documentation, compliance technology, and cybersecurity assurance.</p>
      <div class="hero_actions">
        <a class="btn btn-primary btn-lg" href="contact.html">Book a Regulatory Call</a>
        <a class="btn btn-whatsapp btn-lg" href="{WA}" rel="nofollow">{WA_SVG}Talk to an Expert on WhatsApp</a>
      </div>
      <ul class="hero_trust" aria-label="Trust signals">
        <li><strong>20+</strong><span>Years professional services</span></li>
        <li><strong>15,000+</strong><span>Enterprises serviced</span></li>
        <li><strong>6</strong><span>UAE regulatory authorities covered</span></li>
      </ul>
      <p class="hero_capline">Licensing · AML/KYC · Cybersecurity · Audit Readiness</p>
    </div>
    {command_center(reveal=True)}
  </div></div>
</section>

<section class="section_strip" aria-label="Coverage summary"><div class="container-large strip_inner">
  <span>Regulatory coverage</span>
  <ul class="strip_list"><li>VARA</li><li>SCA</li><li>DFSA</li><li>ADGM · FSRA</li><li>GCGRA</li><li>CBUAE</li></ul>
  <span class="strip_note">Licensing · AML/KYC · Cybersecurity · Audit Readiness</span>
</div></section>"""


def reg_tab_panel(key, active=False):
    d = REG_DATA[key]
    chips = "".join(f"<li>{html.escape(a)}</li>" for a in d["activities"][:5])
    checks = "".join(f"<li>{html.escape(s)}</li>" for s in d["supports"][:4])
    hidden = "" if active else " hidden"
    return f"""<article class="regulator-card{' is-active' if active else ''}" role="tabpanel" data-panel="{key}"{hidden}>
            <div class="reg_card-main">
              <span class="reg_pill">{html.escape(d['full'])}</span>
              <h3>{REG_NAMES[key]} — {html.escape(d['tag'])}</h3>
              <p>{html.escape(d['blurb'])}</p>
              <ul class="reg_chips">{chips}</ul>
            </div>
            <div class="reg_card-side">
              <span class="reg_side-label">SecureVisa supports</span>
              <ul class="reg_check">{checks}</ul>
              <a class="reg_link" href="{key}.html">Explore {REG_NAMES[key]} pathway →</a>
            </div>
          </article>"""


def home_regulators():
    tabs = "\n          ".join(
        f'<button class="reg_tab{" is-active" if i == 0 else ""}" role="tab" aria-selected="{"true" if i==0 else "false"}" data-tab="{k}"><strong>{REG_NAMES[k]}</strong><span>{html.escape(REG_DATA[k]["tag"])}</span></button>'
        for i, k in enumerate(REG_ORDER))
    panels = "\n          ".join(reg_tab_panel(k, i == 0) for i, k in enumerate(REG_ORDER))
    return f"""<section class="section_regulators" id="regulators">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Regulator coverage matrix</span><h2>UAE Regulatory Authorities We Cover</h2>
      <p>Select an authority to review its mandate, who it applies to, and the licensing activities SecureVisa supports. We help map your business model to the right regulator before any application begins.</p></header>
    <div class="reg_tabs" data-tabs>
      <div class="reg_tablist" role="tablist" aria-label="UAE regulators">
          {tabs}
      </div>
      <div class="reg_panels">
          {panels}
      </div>
    </div>
  </div>
</section>"""


def home_ecosystem():
    nodes = [
        ("01", "Regulatory Strategy &amp; Licensing", "Activity mapping and regulator-ready applications."),
        ("02", "Compliance Automation", "Policy, controls and reporting built to be maintained."),
        ("03", "Cybersecurity Assurance by ITSEC", "Regulator-aligned security controls and testing."),
        ("04", "Digital Identity · KYC · KYB", "Onboarding, verification and screening workflows."),
        ("05", "AML/CFT &amp; Travel Rule", "Risk-based monitoring and reporting support."),
        ("06", "Audit-Ready Documentation", "Governance and evidence prepared for review."),
    ]
    li = "\n        ".join(f'<li><span class="eco_idx">{i}</span><strong>{t}</strong><span>{d}</span></li>' for i, t, d in nodes)
    return f"""<section class="section_ecosystem" id="ecosystem">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Integrated capability</span><h2>SecureVisa Group Compliance Ecosystem</h2>
      <p>Licensing is one milestone. SecureVisa connects regulatory strategy, compliance automation, and cybersecurity assurance into a single, audit-ready operating model.</p></header>
    <div class="eco_diagram">
      <div class="eco_core"><img src="assets/icon.png" alt="SecureVisa Group shield" /><strong>SecureVisa Group</strong><span>Regulatory operating core</span></div>
      <ul class="eco_nodes">
        {li}
      </ul>
      <p class="eco_partners">Supported by the <strong>ITSEC</strong>, <strong>VerifiX</strong>, and <strong>CompliX</strong> ecosystem.</p>
    </div>
  </div>
</section>"""


def home_industries():
    cards = []
    for slug in ["crypto-web3-licensing", "fintech-licensing", "tokenization-rwa", "forex-licensing", "gaming-nft", "real-estate-tokenization"]:
        d = IND_DATA[slug]
        cards.append(f"""        <article class="ind_card">
          <h3>{html.escape(d['name'])}</h3>
          <dl>
            <div><dt>Who it's for</dt><dd>{html.escape(d['who'])}</dd></div>
            <div><dt>Main regulator</dt><dd>{html.escape(d['reg'])}</dd></div>
            <div><dt>Core requirements</dt><dd>{html.escape(d['reqs'])}</dd></div>
          </dl>
          <a class="ind_cta" href="{slug}.html">Explore pathway →</a>
        </article>""")
    return f"""<section class="section_industries" id="industries">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Industry pathways</span><h2>Licensing Pathways for Regulated Industries</h2>
      <p>Built for high-stakes regulated businesses. Each pathway pairs the right regulator with the core compliance work required to reach a credible application.</p></header>
    <div class="ind_grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>"""


def process_section():
    steps = "\n        ".join(
        f'<li class="proc_step"><span class="proc_num">{n}</span><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></li>'
        for n, t, d in PROCESS)
    return f"""<section class="section_process" id="process">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Advisory methodology</span><h2>From Business Model to Regulator Approval</h2>
      <p>A structured pathway that turns a business model into a regulator-ready application — and keeps it compliant after approval.</p></header>
    <ol class="process_timeline">
        {steps}
    </ol>
  </div>
</section>"""


def why_section():
    items = [
        ("Multi-regulator UAE expertise", "One team across VARA, SCA, DFSA, ADGM, GCGRA, and CBUAE pathways."),
        ("Compliance technology + cybersecurity backbone", "Advisory reinforced by automation and security capability."),
        ("Audit-ready documentation", "Evidence and governance prepared to withstand regulator review."),
        ("Pre-license and post-license support", "From first assessment through ongoing supervision."),
        ("Built for serious regulated companies", "Executive-grade engagement, not template consulting."),
        ("Supported by ITSEC, VerifiX &amp; CompliX", "An integrated ecosystem behind every engagement."),
    ]
    li = "\n        ".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in items)
    return f"""<section class="section_why" id="why">
  <div class="container-large why_grid">
    <header class="section_head section_head--left"><span class="eyebrow">The SecureVisa difference</span><h2>Why SecureVisa Group</h2>
      <p>A multi-regulator advisory firm with a compliance-technology and cybersecurity backbone — built for companies that cannot afford to get regulation wrong.</p>
      <a class="btn btn-primary" href="contact.html">Book a Regulatory Call</a></header>
    <ul class="why_list">
        {li}
    </ul>
  </div>
</section>"""


def case_section():
    cases = [
        ("Anonymized example · Crypto exchange", "Crypto exchange readiness pathway", "Activity classification, AML/CFT and Travel Rule framework, and a structured application dossier prepared for a virtual asset exchange model.", ["VARA", "AML/CFT", "Custody controls"]),
        ("Anonymized example · Tokenization", "Tokenized asset project", "Structuring support and disclosure documentation aligned to capital-markets expectations for a tokenized investment platform.", ["SCA", "Disclosures", "Investor protection"]),
        ("Anonymized example · FinTech", "FinTech payment service provider", "Safeguarding, governance, and AML/KYC framework preparation for a payments business assessing its UAE pathway.", ["CBUAE", "Safeguarding", "KYC/KYB"]),
        ("Anonymized example · Forex", "Forex brokerage licensing strategy", "Regulator mapping and readiness planning, including conduct and client-money considerations for a brokerage operator.", ["SCA", "Client money", "Conduct"]),
    ]
    cards = "\n        ".join(
        f'<article class="case_card"><span class="case_tag">{html.escape(t)}</span><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p><ul class="case_meta">{"".join(f"<li>{html.escape(m)}</li>" for m in meta)}</ul></article>'
        for t, h, p, meta in cases)
    return f"""<section class="section_case-proof" id="case-proof">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">From licensing to launch</span><h2>Project-type outcomes</h2>
      <p>Illustrative, anonymized examples of the engagement types SecureVisa supports. These are project-type examples, not client testimonials, and do not imply guaranteed regulatory outcomes.</p></header>
    <div class="case_grid">
        {cards}
    </div>
  </div>
</section>"""


def ebook_section():
    return f"""<section class="section_ebook" id="ebook">
  <div class="container-large ebook_grid">
    <div class="ebook_copy">
      <span class="eyebrow">Free resource</span><h2>VARA License Setup Guide</h2>
      <p>A practical, regulator-aware guide to preparing for virtual asset licensing in Dubai.</p>
      <ul class="ebook_list">
        <li>Complete UAE compliance framework overview</li>
        <li>VARA licensing pathway, step by step</li>
        <li>AML/KYC checklist</li>
        <li>Cybersecurity readiness essentials</li>
        <li>Audit-proof documentation guidance</li>
      </ul>
      <a class="btn btn-primary btn-lg" href="ebook.html">Download eBook</a>
    </div>
    <div class="ebook_visual" aria-hidden="true"><div class="ebook_doc">
      <div class="ebook_doc-head"><span class="ebook_badge">VARA</span><span class="dash_mono">Setup Guide</span></div>
      <div class="ebook_lines"><i></i><i></i><i></i><i></i><i></i></div>
      <div class="ebook_check"><span></span>AML/KYC checklist</div>
      <div class="ebook_check"><span></span>Cybersecurity readiness</div>
      <div class="ebook_check"><span></span>Documentation index</div>
    </div></div>
  </div>
</section>"""


def home_nexus():
    mods = "\n        ".join(
        f'<li data-reveal><span class="nx_code">{c}</span><strong>{html.escape(t)}</strong><span class="nx_desc">{html.escape(d)}</span></li>'
        for t, c, d in NEXUS_MODULES)
    return f"""<section class="section_nexus" id="nexus">
  {media_backdrop("assets/media/network-nodes.jpg", opacity="0.10", parallax=True)}
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Introducing the platform</span>
      <h2>SecureVisa <span class="accent">NEXUS</span> — one platform for the whole compliance lifecycle</h2>
      <p>NEXUS turns the regulatory command center into your operating model: regulator mapping, licence tracking, AML/KYC, cybersecurity, and audit-ready evidence in a single supervised view.</p></header>
    <ul class="nexus_modules">
        {mods}
    </ul>
    <div class="nexus_cta" data-reveal>
      <a class="btn btn-primary btn-lg" href="nexus.html">Explore NEXUS</a>
      <a class="btn btn-ghost btn-lg" href="contact.html">Request a demo</a>
    </div>
  </div>
</section>"""


def nexus_page():
    mod_cards = "\n        ".join(
        f'<article class="nx_card" data-reveal><span class="nx_code">{c}</span><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>'
        for t, c, d in NEXUS_MODULES)
    body = subhero(
        "NEXUS · Compliance Platform",
        "SecureVisa NEXUS — your UAE compliance, in one platform",
        "NEXUS unifies regulator mapping, licence tracking, AML/KYC, cybersecurity assurance, and audit-ready evidence into a single supervised workspace, so regulated teams always know exactly where they stand.",
        [("index.html", "Home"), ("services.html", "Services"), ("", "NEXUS")],
        [("6 / 6", "Regulators mapped"), ("1", "Source of truth")],
        primary=("contact.html", "Request a NEXUS demo"),
        bg="assets/media/nexus-hero.jpg",
    ) + f"""
<section class="section_pad">
  <div class="container-large split">
    <div class="prose" data-reveal>
      <span class="eyebrow">What NEXUS is</span>
      <h2>The regulatory command center, productized</h2>
      <p>Most regulated businesses run compliance across spreadsheets, shared drives, and email threads. NEXUS replaces that with one workspace where every regulator, control, and document lives together and stays in sync.</p>
      <p>It is the same operating model SecureVisa uses to take a business model from first assessment to a regulator-ready application — now visible to your team in real time.</p>
      <ul class="check_list">
        <li>A single, supervised view across six UAE regulators</li>
        <li>Live licence-pathway tracking with clear next steps</li>
        <li>AML/KYC and cybersecurity controls in one place</li>
        <li>Versioned, audit-ready evidence on demand</li>
      </ul>
      <div style="margin-top:26px"><a class="btn btn-primary btn-lg" href="contact.html">Request a NEXUS demo</a></div>
    </div>
    <div class="nexus_visual" data-reveal>{command_center()}</div>
  </div>
</section>

<section class="section_pad section_pad--alt">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Inside the platform</span><h2>Six modules, one source of truth</h2>
      <p>Each module is built around what UAE regulators actually expect — and designed to be maintained long after the licence is granted.</p></header>
    <div class="nexus_grid">
        {mod_cards}
    </div>
  </div>
</section>
{process_section()}
{home_ecosystem()}
{faq_block(FAQS[4:7], heading="NEXUS platform FAQs")}
{final_cta()}"""
    return write("nexus.html", "NEXUS Compliance Platform | SecureVisa Group",
                 "SecureVisa NEXUS is a UAE regulatory compliance platform that unifies regulator mapping, licence tracking, AML/KYC, cybersecurity assurance, and audit-ready evidence across VARA, SCA, DFSA, ADGM, GCGRA, and CBUAE.",
                 body, active="nexus",
                 breadcrumb=[("index.html", "Home"), ("services.html", "Services"), ("nexus.html", "NEXUS")])


# ==========================================================================
# SUB-PAGES
# ==========================================================================
def regulator_page(key):
    d = REG_DATA[key]
    name = REG_NAMES[key]
    chips = "".join(f"<li>{html.escape(a)}</li>" for a in d["activities"])
    supports = "".join(f"<li>{html.escape(s)}</li>" for s in d["supports"])
    others = "".join(
        f'<li><span class="info_idx">{REG_NAMES[k]}</span><h3><a class="reg_link" href="{k}.html">{REG_NAMES[k]}</a></h3><p>{html.escape(REG_DATA[k]["tag"])}</p></li>'
        for k in REG_ORDER if k != key)
    body = subhero(
        d["full"], f"{name} licensing &amp; compliance in the UAE", d["blurb"],
        [("index.html", "Home"), ("regulators.html", "Regulators"), ("", name)],
        d["stats"], primary=("contact.html", f"Discuss your {name} pathway"),
    ) + f"""
<section class="section_pad">
  <div class="container-large split">
    <div class="prose">
      <span class="eyebrow">About the regulator</span>
      <h2>What {name} regulates</h2>
      <p>{html.escape(d['long'])}</p>
      <div class="callout">SecureVisa is a private advisory firm and is not affiliated with {name}. We help applicants prepare regulator-ready documentation and navigate the {name} pathway.</div>
      <h3>Regulated activities</h3>
      <ul class="reg_chips" style="margin-top:10px">{chips}</ul>
    </div>
    <div>
      <span class="eyebrow">How SecureVisa supports you</span>
      <h2 class="prose" style="margin-bottom:18px">{name} application support</h2>
      <ul class="check_list">{supports}</ul>
      <div style="margin-top:26px"><a class="btn btn-primary btn-lg" href="contact.html">Book a {name} consultation</a></div>
    </div>
  </div>
</section>

<section class="section_pad section_pad--alt">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Other authorities</span><h2>Explore other UAE regulators</h2></header>
    <ul class="info_grid">{others}</ul>
  </div>
</section>
{process_section()}
{final_cta()}"""
    return write(f"{key}.html",
                 f"{name} License UAE | {d['full']} Advisory | SecureVisa Group",
                 f"SecureVisa Group helps businesses prepare regulator-ready documentation for the {d['full']} ({name}) and navigate UAE licensing and compliance.",
                 body, active="regulators",
                 breadcrumb=[("index.html", "Home"), ("regulators.html", "Regulators"), (f"{key}.html", name)])


def industry_page(slug):
    d = IND_DATA[slug]
    bullets = "".join(f"<li>{html.escape(b)}</li>" for b in d["bullets"])
    reg_cards = "".join(
        f'<li><span class="info_idx">{REG_NAMES[k]}</span><h3><a class="reg_link" href="{k}.html">{REG_NAMES[k]}</a></h3><p>{html.escape(REG_DATA[k]["tag"])}</p></li>'
        for k in d["regs"])
    body = subhero(
        d["pill"], html.escape(d["name"]), d["intro"],
        [("index.html", "Home"), ("industries.html", "Industries"), ("", d["name"])],
        [("Pathway", d["reg"].split("·")[0].strip()), ("Multi-reg", "UAE coverage")],
    ) + f"""
<section class="section_pad">
  <div class="container-large split">
    <div class="prose">
      <span class="eyebrow">The pathway</span>
      <h2>What this pathway involves</h2>
      <p>{html.escape(d['intro'])}</p>
      <dl class="def_list" style="margin-top:8px">
        <div><dt>Who it's for</dt><dd>{html.escape(d['who'])}</dd></div>
        <div><dt>Main regulator pathway</dt><dd>{html.escape(d['reg'])}</dd></div>
        <div><dt>Core compliance requirements</dt><dd>{html.escape(d['reqs'])}</dd></div>
      </dl>
    </div>
    <div>
      <span class="eyebrow">How SecureVisa helps</span>
      <h2 class="prose" style="margin-bottom:18px">Engagement scope</h2>
      <ul class="check_list">{bullets}</ul>
      <div style="margin-top:26px"><a class="btn btn-primary btn-lg" href="contact.html">Explore this pathway</a></div>
    </div>
  </div>
</section>

<section class="section_pad section_pad--alt">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">Likely regulators</span><h2>Regulators on this pathway</h2></header>
    <ul class="info_grid">{reg_cards}</ul>
  </div>
</section>
{process_section()}
{final_cta()}"""
    return write(f"{slug}.html",
                 f"{d['name']} UAE | Regulatory Pathway | SecureVisa Group",
                 f"{d['name']} in the UAE — SecureVisa helps map the regulator, prepare audit-ready documentation, and build compliance for {d['who'].lower()}",
                 body, active="industries",
                 breadcrumb=[("index.html", "Home"), ("industries.html", "Industries"), (f"{slug}.html", d["name"])])


def overview_page(filename, active, pill, h1, sub, lead, grid_items, grid_kind, faq_items=None):
    """grid_kind: 'reg' or 'ind'"""
    if grid_kind == "reg":
        cards = "".join(
            f'<li><span class="info_idx">{REG_NAMES[k]}</span><h3><a class="reg_link" href="{k}.html">{REG_NAMES[k]} — {html.escape(REG_DATA[k]["tag"])}</a></h3><p>{html.escape(REG_DATA[k]["blurb"])}</p></li>'
            for k in grid_items)
        grid = f'<ul class="info_grid">{cards}</ul>'
    else:
        cards = []
        for slug in grid_items:
            d = IND_DATA[slug]
            cards.append(f"""        <article class="ind_card"><h3>{html.escape(d['name'])}</h3>
          <dl><div><dt>Who it's for</dt><dd>{html.escape(d['who'])}</dd></div>
          <div><dt>Main regulator</dt><dd>{html.escape(d['reg'])}</dd></div>
          <div><dt>Core requirements</dt><dd>{html.escape(d['reqs'])}</dd></div></dl>
          <a class="ind_cta" href="{slug}.html">Explore pathway →</a></article>""")
        grid = '<div class="ind_grid">\n' + "\n".join(cards) + "\n    </div>"
    light = " section_pad--light" if grid_kind == "ind" else ""
    body = subhero(pill, h1, sub,
                   [("index.html", "Home"), ("", h1.replace("&amp;", "&"))],
                   [("6", "UAE regulators") if grid_kind == "reg" else ("7", "Industry pathways"), ("Audit-ready", "Documentation")]) + f"""
<section class="section_pad{light}">
  <div class="container-large">
    <header class="section_head"><span class="eyebrow">{html.escape(pill)}</span><h2>{lead}</h2></header>
    {grid}
  </div>
</section>
""" + (faq_block(faq_items) if faq_items else "") + process_section() + final_cta()
    return write(filename, f"{h1.replace('&amp;','&')} | SecureVisa Group", sub, body, active=active,
                 breadcrumb=[("index.html", "Home"), (filename, h1.replace("&amp;", "&"))])


def simple_page(filename, active, pill, h1, sub, sections_html, crumb_name):
    body = subhero(pill, h1, sub,
                   [("index.html", "Home"), ("", crumb_name)],
                   [("UAE", "Dubai-based"), ("Confidential", "Engagements")]) + sections_html + final_cta()
    return write(filename, f"{h1.replace('&amp;','&')} | SecureVisa Group", sub, body, active=active,
                 breadcrumb=[("index.html", "Home"), (filename, crumb_name)])


def main():
    # ---- Home ----
    home_body = (home_hero() + home_regulators() + home_nexus() + home_ecosystem() + home_industries()
                 + process_section() + why_section() + case_section() + ebook_section()
                 + faq_block(FAQS) + final_cta())
    write("index.html",
          "UAE Licensing & Compliance Experts | VARA, SCA, DFSA, ADGM | SecureVisa Group",
          "SecureVisa Group helps crypto, fintech, Web3, tokenization, forex, gaming, and financial services companies secure UAE licensing and build audit-ready compliance across VARA, SCA, DFSA, ADGM, GCGRA, and CBUAE.",
          home_body, active="")

    # ---- NEXUS platform page ----
    nexus_page()

    # ---- Regulator detail pages ----
    for k in REG_ORDER:
        regulator_page(k)

    # ---- Industry detail pages ----
    for slug in IND_DATA:
        industry_page(slug)

    # ---- Overviews ----
    overview_page("regulators.html", "regulators", "Regulator coverage",
                  "UAE Regulatory Authorities We Cover",
                  "From virtual assets to payments, SecureVisa covers the six UAE authorities that matter most to regulated businesses.",
                  "The six regulators we cover", REG_ORDER, "reg",
                  faq_items=FAQS[:4])
    overview_page("industries.html", "industries", "Industry pathways",
                  "Licensing Pathways for Regulated Industries",
                  "Built for high-stakes regulated businesses. Choose your industry to see the regulator pathway and core compliance requirements.",
                  "Built for high-stakes regulated businesses",
                  ["crypto-web3-licensing", "fintech-licensing", "tokenization-rwa", "forex-licensing", "web3-defi-licensing", "real-estate-tokenization", "gaming-nft"], "ind")
    overview_page("services.html", "services", "What we do",
                  "Services Across the Licensing Lifecycle",
                  "Regulatory strategy, compliance automation, and cybersecurity assurance — delivered as one audit-ready operating model.",
                  "From licensing strategy to ongoing compliance",
                  ["crypto-web3-licensing", "fintech-licensing", "tokenization-rwa", "forex-licensing", "real-estate-tokenization", "gaming-nft"], "ind")

    # ---- Ecosystem ----
    eco_body = (subhero("Integrated capability", "SecureVisa Group Compliance Ecosystem",
                        "Licensing is one milestone. SecureVisa connects regulatory strategy, compliance automation, and cybersecurity assurance into a single, audit-ready operating model.",
                        [("index.html", "Home"), ("services.html", "Services"), ("", "Ecosystem")],
                        [("ITSEC", "Cybersecurity"), ("VerifiX · CompliX", "Compliance tech")])
                + home_ecosystem() + why_section() + final_cta())
    write("ecosystem.html", "Compliance Ecosystem | SecureVisa Group",
          "The SecureVisa Group compliance ecosystem: regulatory strategy, compliance automation, cybersecurity assurance by ITSEC, digital identity, AML/CFT, and audit-ready documentation.",
          eco_body, active="services",
          breadcrumb=[("index.html", "Home"), ("services.html", "Services"), ("ecosystem.html", "Ecosystem")])

    # ---- About ----
    about_html = """
<section class="section_pad"><div class="container-large split">
  <div class="prose"><span class="eyebrow">Who we are</span><h2>A UAE regulatory advisory firm, built for serious businesses</h2>
    <p>SecureVisa Group is a private corporate service provider specialising in UAE regulatory licensing, compliance, and cybersecurity assurance. We help regulated and aspiring-regulated businesses navigate the UAE's evolving framework with clarity and credibility.</p>
    <p>Our work spans pre-license strategy through post-license supervision, reinforced by a compliance-technology and cybersecurity backbone via our partner ecosystem.</p>
    <div class="callout">SecureVisa Group is not a government authority or regulator. We support licensing applications and compliance preparation; we do not guarantee regulatory approval.</div>
  </div>
  <div><span class="eyebrow">At a glance</span><h2 class="prose" style="margin-bottom:18px">What defines our practice</h2>
    <ul class="check_list">
      <li>Multi-regulator UAE expertise across six authorities</li>
      <li>Compliance technology and cybersecurity backbone</li>
      <li>Audit-ready documentation and governance</li>
      <li>Pre-license and post-license support</li>
      <li>Supported by ITSEC, VerifiX, and CompliX</li>
    </ul></div>
</div></section>
""" + why_section()
    simple_page("about.html", "resources", "About SecureVisa Group",
                "Your trusted partner for UAE regulatory compliance &amp; licensing",
                "SecureVisa Group helps crypto, fintech, Web3, forex, gaming, and financial services companies get licensed and stay compliant in the UAE.",
                about_html, "About Us")

    # ---- Blog ----
    posts = [
        ("How to get a VARA license in Dubai", "A practical overview of the VARA pathway, activity classes, and what a regulator-ready application looks like.", "VARA"),
        ("UAE fintech compliance requirements explained", "CBUAE, DFSA, or ADGM? How payment and fintech businesses identify the right UAE pathway.", "FinTech"),
        ("SCA licensing for tokenized assets", "What real-world-asset projects should know about capital-markets expectations in the UAE.", "Tokenization"),
        ("Building a regulator-ready cybersecurity framework", "Why cybersecurity governance increasingly shapes UAE licensing outcomes — with ITSEC.", "Cybersecurity"),
        ("AML/CFT compliance framework for UAE businesses", "Core building blocks: CDD, screening, monitoring, reporting, and the Travel Rule.", "AML/KYC"),
        ("DFSA and ADGM compliance advisory", "Comparing the two financial free-zone regimes for funds, fintech, and virtual assets.", "Free zones"),
    ]
    cards = "\n".join(
        f'        <article class="ind_card"><h3>{html.escape(t)}</h3><dl><div><dt>{html.escape(tag)}</dt><dd>{html.escape(s)}</dd></div></dl><a class="ind_cta" href="contact.html">Read more →</a></article>'
        for t, s, tag in posts)
    blog_html = f"""
<section class="section_pad section_pad--light"><div class="container-large">
  <header class="section_head"><span class="eyebrow">Insights</span><h2>Regulatory insights &amp; guidance</h2>
    <p>Plain-language perspectives on UAE licensing, compliance, and cybersecurity. Editorial guidance only — not legal advice.</p></header>
  <div class="ind_grid">
{cards}
  </div>
</div></section>"""
    simple_page("blog.html", "resources", "SecureVisa Blog",
                "Regulatory insights &amp; guidance for UAE-regulated businesses",
                "Plain-language insights on UAE licensing, AML/KYC compliance, cybersecurity, and the VARA, SCA, DFSA, ADGM, GCGRA, and CBUAE frameworks.",
                blog_html, "Blog")

    # ---- Case Studies ----
    case_html = case_section()
    simple_page("case-studies.html", "resources", "Case studies",
                "From Licensing to Launch",
                "Anonymized, project-type examples of SecureVisa engagements across crypto, tokenization, fintech, and forex. Not testimonials; no guaranteed outcomes implied.",
                case_html, "Case Studies")

    # ---- Partners ----
    partners = [
        ("ITSEC", "Cybersecurity assurance — regulator-aligned security controls, testing, and incident response."),
        ("VerifiX", "Digital identity, KYC and KYB onboarding and verification workflows."),
        ("CompliX", "Compliance automation — policy, controls, and reporting built to be maintained."),
    ]
    pc = "".join(f'<li><span class="info_idx">Ecosystem partner</span><h3>{p}</h3><p>{html.escape(d)}</p></li>' for p, d in partners)
    partners_html = f"""
<section class="section_pad"><div class="container-large">
  <header class="section_head"><span class="eyebrow">Our ecosystem</span><h2>Partners behind every engagement</h2>
    <p>SecureVisa Group is supported by an integrated ecosystem spanning cybersecurity, identity, and compliance technology.</p></header>
  <ul class="info_grid">{pc}</ul>
</div></section>"""
    simple_page("partners.html", "resources", "Partners",
                "An integrated regulatory, identity &amp; cybersecurity ecosystem",
                "SecureVisa Group works with ITSEC, VerifiX, and CompliX to deliver licensing, compliance automation, digital identity, and cybersecurity assurance in the UAE.",
                partners_html, "Partners")

    # ---- eBook ----
    ebook_html = ebook_section() + faq_block(FAQS[:4], heading="VARA licensing FAQs")
    simple_page("ebook.html", "", "Free resource",
                "VARA License Setup Guide",
                "Download the SecureVisa VARA License Setup Guide: UAE compliance framework, VARA licensing pathway, AML/KYC checklist, cybersecurity readiness, and audit-proof documentation.",
                ebook_html, "Download eBook")

    # ---- Contact ----
    contact_html = f"""
<section class="section_pad"><div class="container-large split">
  <div class="prose"><span class="eyebrow">Confidential consultation</span><h2>Speak with a SecureVisa compliance expert</h2>
    <p>Share your licensing or compliance goals in a confidential session. SecureVisa will outline regulator requirements, expected documentation, timeline considerations, and next steps.</p>
    <ul class="check_list" style="margin-top:8px">
      <li>Same-day response during UAE business hours</li>
      <li>Confidential, no-obligation discussion</li>
      <li>Clear next steps and documentation outline</li>
    </ul>
    <div class="callout" style="margin-top:20px">No spam. Your information is used only to respond to your enquiry.</div>
  </div>
  <div><span class="eyebrow">Get in touch</span><h2 class="prose" style="margin-bottom:18px">Contact SecureVisa Group</h2>
    <ul class="footer_contact" style="margin-bottom:24px">
      <li><span>Phone</span><a href="tel:{TEL}">+971.4.257.2406</a></li>
      <li><span>WhatsApp</span><a href="{WA}" rel="nofollow">+971.58.517.9303</a></li>
      <li><span>Email</span><a href="mailto:hello@securevisanow.com">hello@securevisanow.com</a></li>
      <li><span>Address</span><address>Onyx Tower 1, The Greens, Dubai</address></li>
    </ul>
    <div class="final_actions">
      <a class="btn btn-primary btn-lg" href="tel:{TEL}">Book a Regulatory Call</a>
      <a class="btn btn-whatsapp btn-lg" href="{WA}" rel="nofollow">WhatsApp SecureVisa Support</a>
    </div>
  </div>
</div></section>"""
    simple_page("contact.html", "", "Contact",
                "Speak with a SecureVisa Compliance Expert",
                "Contact SecureVisa Group for a confidential UAE licensing and compliance consultation across VARA, SCA, DFSA, ADGM, GCGRA, and CBUAE. Same-day response during UAE hours.",
                contact_html, "Contact Us")

    print("Generated pages:")
    for f in sorted(os.listdir(ROOT)):
        if f.endswith(".html"):
            print("  ", f)


if __name__ == "__main__":
    main()
