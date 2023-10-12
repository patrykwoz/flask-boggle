from boggle import Boggle

from flask import Flask, request, flash, render_template, redirect, url_for, session, make_response
from flask import jsonify
import pdb
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "someSecret123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()



@app.route('/', methods=['GET', 'POST'])
def render_home():
    current_board = boggle_game.make_board()
    session["current_board"] = current_board
    board = session["current_board"]
    return render_template('home.html', board = board)


@app.route('/handle-response', methods=['POST'])
def handle_response():
    try:
        user_guess = request.json.get('userGuess')
        if not user_guess:
            return jsonify({"error": "No guess provided!"}), 400
        
        board = session.get("current_board")
        if board is None:
            return jsonify({"error": "Board not found!"}), 400

        result = boggle_game.check_valid_word(board, user_guess)
        response_data = {'result': result}
        return jsonify(response_data)
    except AttributeError:
        return redirect('/game-finished')


@app.route('/game-finished', methods=['POST'])
def handle_endgame():
    game_score = request.json.get('score')
        
    if (not game_score) and (not isinstance(game_score, int)):
            return jsonify({"error": "No game_score provided!"}), 400

    try:
        highest_score = int(session['highest_score']) + int(game_score)
    except:
        highest_score = int(game_score)
    session['highest_score'] = highest_score

    try:
        games_count = int(session['count_games']) + 1
    except:
        games_count = 1
    session['count_games'] = games_count

    response_data = {'message': f"Thanks for playing {games_count} game(s)!", 'highestscore':highest_score}
    return jsonify(response_data)



@app.route('/handle-reset', methods=['GET'])
def handle_reset():
    return redirect('/')
