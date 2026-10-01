# Zahlen_Raten

Miniprojekt im **Lernfeld 10a - Benutzerschnittstellen gestalten und entwickeln**.

Eine **barrierefreie Flask-Webanwendung**, mit der man das Spiel „Zahlen raten" gegen den
Computer spielt. Spielername und Anzahl der Rateversuche werden dauerhaft in einer Datenbank
gespeichert und als Highscore-Liste angezeigt.

---

## Inhaltsverzeichnis

- [Auftrag](#auftrag)
- [Spielregeln](#spielregeln)
- [Team](#team)
- [Zeitplan](#zeitplan)
- [Vorgehensmodell](#vorgehensmodell)
- [Anforderungen](#anforderungen)
- [Barrierefreiheit](#barrierefreiheit)
- [Technischer Aufbau](#technischer-aufbau)
- [Entwicklungsumgebung einrichten](#entwicklungsumgebung-einrichten)
- [Arbeiten im Repository](#arbeiten-im-repository)
- [Kostenkalkulation](#kostenkalkulation)
- [Abzugebende Artefakte](#abzugebende-artefakte)
- [Präsentationen](#präsentationen)
- [Quellen](#quellen)

---

## Auftrag

Das Spiel „Zahlen raten" ist als barrierefreie Flask-Webanwendung im Team (3-4 Personen)
umzusetzen. Neben der lauffähigen Anwendung gehören eine Anforderungsanalyse, ein Mockup der
Benutzeroberfläche, ein Aktivitätsdiagramm, eine Kostenkalkulation sowie zwei Präsentationen
zum Projektumfang.

## Spielregeln

1. Der Computer denkt sich eine ganze Zahl zwischen **0 und 100** aus.
2. Der Spieler gibt seinen Namen ein und rät die Zahl.
3. Nach jedem Versuch meldet die Anwendung, ob die geratene Zahl **zu groß** oder **zu klein** ist.
4. Ist die Zahl erraten, werden **Spielername und Anzahl der Versuche** in der Datenbank gespeichert.
5. Die Bestenliste wird **zu Beginn und am Ende** des Spiels ausgelesen und angezeigt.

---

## Team

| Name                | GitHub                                               | Rolle       |
| ------------------- | ---------------------------------------------------- | ----------- |
| Jan-Timothy Beckord | [@SuT-JTB](https://github.com/SuT-JTB)               | Entwicklung |
| Daniel Haas         | [@AlterErntshaft](https://github.com/AlterErntshaft) | Entwicklung |
| Simon               | [@Loafiie](https://github.com/Loafiie)               | Entwicklung |

> Rollen noch festlegen, z. B. Product Owner, Scrum Master, Entwicklung, Dokumentation/Präsentation.

---

## Zeitplan

| Termin     | Inhalt                                                                         | Status |
| ---------- | ------------------------------------------------------------------------------ | ------ |
| **23.09.** | Projektstart, Teambildung, Auftrag verstehen                                   | ✅     |
| **30.09.** | Anforderungsermittlung, Mockup, Aktivitätsdiagramm, Repo-Setup                 | 🔄     |
| **07.10.** | **Zwischenpräsentation** (5 Min.) - Benutzerschnittstelle + Aktivitätsdiagramm | ⬜     |
| **14.10.** | Implementierung, Kostenkalkulation, Test                                       | ⬜     |
| _n. n._    | **Abschlusspräsentation** (max. 15 Min.)                                       | ⬜     |

### Meilensteine bis zur Zwischenpräsentation (07.10.)

- [ ] Funktionale und nicht funktionale Anforderungen vollständig erfasst
- [ ] Mockup der Benutzeroberfläche (alle Screens)
- [ ] Aktivitätsdiagramm mit Swimlanes **User** und **Webanwendung**
- [ ] Präsentationsfolien (5 Min.)

### Meilensteine bis zur Abschlusspräsentation

- [ ] Lauffähige Flask-Anwendung inkl. Datenbank
- [ ] Barrierefreiheit geprüft (WAVE / Lighthouse / Screenreader)
- [ ] Kostenkalkulation mit Break-Even
- [ ] Abschlusspräsentation (max. 15 Min.)

---

## Vorgehensmodell

Realisierung in einem **agilen Team nach Scrum**:

- **Product Backlog** - alle Anforderungen als Epics und User Stories aus Benutzersicht
  („Als _Spieler_ möchte ich _…_, um _…_").
- **Sprints** - entlang der Wochentakte des Zeitplans.
- **Sprint Planning / Review** - jeweils zu Beginn und Ende einer Unterrichtseinheit.
- **Priorisierung** - Anforderungen nach Wichtigkeit ordnen, damit früh ein vorzeigbares
  Ergebnis existiert.

Das Product Backlog wird über **GitHub Issues** geführt, der Sprintfortschritt optional über ein
GitHub Project Board.

---

## Anforderungen

Nach LF10a werden Anforderungen in **funktionale** (_was_ das System leisten soll) und
**nicht funktionale** (_wie_ es die Leistung erbringen soll) unterteilt. Nicht funktionale
Anforderungen gliedern sich weiter in **Qualitätsanforderungen** und **Randbedingungen**.

### Funktionale Anforderungen

| ID  | Anforderung                                                                | Priorität |
| --- | -------------------------------------------------------------------------- | --------- |
| F1  | Spieler kann seinen Namen eingeben                                         | Muss      |
| F2  | System erzeugt eine Zufallszahl zwischen 0 und 100                         | Muss      |
| F3  | Spieler kann eine Zahl eingeben und absenden                               | Muss      |
| F4  | System meldet „zu groß" / „zu klein" / „richtig"                           | Muss      |
| F5  | System zählt die Rateversuche                                              | Muss      |
| F6  | System speichert Name + Versuche in der Datenbank                          | Muss      |
| F7  | Bestenliste wird zu Spielbeginn angezeigt                                  | Muss      |
| F8  | Bestenliste wird am Spielende angezeigt                                    | Muss      |
| F9  | Spieler kann ein neues Spiel starten                                       | Muss      |
| F10 | Fehlerhafte Eingaben (leer, keine Zahl, außerhalb 0-100) werden abgefangen | Muss      |
| F11 | Spielstand bleibt über die Session erhalten                                | Muss      |

> Liste ist ein Startpunkt und im Team zu vervollständigen und zu priorisieren.

### Nicht funktionale Anforderungen

**Qualitätsanforderungen**

- **Benutzbarkeit** - Selbstbeschreibungsfähigkeit (jeder Screen erklärt sich selbst),
  Erwartungskonformität (Bedienung folgt gewohnten Web-Mustern).
- **Zuverlässigkeit** - Fehlertoleranz der Benutzerschnittstelle: ungültige Eingaben führen zu
  einer verständlichen Meldung, nie zu einem Absturz oder Serverfehler.
- **Effizienz** - schlanke Seiten, keine unnötigen Ressourcen; Antwortzeit spürbar sofort.

**Randbedingungen**

- **Grad der Barrierefreiheit** - Ziel: WCAG 2.0 Level AA (siehe unten).
- **Endgeräte** - Desktop und Smartphone; Layout muss ab **320 px** Breite funktionieren.
- **Browser** - aktuelle Versionen von Firefox, Chrome und Edge.
- **Technologie** - Python 3 mit Flask, Datenhaltung in SQLite.

### Anforderungen an die Benutzerschnittstelle

- Bedienbarkeit per **Maus, Tastatur und Screenreader** - vollständige Tastatursteuerung.
- Ausreichend große Schaltflächen für motorisch eingeschränkte Nutzer.
- Textgröße durch den Nutzer auf das Doppelte vergrößerbar, ohne dass das Layout bricht.

---

## Barrierefreiheit

Leitlinie sind die **WCAG 2.0**, auf die sich auch die deutsche **BITV** stützt. Eine Website muss
demnach **wahrnehmbar, bedienbar, verständlich und robust** sein.

### Konkrete Umsetzung im Projekt

**Wahrnehmbar**

- Jedes `<img>` bekommt ein `alt`-Attribut; rein dekorative Bilder erhalten `alt=""`.
- Kontrastverhältnis mindestens **4,5:1** für Fließtext und **3:1** für große Schrift.
- Keine Information ausschließlich über Farbe transportieren - „zu groß" / „zu klein" wird als
  **Text** ausgegeben, nicht nur als rotes bzw. grünes Feld.
- Schriftgröße nicht unter 12 px.

**Bedienbar**

- Semantisch korrektes HTML: echte `<button>`- und `<form>`-Elemente statt klickbarer `<div>`s.
- Sichtbarer Fokusindikator, sinnvolle Tab-Reihenfolge.
- Das Spiel ist vollständig ohne Maus spielbar.

**Verständlich**

- Klare Überschriftenhierarchie (`<h1>` … `<h3>`) ohne Sprünge.
- Jedes Eingabefeld hat ein verknüpftes `<label>`.
- Fehlermeldungen sagen, **was** falsch war und **wie** es richtig geht.
- Einfache, kurze Sprache; `lang="de"` am `<html>`-Element.

**Robust**

- ARIA nur **ergänzend**, nicht als Ersatz für Semantik - keine doppelten Rollen
  (`<button role="button">` ist überflüssig, `<h3 role="button">` ist falsch).
- Dynamische Rückmeldungen nach einem Rateversuch über eine **ARIA-Live-Region**, damit
  Screenreader die Antwort vorlesen, ohne dass der Fokus springt.
- Responsives Layout, das auch bei 400 % Zoom nutzbar bleibt.

### Prüfwerkzeuge

| Werkzeug                                           | Zweck                                        |
| -------------------------------------------------- | -------------------------------------------- |
| **WAVE** (Browser-Erweiterung)                     | Barrieren aller Art in einer Seite aufspüren |
| **Lighthouse** (in Chromium integriert)            | Automatisierter Accessibility-Score          |
| **contrastchecker.com** / Color Contrast Analyzer  | Kontrastverhältnisse prüfen                  |
| **Accessibility Tree** (Firefox / Chrome DevTools) | Seite so sehen, wie Screenreader sie „sehen" |
| **NVDA** (kostenlos) oder Windows-Sprachausgabe    | Echter Screenreader-Test                     |
| **HeadingsMap**                                    | Überschriften-Hierarchie prüfen              |

---

## Technischer Aufbau

| Bereich             | Technologie                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| Sprache             | Python 3.14                                                                         |
| Webframework        | Flask                                                                               |
| Templates           | Jinja2                                                                              |
| Datenbank           | SQLite (`sqlite3` oder SQLAlchemy)                                                  |
| Zustand pro Spieler | Flask-Session                                                                       |
| Styling             | CSS (ohne schweres Framework, um Kontrolle über Kontraste und Semantik zu behalten) |

### Geplante Projektstruktur

```
Zahlen_Raten/
├── app.py                 # Flask-Anwendung, Routen
├── db.py                  # Datenbankzugriff
├── schema.sql             # Tabellendefinition
├── requirements.txt       # Abhängigkeiten
├── static/
│   └── style.css
├── templates/
│   ├── base.html          # Grundgerüst, lang="de", Skip-Link
│   ├── index.html         # Namenseingabe + Bestenliste
│   ├── game.html          # Rateformular + Rückmeldung
│   └── result.html        # Ergebnis + Bestenliste
└── docs/
    ├── anforderungen.md
    ├── mockup/
    ├── aktivitaetsdiagramm/
    └── kostenkalkulation.md
```

> Struktur ist ein Vorschlag und wird bei der Umsetzung angepasst.

### Datenmodell (Entwurf)

Tabelle `highscore`:

| Spalte      | Typ                 | Beschreibung               |
| ----------- | ------------------- | -------------------------- |
| `id`        | INTEGER PRIMARY KEY | Fortlaufende ID            |
| `name`      | TEXT NOT NULL       | Spielername                |
| `versuche`  | INTEGER NOT NULL    | Anzahl der Rateversuche    |
| `zeitpunkt` | TEXT                | Zeitstempel des Spielendes |

---

## Entwicklungsumgebung einrichten

Flask installieren:

```bash
py -m pip install flask
```

Anwendung im Debug-Modus starten (im Ordner des Flask-Projekts):

```bash
py -m flask run --debug
```

Im Debug-Modus wird die `.py`-Datei automatisch neu geladen - ein Neustart des Servers nach
Änderungen ist nicht nötig. Außerdem lassen sich Debug-Nachrichten ausgeben:

```python
app.logger.debug('fetching highscores from db')
```

Die Anwendung läuft anschließend auf <http://127.0.0.1:5000>.

---

## Arbeiten im Repository

- `main` bleibt jederzeit lauffähig.
- Änderungen über Feature-Branches: `feature/<kurzbeschreibung>`, z. B. `feature/highscore-db`.
- Pull Request stellen und von einem Teammitglied gegenlesen lassen, bevor nach `main` gemergt wird.
- Aussagekräftige Commit-Nachrichten auf Deutsch oder Englisch - aber einheitlich.

> Verbindlich festzulegen - aktuell committen alle direkt auf `main`.

---

## Kostenkalkulation

Zu erstellen sind **Entwicklungskosten**, **Verkaufserlös** und **Break-Even-Punkt**.

**Entwicklungskosten**

| Position                        | Aufwand | Stundensatz | Kosten     |
| ------------------------------- | ------- | ----------- | ---------- |
| Anforderungsanalyse             | _TODO_  | _TODO_      | _TODO_     |
| UI-Konzept & Mockup             | _TODO_  | _TODO_      | _TODO_     |
| Implementierung                 | _TODO_  | _TODO_      | _TODO_     |
| Test & Barrierefreiheitsprüfung | _TODO_  | _TODO_      | _TODO_     |
| Dokumentation & Präsentation    | _TODO_  | _TODO_      | _TODO_     |
| **Summe**                       |         |             | **_TODO_** |

**Verkaufserlös** - Preis pro verkaufter Lizenz bzw. Einheit: _TODO_

**Break-Even** - Absatzmenge, ab der die Entwicklungskosten gedeckt sind:

```
Break-Even-Menge = Entwicklungskosten / (Verkaufspreis − variable Stückkosten)
```

Ergebnis: _TODO_

---

## Abzugebende Artefakte

| Artefakt              | Beschreibung                                                 | Status |
| --------------------- | ------------------------------------------------------------ | ------ |
| Anforderungskatalog   | Funktionale und nicht funktionale Anforderungen, priorisiert | ⬜     |
| Mockup                | Entwurf der Benutzeroberfläche, barrierefrei und ergonomisch | ⬜     |
| Aktivitätsdiagramm    | Abläufe mit Swimlanes **User** und **Webanwendung**          | ⬜     |
| Flask-Anwendung       | Lauffähiges Spiel inkl. Datenbank                            | ⬜     |
| Kostenkalkulation     | Entwicklungskosten, Verkaufserlös, Break-Even                | ⬜     |
| Zwischenpräsentation  | 5 Minuten                                                    | ⬜     |
| Abschlusspräsentation | max. 15 Minuten                                              | ⬜     |

---

## Präsentationen

### Zwischenpräsentation - 07.10., 5 Minuten

Vorzustellen sind:

- die **Benutzerschnittstelle** (Mockup)
- das **Aktivitätsdiagramm**

### Abschlusspräsentation - max. 15 Minuten

Aufbereitung der gesamten Projektergebnisse:

- Auftrag und Anforderungen
- Benutzerschnittstelle und Umsetzung der Barrierefreiheit
- Live-Demo der Anwendung
- Vorgehen im Team (Scrum)
- Kostenkalkulation und Break-Even
- Fazit und Ausblick

---

## Quellen

- **Aufgabenstellung** - `Zahlen raten - Miniprojekt.docx`
- **Anforderungen** - `Anforderungen.pdf` (LF10a, Kapitel 1.1.3 „Anforderungskatalog erstellen")
- **Barrierefreiheit** - Herbert Braun: _Web ohne Hürden - Websites barrierearm gestalten, 1. Teil_,
  c't 14/2022, S. 136-139
  ([SharePoint](https://tbseins-my.sharepoint.com/:b:/g/personal/bakera_tbs1_de/EWdxzNN7dipOooJGaOjdxJQB9RxBcU1tM_5zBzxOVujjcw?e=dw2aRh))
- **Interaktionsprinzipien** - `Benutzerschnittstellen.pdf`
- **Flask-Sessions** - <https://flask.palletsprojects.com/en/stable/quickstart/#sessions>
- **WCAG 2.0 / Werkzeuge** - <https://ct.de/yjp2>
