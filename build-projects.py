#!/usr/bin/env python3
# =============================================================================
# PRIME STRUCTURES — project page generator
#
# One template, one data table, eleven pages. Change the template or the CSS
# and every project page changes with it. Run:  python3 build-projects.py
#
# RULE: nothing in PROJECTS may be invented. Every value here traces to the
# original project pages (data strips) or projects_info.pdf as recorded in
# "PROJECT INVENTORY & COLOR RHYTHM.md". Fields with no documented value are
# simply omitted — the template never prints an empty or [TBD] row.
# =============================================================================

import html, io, os, re

SITE = "https://primestructures.de"
CSS_V, JS_V = "51", "17"

DIAGRAMS = open("_diagrams.part").read() if os.path.exists("_diagrams.part") else ""

# --- project table --------------------------------------------------------
# slug, name, category, descriptor (one line, factual), hero image + alt,
# facts (ordered, only documented), aufgabe/loesung copy, scope list,
# gallery (optional), note (optional honesty line), title/description for SEO
PROJECTS = [
 dict(
  slug="friedbergstrasse", name="Dachgeschossausbau Friedbergstraße", cat="Bauen im Bestand",
  descriptor="Tragwerksplanung für den Ausbau eines Gründerzeit-Dachgeschosses zu Wohnraum.",
  hero="friedbergstrasse.jpg", hero_w=2000, hero_h=1341,
  hero_alt="Dachgeschossausbau Friedbergstraße in Berlin-Friedrichshain — Straßenansicht des Gründerzeithauses mit neuem Dachgeschoss",
  facts=[("Projektart","Bauen im Bestand"),("Standort","Berlin-Friedrichshain"),
         ("Bestand","Gründerzeit-Mehrfamilienhaus, Baujahr um 1910"),
         ("Konstruktion","Vollholz / Holz-Stahl-Hybrid / Vollstahl — in Untersuchung"),
         ("Leistung","Komplette Tragwerksplanung"),("Status","In Planung")],
  aufgabe="Ein Gründerzeit-Mehrfamilienhaus, Baujahr um 1910. Das Dachgeschoss soll Wohnraum werden. Die Frage an die Tragwerksplanung: Welche Dachkonstruktion trägt der Bestand — und welche trägt sich wirtschaftlich?",
  loesung="Wir haben drei Tragwerksvarianten für die neue Dachkonstruktion untersucht und jede nach Lastabtrag in den Bestand, Kosten und Bauablauf bewertet. So entscheidet der Bauherr auf Grundlage von Zahlen, nicht von Annahmen.",
  facts_big=[("1910","Baujahr Bestand"),("3","Varianten untersucht")],
  diagrams=True, diagrams_label="Variantenuntersuchung · Dachkonstruktion",
  scope=["Komplette Tragwerksplanung","Variantenuntersuchung der Dachkonstruktion",
         "Nachweis des Lastabtrags in den Bestand"],
  gallery=[("friedberg-tall.jpg",1000,1342,"Gründerzeitfassade der Friedbergstraße mit neuem Dachgeschoss in Stehfalzdeckung","tall")],
  title="Dachgeschossausbau Friedbergstraße Berlin — Tragwerksplanung | Prime Structures",
  desc="Tragwerksplanung für den Dachgeschossausbau eines Gründerzeithauses von 1910 in Berlin-Friedrichshain: Variantenuntersuchung Vollholz, Holz-Stahl-Hybrid und Vollstahl."),

 dict(
  slug="villa-ruedersdorf", name="Aufstockung Villa Rüdersdorf", cat="Bauen im Bestand",
  descriptor="Tragwerksplanung für Aufstockung und Umbau eines Mehrfamilienhauses in Hanglage.",
  hero="villa-ruedersdorf.jpg", hero_w=1600, hero_h=900,
  hero_alt="Villa Rüdersdorf bei Berlin nach der Aufstockung — Hanglage mit neuem Obergeschoss",
  facts=[("Projektart","Bauen im Bestand"),("Standort","Rüdersdorf bei Berlin"),
         ("Konstruktion","Aufstockung · Pfosten-Riegel-Fassade"),
         ("Leistung","Tragwerksplanung · Genehmigungsstatik"),("Status","Fertiggestellt")],
  aufgabe="Ein Mehrfamilienhaus in Hanglage. Der Bauherr wollte ein zusätzliches Dachgeschoss — und einen Wintergarten mit Glasfassade.",
  loesung="Tragwerksplanung für Aufstockung und Umbau: Das neue Geschoss trägt in den Bestand ab, der Wintergarten steht als Pfosten-Riegel-Konstruktion aus Glas und Stahl.",
  scope=["Tragwerksplanung für Aufstockung und Umbau","Genehmigungsstatik",
         "Pfosten-Riegel-Konstruktion des Wintergartens"],
  title="Aufstockung Villa Rüdersdorf — Statik & Tragwerksplanung | Prime Structures",
  desc="Tragwerksplanung für Umbau und Aufstockung eines Mehrfamilienhauses in Hanglage in Rüdersdorf bei Berlin, mit Wintergarten in Pfosten-Riegel-Bauweise."),

 dict(
  slug="daenenstrasse", name="Umnutzung Dänenstraße", cat="Bauen im Bestand",
  descriptor="Statik für neue Öffnungen in tragenden Wänden eines Altbau-Erdgeschosses.",
  hero="daenenstrasse-symbolbild.jpg", hero_w=1264, hero_h=848,
  hero_alt="Gründerzeit-Altbau in Berlin-Prenzlauer Berg mit umgenutztem Erdgeschoss",
  hero_caption="Gründerzeitquartier, Berlin-Prenzlauer Berg",
  facts=[("Projektart","Bauen im Bestand"),("Standort","Berlin-Prenzlauer Berg"),
         ("Bestand","Altbau vor 1918 · Mauerwerk"),
         ("Nutzung","24 Plätze · 6 rollstuhlgerecht"),
         ("Leistung","Statik für Öffnungen in tragenden Wänden"),("Status","Fertiggestellt")],
  aufgabe="Ein Altbau-Erdgeschoss, gebaut vor 1918. Aus der Kindertagesstätte sollte eine barrierefreie Wohneinrichtung werden. Barrierefrei heißt hier: breitere Wege durch tragende Wände.",
  loesung="Wir haben die Bestandslasten ermittelt, neue Öffnungen in tragenden Wänden nachgewiesen und bestehende Öffnungen verbreitert. Die Stahlstürze wurden für den vorhandenen Lastabtrag bemessen.",
  facts_big=[("24","Plätze · 6 rollstuhlgerecht")],
  scope=["Ermittlung der Bestandslasten","Nachweis neuer und verbreiterter Öffnungen",
         "Bemessung der Stahlstürze"],
  title="Umnutzung Dänenstraße Prenzlauer Berg — Statik Altbau | Prime Structures",
  desc="Statik für die Umnutzung eines Altbau-Erdgeschosses in Berlin-Prenzlauer Berg: neue Öffnungen in tragenden Wänden, Bestandslasten und Bemessung der Stahlstürze."),

 dict(
  slug="gewerbestandort-hennigsdorf", name="Gewerbestandort Hennigsdorf", cat="Gewerbe",
  descriptor="Tragwerksplanung für Lager, Büro und Wohnen unter einem Dach.",
  hero="gewerbestandort-hennigsdorf.jpg", hero_w=1800, hero_h=1207,
  hero_alt="Gewerbestandort Hennigsdorf — zweigeschossige Lagerhalle mit Büro- und Wohngeschoss",
  facts=[("Projektart","Gewerbe"),("Standort","Hennigsdorf"),
         ("Nutzung","Lager · Büro · Wohnen"),("Konstruktion","Massivbau mit Holzdach"),
         ("Leistung","Tragwerksplanung"),("Status","Fertiggestellt")],
  aufgabe="Ein Gewerbestandort entsteht: eine zweigeschossige Lagerhalle, im Obergeschoss Büro und Wohnung. Drei Nutzungen, ein Tragwerk.",
  loesung="Massivbau mit Holzdach: robust im Lagerbetrieb, wirtschaftlich im Bau, wohntauglich im Obergeschoss.",
  scope=["Tragwerksplanung Massivbau mit Holzdach"],
  title="Gewerbestandort Hennigsdorf — Tragwerksplanung Gewerbebau | Prime Structures",
  desc="Tragwerksplanung für einen Gewerbestandort in Hennigsdorf: zweigeschossige Lagerhalle mit Büro- und Wohnnutzung als Massivbau mit Holzdach."),

 dict(
  slug="lagerhalle-philipp-pforr-strasse", name="Lagerhalle Philipp-Pforr-Straße", cat="Gewerbe",
  descriptor="Neubau in Stahl und Standsicherheitsnachweise für den Bestand.",
  hero="halle-hennigsdorf.jpg", hero_w=2000, hero_h=1341,
  hero_alt="Neubau Lagerhalle und Bestandshalle in der Philipp-Pforr-Straße, Hennigsdorf",
  facts=[("Projektart","Gewerbe"),("Standort","Hennigsdorf"),
         ("Konstruktion","Stahlbau"),
         ("Leistung","Tragwerksplanung · Nachweise im Bestand"),("Status","Fertiggestellt")],
  aufgabe="Zwei Aufgaben an einem Standort: der Neubau einer zweigeschossigen Lagerhalle mit Büro- und Wohnnutzung — und die Umwandlung einer Bestandshalle zur KFZ-Werkstatt mit Lackiererei.",
  loesung="Für den Neubau: Tragwerksplanung in Stahl. Für den Bestand: Standsicherheitsnachweise inklusive Ersatzprofil-Nachrechnung — die vorhandene Konstruktion wurde rechnerisch belegt statt ersetzt.",
  scope=["Tragwerksplanung Stahlbau (Neubau)","Standsicherheitsnachweise der Bestandshalle",
         "Ersatzprofil-Nachrechnung","Standsicherheitserklärung","Schallschutznachweis"],
  title="Lagerhalle Philipp-Pforr-Straße Hennigsdorf — Statik Stahlbau | Prime Structures",
  desc="Neubau einer Lagerhalle in Stahl und Nutzungsänderung einer Bestandshalle in Hennigsdorf: Tragwerksplanung, Standsicherheitsnachweise und Ersatzprofil-Nachrechnung."),

 dict(
  slug="stahlhalle", name="Neubau Stahlhalle", cat="Gewerbe",
  descriptor="Komplette Tragwerksplanung einer Halle in Stahlbauweise.",
  hero="stahlhalle.jpg", hero_w=1150, hero_h=900,
  hero_alt="Neubau Stahlhalle mit Pultdach und mittigem Sektionaltor",
  facts=[("Projektart","Gewerbe"),
         ("Konstruktion","Eingespannte Stahlrahmen · Sandwichpaneele · Pultdach"),
         ("Leistung","Komplette Tragwerksplanung"),("Status","Fertiggestellt")],
  aufgabe="Eine eingeschossige Halle mit Pultdach, erschlossen über ein mittig im Giebel angeordnetes Sektionaltor. Große Öffnung, klare Spannweite, wirtschaftliche Konstruktion.",
  loesung="Eingespannte Stahlrahmen mit einbetonierten Stützen: Die Einspannung übernimmt die Aussteifung, die Fassade aus Sandwichpaneelen bleibt frei von Verbänden.",
  scope=["Komplette Tragwerksplanung","Eingespannte Stahlrahmen mit einbetonierten Stützen"],
  title="Neubau Stahlhalle — Tragwerksplanung Stahlbau | Prime Structures",
  desc="Komplette Tragwerksplanung einer eingeschossigen Stahlhalle mit Pultdach und Sandwichpaneel-Fassade: eingespannte Stahlrahmen mit einbetonierten Stützen."),

 dict(
  slug="doppelhaus-raabestrasse", name="Doppelhaus Raabestraße", cat="Neubau",
  descriptor="Tragwerksplanung für ein auskragendes Vordach in Stahlbeton.",
  hero="raabe-front.jpg", hero_w=2000, hero_h=666,
  hero_alt="Doppelhaus Raabestraße in Berlin — Frontansicht mit auskragendem Vordach",
  facts=[("Projektart","Neubau"),("Standort","Berlin"),
         ("Konstruktion","Stahlbeton-Filigranbauweise · Auskragendes Vordach"),
         ("Leistung","Tragwerksplanung"),("Status","Fertiggestellt")],
  aufgabe="Eine Doppelhaushälfte mit einem weit auskragenden Vordach. Die Auskragung ist das architektonische Motiv — und die statische Aufgabe.",
  loesung="Stahlbeton-Filigranbauweise: präzise Fertigteile, monolithisch ergänzt. Das Vordach kragt frei aus, ohne Stützen und ohne sichtbare Technik.",
  scope=["Tragwerksplanung in Stahlbeton-Filigranbauweise","Nachweis des auskragenden Vordachs"],
  gallery=[("raabe-hero.jpg",1050,667,"Doppelhaus Raabestraße — Nahansicht der Fassade mit auskragendem Vordach","wide")],
  title="Doppelhaus Raabestraße Berlin — Tragwerksplanung Neubau | Prime Structures",
  desc="Tragwerksplanung für eine Doppelhaushälfte in Berlin: Stahlbeton-Filigranbauweise mit weit auskragendem Vordach ohne Stützen."),

 dict(
  slug="villa-schulzendorf", name="Villa Schulzendorf", cat="Neubau",
  descriptor="Architektur und Tragwerksplanung für ein privates Wohnhaus.",
  hero="villa-schulzendorf.jpg", hero_w=1400, hero_h=733,
  hero_alt="Neubau Villa Schulzendorf — Straßenansicht des Wohnhauses",
  facts=[("Projektart","Neubau"),("Standort","Schulzendorf"),("Bauherr","Privat"),
         ("Leistung","Architektur und Tragwerksplanung")],
  note="Referenzprojekt aus dem Bestand der bisherigen Prime-Structures-Website. Weitere Projektdaten werden ergänzt.",
  scope=["Architektur","Tragwerksplanung"],
  title="Neubau Villa Schulzendorf — Architektur & Tragwerksplanung | Prime Structures",
  desc="Neubau einer Villa in Schulzendorf: Architektur und Tragwerksplanung aus einer Hand. Referenzprojekt von Prime Structures, Ingenieurbüro für Tragwerksplanung."),

 dict(
  slug="einfamilienhaus-1", name="Einfamilienhaus I", cat="Neubau",
  descriptor="Architektur und Tragwerksplanung für ein privates Einfamilienhaus.",
  hero="einfamilienhaus-1.jpg", hero_w=1400, hero_h=1050,
  hero_alt="Neubau Einfamilienhaus I — Ansicht des Wohnhauses mit Satteldach",
  facts=[("Projektart","Neubau"),("Bauherr","Privat"),
         ("Leistung","Architektur und Tragwerksplanung")],
  note="Referenzprojekt aus dem Bestand der bisherigen Prime-Structures-Website. Weitere Projektdaten werden ergänzt.",
  scope=["Architektur","Tragwerksplanung"],
  title="Neubau Einfamilienhaus I — Architektur & Tragwerksplanung | Prime Structures",
  desc="Neubau eines Einfamilienhauses: Architektur und Tragwerksplanung von Prime Structures, Ingenieurbüro für Tragwerksplanung in Berlin und Brandenburg."),

 dict(
  slug="wochenendhaus", name="Wochenendhaus", cat="Neubau",
  descriptor="Architektur und Tragwerksplanung für ein Wochenendhaus in Holzbauweise.",
  hero="wochenendhaus.jpg", hero_w=1400, hero_h=1107,
  hero_alt="Neubau Wochenendhaus — Visualisierung des holzverkleideten Baukörpers",
  hero_caption="Visualisierung",
  facts=[("Projektart","Neubau"),("Bauherr","Privat"),
         ("Leistung","Architektur und Tragwerksplanung")],
  note="Referenzprojekt aus dem Bestand der bisherigen Prime-Structures-Website. Die Darstellung ist eine Visualisierung; weitere Projektdaten werden ergänzt.",
  scope=["Architektur","Tragwerksplanung"],
  title="Neubau Wochenendhaus — Architektur & Tragwerksplanung | Prime Structures",
  desc="Neubau eines Wochenendhauses: Architektur und Tragwerksplanung von Prime Structures, Ingenieurbüro für Tragwerksplanung in Berlin und Brandenburg."),

 dict(
  slug="einfamilienhaus-2", name="Einfamilienhaus II", cat="Neubau",
  descriptor="Architektur und Tragwerksplanung für ein privates Einfamilienhaus.",
  hero="einfamilienhaus-2.jpg", hero_w=1400, hero_h=1150,
  hero_alt="Neubau Einfamilienhaus II — Ansicht mit Terrasse",
  facts=[("Projektart","Neubau"),("Bauherr","Privat"),
         ("Leistung","Architektur und Tragwerksplanung")],
  note="Referenzprojekt aus dem Bestand der bisherigen Prime-Structures-Website. Weitere Projektdaten werden ergänzt.",
  scope=["Architektur","Tragwerksplanung"],
  title="Neubau Einfamilienhaus II — Architektur & Tragwerksplanung | Prime Structures",
  desc="Neubau eines Einfamilienhauses: Architektur und Tragwerksplanung von Prime Structures, Ingenieurbüro für Tragwerksplanung in Berlin und Brandenburg."),
]

