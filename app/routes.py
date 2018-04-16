from flask import render_template, request, jsonify
from app import app
from action import Action
from chessboard import Chessboard
from app import _BLACK, _WHITE
import time
@app.route('/')
@app.route('/index')
def index():
    usr = {'username':'Dewey'}
    return render_template('index.html', title='Gobang', user=usr)

@app.route('/play', methods=['POST'])
def one_step():
    data = {}
    x = int(request.form.get('x', 0))
    y = int(request.form.get('y', 0))
    action = Action(x, y, True)
    cur = _usr_action(action)
    # calculate elapsed time
    start = time.clock()
    # bestmove, bestscore = cur.minimax(2)
    bestmove, bestscore = cur.alpha_beta(2)
    elapsed = time.clock()-start
    data['elapsed-time'] = elapsed
    if bestmove is None:
        data['win'] = False
        return data
    data['best'] = str(bestmove)
    bd = cur.board

    # cands = cur.gen()
    # data = {}
    # maxval = 0
    # bestaction = None
    # bd = cur.board
    # curval = cur.val
    # for c in cands:
    #     tmp = Action(c[0], c[1], False)
    #     _ = cur.play(tmp)
    #     if _ is None:
    #         continue
    #     val = _.val
    #     data[str(c)] = val
    #     if val > maxval:
    #         bestaction = c
    #         maxval = val

    # if bestaction is None:
    #     data['win'] = False
    #     return data
    # data['best'] = str(bestaction)


    x = bestmove[0]
    y = bestmove[1]
    data.update({'x':x, 'y':y})
    bd[x][y] = _WHITE
    cb = Chessboard(None, bd, bestscore)
    Chessboard.curB = bd
    Chessboard.curV = bestscore
    data['win'] = Chessboard.isWin
    _print_chessboard(bd)
    return jsonify(data)

def _usr_action(action):
    cb = Chessboard(None, Chessboard.curB, Chessboard.curV)
    return cb.play(action)

def _print_chessboard(bd):
    for i in range(0, 7):
        print '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (bd[0][i],bd[1][i],bd[2][i],bd[3][i],bd[4][i],bd[5][i],bd[6][i],bd[7][i],bd[8][i],bd[9][i],bd[10][i],bd[11][i],bd[12][i],bd[13][i], bd[14][i])
        print '--------------------------------'

    
