# Regeln für Skripte, Captions und Faktenprüfung

## Kanal
„Kurz erklärt: Alltag", deutsche Reels (Instagram short.wissen.to_go), Du-Form, ohne Person im Bild, Stimme ElevenLabs „Jones". Länge 24 bis 32 Sekunden gesprochen, das sind 55 bis 80 Wörter in den 7 Szenen zusammen. Ton: freundlich, klar, ohne Show.

## Themenwahl
- Alltagswissen mit Warum und drei konkreten Tipps: Haushalt, Küche, Technik, Energie sparen, Wohnen, Körper-Alltag (nur harmlos und unkritisch).
- Muss in einfachen, bildbaren Objekten zeigbar sein (Kaffeemaschine, Fenster, Steckdose, Pfanne, Kühlschrank ...). Keine Menschen im Fokus.
- Keine Duplikate: plan/themen.json beachten. Mindestens 4 Wochen Abstand zum selben Oberthema.
- Verboten: medizinische Ratschläge, Diagnosen, Medikamente, Nahrungsergänzung, Diäten, Geld- und Anlagetipps, rechtliche Beratung, Sicherheitskritisches ohne Warnhinweis (Strom, Gas, Chemikalien mischen), Politik, Marken im Vergleich, Gerüchte ohne Beleg.

## Aufbau der 7 Szenen
0. Hook (2 Zeilen). Variante A, Fehler-Hook: „Dieser Fehler macht dein/deine X Y." Variante B, Versprechen-Hook: „So wird dein X in Y wieder Z." Der Hook muss wahr sein und gehalten werden.
1. Ursache in einem Satz (2 Zeilen).
2. Warum es passiert, zweiter Satz, dann „Drei Schritte/Tricks/Dinge helfen." (bis 3 Zeilen).
3. „Erstens: ..." (2 Zeilen)
4. „Zweitens: ..." (2 Zeilen)
5. „Drittens: ..." (2 Zeilen)
6. „Merk dir:" plus drei Stichwörter (2 Zeilen), z. B. „Tuch, öffnen, Druck prüfen."
Eine Zeile höchstens 38 Zeichen (Ausnahme Szene 2, bis 52). Keine Auslassungspunkte, keine Emojis im Videotext, Zahlen als Zahl oder Wort ohne Sonderzeichen.
schluesselwoerter: pro Szene 1 bis 3 Wörter, die farbig hervorgehoben werden (exakt wie im Text geschrieben, ohne Satzzeichen außer Punkt am Ende, wenn dort einer steht). merksatz_woerter: die drei Stichwörter aus Szene 6 (exakt wie dort).

## Caption
Vier Zeilen: (1) Hook-Satz plus ein passendes Emoji und kurze Ursache, (2) die drei Tipps als Stichworte mit je einem Emoji, bei Sicherheitsthemen ein kurzer Warnhinweis, (3) eine Frage an die Zuschauer mit 👇, (4) genau 5 Hashtags: 2 Themen-Hashtags, #alltagswissen, #kurzwissen und ein weiterer passender (z. B. #küchentipps, #haushaltstipps, #technikerklärt, #energiesparen). Keine Hashtags im Text davor.

## Skript-Datei (plan/skripte/<id>.json)
id: s3_NN_stichwort (fortlaufend, Staffel 3 beginnt bei s3_01; Zähler = höchste vorhandene Nummer + 1)
```
{
 "id": "s3_01_stichwort",
 "thema": "Kurzname des Themas",
 "kategorie": "Haushalt|Küche|Technik|Energie|Wohnen",
 "variante": "A|B",
 "stil": "flat|3d",
 "scenes": [ {"zeilen": ["...", "..."], "schluesselwoerter": ["..."]}, ... genau 7 ],
 "merksatz_woerter": ["...", "...", "..."],
 "bildideen": ["je Szene eine kurze Beschreibung des zu zeigenden Objekts/der Animation (7 Einträge)"],
 "caption": "...",
 "quellen": [],
 "status": "skript",
 "faktencheck": {"ergebnis": "", "notizen": "", "geprueft_am": ""},
 "erstellt_am": "JJJJ-MM-TT"
}
```
Statuswerte: skript → (Faktenprüfer) geprueft | ueberarbeiten | abgelehnt → (Produzent) produziert.

## Faktenprüfer
- Jede einzelne Tatsachenbehauptung (Ursache, jeder der drei Tipps) per Websuche gegen mindestens eine verlässliche Quelle prüfen (Behörden, Verbraucherzentralen, Hersteller, Universitäten, Fachverbände, seriöse Fachmedien). Keine Foren, keine Content-Farmen. Gerüchte-Tipps (zum Beispiel „Zahnpasta gegen Kratzer") nicht durchwinken.
- ok: alles belegt, Aussagen nicht stärker als die Quelle. Quellen mit Titel und URL in „quellen" eintragen.
- ueberarbeiten: kleine Korrektur möglich (Wortwahl, Einschränkung ergänzen). Der Prüfer darf die Texte selbst abschwächen oder korrigieren, aber nur im Rahmen der Regeln oben, und trägt die Änderung in notizen ein. Nach der Korrektur ergebnis „ok".
- abgelehnt: nicht belegbar, riskant oder medizinisch. Grund in notizen, Thema in plan/themen.json auf „abgelehnt" setzen.
- Sicherheitsrelevantes (Strom, Gas, Heizungsanlage, Chemikalien, Druck) braucht einen Warnhinweis in der Caption („Bei Unsicherheit Fachbetrieb fragen") und passende Formulierung („meist", „in der Regel").
