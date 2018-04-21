from flask import render_template, request, jsonify
from app import app
from action import Action
from chessboard import Chessboard
from app import _BLACK, _WHITE
import time, math
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Gobang')

@app.route('/start', methods=['POST'])
def start():
    bd = [[0 for i in range(0, 15)] for j in range(0, 15)]
    Chessboard.curV = None
    bd[7][7] = _WHITE
    Chessboard.curB = bd
    return jsonify(dict())

@app.route('/restart', methods=['POST'])
def restart():
    Chessboard.curB = [[0 for i in range(0, 15)] for j in range(0, 15)]
    Chessboard.curV = None
    return jsonify(dict())


@app.route('/play', methods=['POST'])
def one_step():
    data = {}
    x = int(request.form.get('x', 0))
    y = int(request.form.get('y', 0))
    action = Action(x, y, True)
    cur = _usr_action(action)
    if cur.checkWin(action) is True:
        data['win'] = False
        return jsonify(data)
    # calculate elapsed time
    start = time.clock()
    # bestmove, bestscore = cur.minimax(2)
    bestmove, bestscore = cur.alpha_beta(1)
    elapsed = time.clock()-start
    data['elapsed-time'] = math.ceil(elapsed)
    if bestmove is None:
        data['win'] = False
        return jsonify(data)
    data['best'] = str((bestmove.x, bestmove.y))
    bd = cur.board
    x = bestmove.x
    y = bestmove.y
    data.update({'x':x, 'y':y})
    bd[x][y] = _WHITE
    cb = Chessboard(None, bd, bestscore)
    Chessboard.curB = bd
    Chessboard.curV = bestscore
    if abs(bestscore) > 40000:
        if cur.checkWin(bestmove) is True:
            data['win'] = True
    _print_chessboard(bd)
    return jsonify(data)

def _usr_action(action):
    cb = Chessboard(None, Chessboard.curB, Chessboard.curV)
    return cb.play(action)

def _print_chessboard(bd):
    for i in range(0, 15):
        print '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (bd[0][i],bd[1][i],bd[2][i],bd[3][i],bd[4][i],bd[5][i],bd[6][i],bd[7][i],bd[8][i],bd[9][i],bd[10][i],bd[11][i],bd[12][i],bd[13][i], bd[14][i])
        # print '--------------------------------'

    