E = lambda t: html.escape(t, quote=True)


def head(p):
    url = "%s/projekt-%s.html" % (SITE, p["slug"])
    img = "%s/assets/%s" % (SITE, p["hero"])
    return f'''<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["desc"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Prime Structures">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{E(p["title"])}">
<meta property="og:description" content="{E(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(p["title"])}">
<meta name="twitter:description" content="{E(p["desc"])}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="assets/prime-structures-symbol-black.svg">
<link rel="preconnect" href="https://api.fontshare.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=general-sans@500,600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={CSS_V}">
</head>'''


HEADER = '''<a class="skip-link" href="#inhalt">Zum Inhalt springen</a>

<header class="site-header site-header--over">
  <div class="container header-inner">
    <a class="logo" href="index.html" aria-label="Prime Structures — Startseite">
      <img src="assets/prime-structures-lockup-black.svg" alt="Prime Structures">
    </a>
    <nav class="nav" aria-label="Hauptnavigation">
      <a href="index.html#leistungen">Leistungen</a>
      <a href="projekte.html" aria-current="page">Projekte</a>
      <a href="team.html">Über uns</a>
      <a href="index.html#kontakt">Kontakt</a>
    </nav>
    <a class="header-phone" href="tel:+4915227081206">+49 152 270 812 06</a>
    <a class="btn header-cta" href="index.html#kontakt">Projekt besprechen <span class="arr">→</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="mobile-menu">
      Menü <span class="bars" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>
  </div>
</header>

<div class="mobile-menu" id="mobile-menu">
  <nav aria-label="Mobile Navigation">
    <a href="projekte.html" aria-current="page">Projekte</a>
    <a href="index.html#leistungen">Leistungen</a>
    <a href="team.html">Über uns</a>
    <a href="index.html#kontakt">Kontakt</a>
  </nav>
  <div class="mobile-menu-foot">
    <a class="phone-big" href="tel:+4915227081206">+49 152 270 812 06</a>
    <a class="btn btn--light" href="index.html#kontakt">Projekt besprechen <span class="arr">→</span></a>
  </div>
</div>'''

