# Agenten-System „Kurz erklärt: Alltag"

Jeder Agent ist eine geplante Aufgabe in der Cloud. Er startet ohne Gedächtnis, liest den Stand aus diesem Repository
(GitHub: Kurz-erklaert/Kurz-erklaert, Zweig main) und schreibt nur seine eigenen Dateien zurück. Die Dateien sind die Übergabe zwischen den Agenten.

## Rollen und Takt (deutsche Zeit)

| Agent | Takt | Liest | Schreibt (nur diese Dateien!) |
|---|---|---|---|
| Wächter | täglich 21:41 | posted.json, queue.json, insights.json, GitHub-Läufe | status.json |
| Analyst | Mo + Do 10:17 | insights.json, queue.json, posted.json | Projekt-Doc `claude/auswertung.md` (kein Repo-Schreiben) |
| Manager | Mo 11:23 | status.json, auswertung.md (Projekt), queue.json, plan/ | strategie.md, plan/auftrag.json |
| Skript-Autor | Di + Fr 10:31 | strategie.md, plan/auftrag.json, plan/themen.json, agenten/skript-regeln.md | plan/skripte/*.json (neu), plan/themen.json |
| Faktenprüfer | Di + Fr 12:47 | plan/skripte/*.json (Status „skript") | dieselben Skript-Dateien (nur Felder status, faktencheck, quellen) |
| Veröffentlichung | täglich 8:00 + 18:30 | queue.json, posted.json | posted.json (GitHub Action, keine KI) |
| Produzent | wöchentlich, mit dem Nutzer in einer Sitzung | geprüfte Skripte | videos/, queue.json |

## Regeln für alle Agenten

1. Vor dem Schreiben immer `git fetch` und `git rebase origin/main`, dann kleine Commits, dann `git push`. Bei Konflikt erneut rebasen. Der Bot schreibt parallel posted.json und insights.json.
2. Nur die eigenen Dateien schreiben (Tabelle oben). Niemals queue.json, posted.json, insights.json, videos/ oder .github/ ändern, außer die Rolle erlaubt es ausdrücklich.
3. Keine Schlüssel, Tokens oder Passwörter in Dateien oder Nachrichten.
4. Keine erfundenen Zahlen. Fehlt etwas, steht „fehlt" in der Datei.
5. Der Nutzer will nur bei Problemen oder Entscheidungen hören. Kurze Meldung (höchstens 6 Zeilen) per Nachricht, sonst still bleiben.
6. Entscheidungen des Nutzers gelten: keine medizinischen Ratschläge, genau 5 Hashtags, Veröffentlichung ohne Vorab-Prüfung (darum ist der Faktenprüfer die einzige Kontrolle), keine realistischen KI-Videos.
7. Der Stil (flach oder 3D) wird durch den Stil-Test entschieden (siehe strategie.md).

## Dateien

- strategie.md: Strategie und aktueller Standard (Manager)
- plan/auftrag.json: Auftrag des Managers an den Skript-Autor
- plan/themen.json: Themenliste mit Status, bereits genutzte Themen (Skript-Autor)
- plan/skripte/*.json: ein Skript je Video, Format siehe agenten/skript-regeln.md
- status.json: Gesundheitszustand (Wächter)
- Beispiel: agenten/beispiel_skript.json. Prüfen: python3 agenten/pruefe_skript.py [datei]

## Erweiterung (27.11.)
- **Qualitätsprüfung & Lautstärke (Pflicht in der Produktion):** jedes fertige Video vor dem Einreihen mit `python3 agenten/pruefe_video.py <datei>` prüfen und mit `python3 agenten/normalisiere_ton.py <datei>` auf ca. -16 LUFS bringen. Fehler = nicht einreihen.
- **Saison-Planer** (mittwochs): schreibt `plan/saison_themen.json` (Themen 2–4 Wochen vor dem Anlass). Der Skript-Autor bevorzugt fällige Saisonthemen.
- **Recycling-Agent** (monatlich): schreibt `plan/recycling.json` (Reels ≥42 Tage alt mit guten Zahlen, neuer Hook/Winkel, nie identisch). Der Autor darf pro Lauf 1 Skript daraus machen.
- **Community-Agent** (täglich nach Kennzahlen): schreibt NUR Antwortvorschläge nach `plan/antworten.json`. Er antwortet nie selbst auf Instagram.
- **Experiment-Planer** (Teil des Managers): immer nur EINE Variable gleichzeitig (Stil, Hook, Uhrzeit, Länge, Thema), Gruppen ausgewogen, Ergebnis erst ab n≥6 pro Gruppe und ≥72 h Laufzeit als Tendenz, ab n≥10 als Entscheidung.
- **Wächter** prüft zusätzlich: ElevenLabs-Guthaben, ob Kennzahlen-Läufe fehlschlagen (= Token-Problem, Meta-Token läuft ca. alle 60 Tage ab), ob geplante Post-Läufe stattfinden.
- Dateibesitz neu: Saison-Planer `plan/saison_themen.json`; Recycling `plan/recycling.json`; Community `plan/antworten.json`.

## Stil-Werte (seit 27.11.)
`stil` in queue.json, Skripten und plan/auftrag.json hat drei Werte: `flat` (hell), `flat-dunkel` (flach auf Schwarz, Generator `pipeline/genvid2_dark.py`, Cover `pipeline/cover.py … dark`), `3d`. Der Manager darf `stil` in plan/auftrag.json auf jeden dieser Werte setzen, passend zur Empfehlung des Analysten (z. B. „flat-dunkel als Standard"). Test läuft: 4 Videos `flat-dunkel` (d2_*), 2 Videos `3d`, Rest `flat`.

## Regel-Beobachter (monatlich, 15.)
Prüft Plattform-/Rechtsregeln (Instagram, Meta-KI-Label, YouTube, TikTok, KI-VO, Werbekennzeichnung) gegen `plan/regeln_stand.json`, schreibt nur diese Datei und meldet dem Nutzer nur wesentliche Änderungen. Saison-Planer macht zusätzlich kostenlose Trend-Recherche per Websuche (kein Apify/Firecrawl, keine Zusatzkosten).

Zusätzlich lesen: `agenten/leitlinien.md` (Caption-SEO, Hook-Regeln, Experiment-Regeln). Alle Agenten halten sich daran.

## Namen
Jeder Eintrag in queue.json hat ein Feld `name` (kurzer, eindeutiger Themenname wie „Heizung entlüften"). Wer ein Video einreiht, setzt es. Die Excel-Auswertung zeigt diesen Namen.
