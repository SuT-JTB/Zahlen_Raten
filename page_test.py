import os
import random
import sqlite3
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for

from database import DB_PATH, init_db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "figma-69"
)

init_db()


def get_highscores():
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT name, versuche, zeitpunkt
            FROM highscore
            ORDER BY versuche ASC, id ASC
            LIMIT 10
            """
        ).fetchall()
    return [dict(row) for row in rows]


@app.route("/")
def index():
    return render_template("index.html", highscores=get_highscores(), error=None)


@app.route("/start", methods=["POST"])
def start_game():
    player_name = request.form.get("player_name", "").strip()
    if not player_name:
        return (
            render_template(
                "index.html",
                highscores=get_highscores(),
                error="Bitte gib einen Spielernamen ein.",
            ),
            400,
        )

    session["player_name"] = player_name[:50]
    session["number_to_guess"] = random.randint(0, 100)
    session["attempts"] = 0
    return redirect(url_for("game"))


@app.route("/game", methods=["GET", "POST"])
def game():
    if "number_to_guess" not in session:
        return redirect(url_for("index"))

    status = None
    error = None

    if request.method == "POST":
        guess_value = request.form.get("guess", "")
        try:
            guess = int(guess_value)
        except ValueError:
            error = "Bitte gib eine ganze Zahl zwischen 0 und 100 ein."
        else:
            if not 0 <= guess <= 100:
                error = "Deine Zahl muss zwischen 0 und 100 liegen."
            else:
                session["attempts"] += 1
                number_to_guess = session["number_to_guess"]
                if guess < number_to_guess:
                    status = "Zu klein. Versuch es noch einmal."
                elif guess > number_to_guess:
                    status = "Zu groß. Versuch es noch einmal."
                else:
                    with sqlite3.connect(DB_PATH) as connection:
                        connection.execute(
                            """
                            INSERT INTO highscore (name, versuche, zeitpunkt)
                            VALUES (?, ?, ?)
                            """,
                            (
                                session["player_name"],
                                session["attempts"],
                                datetime.now().strftime("%d.%m.%Y %H:%M"),
                            ),
                        )
                    result_message = (
                        f"Glückwunsch, {session['player_name']}! "
                        f"Du hast die Zahl in {session['attempts']} "
                        f"Versuchen erraten."
                    )
                    session.pop("number_to_guess", None)
                    session.pop("attempts", None)
                    session.pop("player_name", None)
                    return render_template(
                        "result.html",
                        result_message=result_message,
                        highscores=get_highscores(),
                    )

    return render_template(
        "game.html",
        player_name=session["player_name"],
        status=status,
        error=error,
        highscores=get_highscores(),
    )


@app.route("/new-game")
def new_game():
    session.pop("number_to_guess", None)
    session.pop("attempts", None)
    session.pop("player_name", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