FOOTER = open("_footer.part").read() if os.path.exists("_footer.part") else ""


def page(p, prev, nxt):
    o = io.StringIO()
    w = o.write
    w("<!DOCTYPE html>\n<html lang=\"de\">\n%s\n<body>\n%s\n\n<main id=\"inhalt\">\n" % (head(p), HEADER))

    # --- HERO: photograph + project identity ------------------------------
    cap = p.get("hero_caption")
    w(f'''
  <!-- Hero: the photograph carries the page; identity sits on the plate -->
  <section class="pp-hero">
    <figure class="pp-hero-img">
      <img src="assets/{p["hero"]}" alt="{E(p["hero_alt"])}" width="{p["hero_w"]}" height="{p["hero_h"]}" fetchpriority="high">
    </figure>
    <i class="pp-hero-veil" aria-hidden="true"></i>
    <div class="container pp-hero-id">
      <p class="p-kicker">{E(p["cat"])}</p>
      <h1 class="pp-title">{E(p["name"])}<span class="dot">.</span></h1>
      <p class="pp-descriptor">{E(p["descriptor"])}</p>
    </div>
  </section>
''')
    if cap:
        w(f'  <p class="container pp-hero-caption caption">{E(cap)}</p>\n')

    # --- FACTS -------------------------------------------------------------
    w('\n  <section class="section--tight pp-facts">\n    <div class="container">\n')
    w('      <div class="pp-facts-head reveal"><p class="label">Projektdaten</p><i class="pp-rule" aria-hidden="true"></i></div>\n')
    w('      <dl class="data-strip reveal d1">\n')
    for k, v in p["facts"]:
        w(f'        <div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>\n')
    w('      </dl>\n    </div>\n  </section>\n')

    # --- STORY -------------------------------------------------------------
    if p.get("aufgabe"):
        big = p.get("facts_big") or []
        w('\n  <section class="section dossier-section">\n    <div class="container grid aufgabe-grid">\n')
        w('      <div class="aufgabe-txt">\n        <p class="label reveal">Die Aufgabe</p>\n')
        w(f'        <p class="lede reveal d1">{E(p["aufgabe"])}</p>\n      </div>\n')
        if big:
            w(f'      <div class="aufgabe-fact reveal d2"><p class="fact">{E(big[0][0])}</p><p class="label fact-label">{E(big[0][1])}</p></div>\n')
        w('    </div>\n  </section>\n')

        w('\n  <section class="section--tight dossier-section">\n    <div class="container grid loesung-grid">\n')
        w('      <div class="loesung-txt">\n        <p class="label reveal">Die Lösung</p>\n')
        w(f'        <p class="lede reveal d1">{E(p["loesung"])}</p>\n      </div>\n')
        if len(big) > 1:
            w(f'      <div class="loesung-fact reveal d2"><p class="fact">{E(big[1][0])}</p><p class="label fact-label">{E(big[1][1])}</p></div>\n')
        w('    </div>\n  </section>\n')

    if p.get("note"):
        w(f'\n  <section class="section--tight dossier-section">\n    <div class="container">\n      <p class="kompakt-note reveal">{E(p["note"])}</p>\n    </div>\n  </section>\n')

    # --- DIAGRAMS (real project material, Friedbergstraße only) -----------
    if p.get("diagrams") and DIAGRAMS:
        w('\n  <section class="section dossier-section band-blueprint">\n    <div class="container">\n')
        w(f'      <p class="label reveal">{E(p["diagrams_label"])}</p>\n      {DIAGRAMS}\n    </div>\n  </section>\n')

    # --- GALLERY -----------------------------------------------------------
    if p.get("gallery"):
        w('\n  <section class="section--tight pp-gallery">\n    <div class="container">\n')
        w('      <div class="pp-facts-head reveal"><p class="label">Weitere Ansichten</p><i class="pp-rule" aria-hidden="true"></i></div>\n')
        w('      <div class="pp-gallery-grid">\n')
        for src, gw, gh, alt, shape in p["gallery"]:
            w(f'        <figure class="pp-shot pp-shot--{shape} reveal"><img src="assets/{src}" alt="{E(alt)}" width="{gw}" height="{gh}" loading="lazy"></figure>\n')
        w('      </div>\n    </div>\n  </section>\n')

    # --- SCOPE -------------------------------------------------------------
    if p.get("scope"):
        w('\n  <section class="section--tight dossier-section">\n    <div class="container">\n')
        w('      <div class="pp-facts-head reveal"><p class="label">Die Leistung</p><i class="pp-rule" aria-hidden="true"></i></div>\n')
        w('      <ul class="scope-list">\n')
        for i, li in enumerate(p["scope"]):
            w(f'        <li class="reveal{" d"+str(min(i,3)) if i else ""}">{E(li)}</li>\n')
        w('      </ul>\n    </div>\n  </section>\n')

    # --- HANDOFF: CTA + three-way project navigation ----------------------
    w(f'''
  <section class="section pp-handoff">
    <div class="container">
      <h2 class="h2 reveal">Ähnliches Vorhaben?</h2>
      <a class="btn reveal d1" href="index.html#kontakt">Projekt besprechen <span class="arr">→</span></a>

      <nav class="pp-nav reveal d2" aria-label="Weitere Projekte">
        <a class="pp-nav-prev" href="projekt-{prev["slug"]}.html" rel="prev">
          <span class="label">← Voriges Projekt</span>
          <span class="title">{E(prev["name"])}</span>
        </a>
        <a class="pp-nav-all" href="projekte.html">
          <span class="label">Übersicht</span>
          <span class="title">Alle Projekte</span>
        </a>
        <a class="pp-nav-next" href="projekt-{nxt["slug"]}.html" rel="next">
          <span class="label">Nächstes Projekt →</span>
          <span class="title">{E(nxt["name"])}</span>
        </a>
      </nav>
    </div>
  </section>
''')

    # --- CONTACT (links to the single contact system on the homepage) -----
    w('''
  <section class="section k-section" id="kontakt">
    <div class="container grid k-grid">
      <div class="k-main">
        <p class="label reveal">Kontakt</p>
        <h2 class="k-statement reveal d1">Erzählen Sie uns von Ihrem Projekt.</h2>
        <a class="k-phone reveal d2" href="tel:+4915227081206">+49 152 270 812 06</a>
        <p class="k-meta reveal d3">Mo–Fr · 9–19 Uhr · Sie sprechen direkt mit dem Ingenieur.</p>
      </div>
      <div class="k-side reveal d2">
        <p class="k-strip">Anfrage <span class="sep">→</span> Ersteinschätzung <span class="sep">→</span> Angebot <span class="sep">→</span> Nachweis</p>
        <a class="btn" href="index.html#kontakt">Projekt besprechen <span class="arr">→</span></a>
      </div>
    </div>
  </section>

</main>
''')
    w("\n" + FOOTER + "\n")
    w('<script src="main.js?v=%s"></script>\n</body>\n</html>\n' % JS_V)
    return o.getvalue()


if __name__ == "__main__":
    n = len(PROJECTS)
    for i, p in enumerate(PROJECTS):
        out = page(p, PROJECTS[(i - 1) % n], PROJECTS[(i + 1) % n])
        fn = "projekt-%s.html" % p["slug"]
        open(fn, "w").write(out)
        print("  wrote %-46s %6d bytes  facts=%d scope=%d gallery=%d" % (
            fn, len(out), len(p["facts"]), len(p.get("scope") or []), len(p.get("gallery") or [])))
    print("\n%d project pages generated." % n)
