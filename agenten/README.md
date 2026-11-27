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
