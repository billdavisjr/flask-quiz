import os

from flask import Flask, render_template, flash, request, redirect, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "not a secret")

MAX_ATTEMPTS = 3
RIDDLES = [
    {"question": "Who?", "answer": "doctor"},
    {"question": "Why?", "answer": "why not"},
    {"question": "When?", "answer": "future"},
    {"question": "What?", "answer": "watt"},
]

game_state = dict()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new_game", methods=["POST"])
def new_game():
    player = request.form["player"]
    game_state[player] = {
        "score": 0,
        "riddle_num": 0,
        "riddle_attempts": MAX_ATTEMPTS,
    }
    return redirect(url_for("riddle", player=player))


@app.route("/riddle/<player>", methods=["GET", "POST"])
def riddle(player):
    if player not in game_state:
        return redirect(url_for("index"))

    player_state = game_state[player]

    if request.method == "POST" and player_state["riddle_num"] < len(RIDDLES):
        previous_riddle = RIDDLES[player_state["riddle_num"]]
        if request.form["answer"].lower() == previous_riddle["answer"]:
            player_state["riddle_num"] += 1
            player_state["score"] += 1
            flash("Correct answer, %s! Your score is %s." % (
                  player, player_state["score"]))
        elif not player_state["riddle_attempts"]:
            flash("Wrong answer, %s. Better luck with the next riddle." % (
                  player))
            player_state["riddle_num"] += 1
            player_state["riddle_attempts"] = MAX_ATTEMPTS
        else:
            player_state["riddle_attempts"] -= 1
            flash("Wrong answer, %s. You have %s attempts left." % (
                  player, player_state["riddle_attempts"]))

    if player_state["riddle_num"] >= len(RIDDLES):
        return render_template("game_over.html", player=player)

    new_riddle = RIDDLES[player_state["riddle_num"]]
    return render_template(
        "riddle.html", player=player,
        question=new_riddle["question"], player_state=player_state)


if __name__ == "__main__":
    app.run(os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")),
            debug=True)
