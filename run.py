import os
from flask import Flask, render_template, flash, request, redirect, url_for

app = Flask(__name__)
app.secret_key = '&u)5v-%$df0e@=gptj@mu3q#pim-j#wjll9@w_1o(m@^-63t_q'


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect(request.form["user"])
    return render_template("index.html")


@app.route('/<user>')
def user(user):
    return redirect('/' + user +'/riddle')


game_state = {
    "yoni": {
        "score": 0,
        "current_riddle": 0,
        "attempts_left_for_riddle": 3,
    },
    "niel": {
        "score": 12,
        "current_riddle": 0,
        "attempts_left_for_riddle": 3,
    }
}


@app.route('/<user>/riddle', methods=["GET", "POST"])
def riddle(user):
    
    riddles = [
        {"question": "who?", "answer": "Doctor"},
        {"question": "why?", "answer": "Why not"},
        {"question": "when?", "answer": "future"},
        {"question": "what?", "answer": "watt"},
    ]

    player_state = game_state[user]
    if request.method == 'POST':
        if request.form["answer"] == riddles[player_state['current_riddle']]['answer']:
            player_state['current_riddle'] += 1
            player_state['score'] += 1
            flash('Correct answer, ' + user + '. Your score is ' + str(player_state['score']) + '. ')
            print(game_state)
        elif player_state['attempts_left_for_riddle'] ==  0:
            player_state['current_riddle'] += 1
        else:
            player_state['attempts_left_for_riddle'] -=  1
            flash('Wrong answer, ' + user + '. Try again. You have ' + str(player_state['attempts_left_for_riddle']) + ' attempts left.')
            print(game_state)
    return render_template("riddle.html", question = riddles, username=user)   
    
    
app.run(os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)