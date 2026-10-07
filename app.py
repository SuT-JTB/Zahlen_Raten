"""Zahlen raten – Flask-Anwendung mit Routen und Spiellogik."""

import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for

import db

MIN_ZAHL = 0
MAX_ZAHL = 100
MAX_NAME_LAENGE = 30

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-nur-lokal-verwenden")

db.init_db()


def neues_spiel(name):
    """Legt den Spielstand für eine neue Runde in der Session an (F2, F11)."""
    session["name"] = name
    session["ziel"] = secrets.randbelow(MAX_ZAHL - MIN_ZAHL + 1) + MIN_ZAHL
    session["verlauf"] = []
    session["meldung"] = None
    session.pop("ergebnis", None)


def pruefe_name(eingabe):
    """Gibt (name, fehler) zurück. Genau einer der beiden Werte ist None."""
    name = " ".join(eingabe.split())
    if not name:
        return None, "Bitte gib einen Namen ein, damit wir dich in die Rangliste eintragen können."
    if len(name) > MAX_NAME_LAENGE:
        return None, f"Dein Name ist zu lang. Erlaubt sind höchstens {MAX_NAME_LAENGE} Zeichen."
    return name, None


def pruefe_zahl(eingabe):
    """Gibt (zahl, fehler) zurück. Genau einer der beiden Werte ist None (F10)."""
    text = eingabe.strip()
    if not text:
        return None, f"Bitte gib eine Zahl von {MIN_ZAHL} bis {MAX_ZAHL} ein."
    try:
        zahl = int(text)
    except ValueError:
        return None, f"„{text[:12]}“ ist keine ganze Zahl. Erlaubt sind {MIN_ZAHL} bis {MAX_ZAHL}."
    if not MIN_ZAHL <= zahl <= MAX_ZAHL:
        return None, f"{zahl} liegt außerhalb. Erlaubt sind {MIN_ZAHL} bis {MAX_ZAHL}."
    return zahl, None


@app.route("/")
def start():
    return render_template(
        "index.html",
        rangliste=db.get_highscores(),
        name=session.get("name", ""),
        fehler=None,
    )


@app.post("/start")
def spiel_starten():
    eingabe = request.form.get("name", "")
    name, fehler = pruefe_name(eingabe)
    if fehler:
        return (
            render_template(
                "index.html",
                rangliste=db.get_highscores(),
                name=eingabe[:MAX_NAME_LAENGE],
                fehler=fehler,
            ),
            400,
        )
    neues_spiel(name)
    return redirect(url_for("spiel"))


@app.route("/spiel", methods=["GET", "POST"])
def spiel():
    if "ziel" not in session:
        return redirect(url_for("start"))

    if request.method == "POST":
        zahl, fehler = pruefe_zahl(request.form.get("zahl", ""))
        if fehler:
            session["meldung"] = {"art": "fehler", "text": fehler}
        else:
            verlauf = session["verlauf"]
            schon_geraten = any(eintrag["zahl"] == zahl for eintrag in verlauf)
            ziel = session["ziel"]
            richtung = "hoeher" if zahl < ziel else "tiefer" if zahl > ziel else "richtig"
            verlauf.append({"zahl": zahl, "richtung": richtung})
            session["verlauf"] = verlauf

            if richtung == "richtig":
                versuche = len(verlauf)
                score_id = db.save_score(session["name"], versuche)
                session["ergebnis"] = {
                    "id": score_id,
                    "name": session["name"],
                    "zahl": zahl,
                    "versuche": versuche,
                }
                for schluessel in ("ziel", "verlauf", "meldung"):
                    session.pop(schluessel, None)
                return redirect(url_for("ergebnis"))

            session["meldung"] = {
                "art": richtung,
                "zahl": zahl,
                "schon_geraten": schon_geraten,
            }
        # Post/Redirect/Get: Neuladen der Seite zählt keinen Versuch doppelt.
        return redirect(url_for("spiel"))

    return render_template(
        "spiel.html",
        name=session["name"],
        verlauf=session["verlauf"],
        meldung=session.get("meldung"),
        min_zahl=MIN_ZAHL,
        max_zahl=MAX_ZAHL,
    )


@app.route("/ergebnis")
def ergebnis():
    daten = session.get("ergebnis")
    if not daten:
        return redirect(url_for("start"))
    return render_template(
        "ergebnis.html",
        ergebnis=daten,
        platz=db.get_rank(daten["id"]),
        rangliste=db.get_highscores(),
    )


@app.post("/neu")
def neue_runde():
    """Startet direkt eine neue Runde mit demselben Namen (F9)."""
    name = session.get("name")
    if not name:
        return redirect(url_for("start"))
    neues_spiel(name)
    return redirect(url_for("spiel"))


if __name__ == "__main__":
    app.run(debug=True)
