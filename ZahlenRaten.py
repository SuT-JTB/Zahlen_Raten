import os
import random
import sqlite3
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "zahlen-raten-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "highscores.db")


def init_db():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS highscore (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                versuche INTEGER NOT NULL,
                zeitpunkt TEXT NOT NULL
            )
            """
        )
        connection.commit()


def get_highscores(limit=10):
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT name, versuche, zeitpunkt FROM highscore ORDER BY versuche ASC, zeitpunkt ASC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def save_highscore(name, attempts):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "INSERT INTO highscore (name, versuche, zeitpunkt) VALUES (?, ?, ?)",
            (name, attempts, datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
        )
        connection.commit()


@app.route("/")
def index():
    error = request.args.get("error", "")
    return render_template(
        "index.html",
        error=error,
        highscores=get_highscores(),
    )

@app.route("/start", methods=["POST"])
def start_game():
    player_name = (request.form.get("player_name") or "").strip()
    if not player_name:
        return redirect(url_for("index", error="Bitte gib deinen Namen ein."))

    session["player_name"] = player_name
    session["secret_number"] = random.randint(0, 100)
    session["attempts"] = 0
    session["status"] = "Suche eine Zahl zwischen 0 und 100."
    return redirect(url_for("game"))


@app.route("/game", methods=["GET", "POST"])
def game():
    player_name = session.get("player_name")
    if not player_name:
        return redirect(url_for("index"))

    error = ""
    status = session.get("status", "")

    if request.method == "POST":
        guess_raw = (request.form.get("guess") or "").strip()
        try:
            guess = int(guess_raw)
        except ValueError:
            error = "Bitte gib eine ganze Zahl zwischen 0 und 100 ein."
            return render_template(
                "game.html",
                player_name=player_name,
                status=status,
                error=error,
                highscores=get_highscores(),
            )

        if not 0 <= guess <= 100:
            error = "Die Zahl muss zwischen 0 und 100 liegen."
            return render_template(
                "game.html",
                player_name=player_name,
                status=status,
                error=error,
                highscores=get_highscores(),
            )

        secret_number = session.get("secret_number")
        session["attempts"] = int(session.get("attempts", 0)) + 1
        attempts = session["attempts"]

        if guess < secret_number:
            status = "Zu klein! Versuche es erneut."
        elif guess > secret_number:
            status = "Zu groß! Versuche es erneut."
        else:
            save_highscore(player_name, attempts)
            result_message = f"Richtig! {player_name} hat die Zahl in {attempts} Versuchen erraten."
            session.pop("player_name", None)
            session.pop("secret_number", None)
            session.pop("attempts", None)
            session.pop("status", None)
            return render_template(
                "result.html",
                result_message=result_message,
                highscores=get_highscores(),
            )

        session["status"] = status
        return render_template(
            "game.html",
            player_name=player_name,
            status=status,
            error=error,
            highscores=get_highscores(),
        )

    return render_template(
        "game.html",
        player_name=player_name,
        status=status,
        error=error,
        highscores=get_highscores(),
    )


@app.route("/new-game")
def new_game():
    session.clear()
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
