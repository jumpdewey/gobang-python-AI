from app import _BLACK, _WHITE
from action import Action

FIVE_POINT = 70000
FOUR_POINT = 10000
THREE_POINT = 1000
class Chessboard:
    curB = None
    curV = None
    def __init__(self, prev=None, givenbd=None, givenVal=None):
        self.board = [[0 for i in range(0, 15)] for j in range(0, 15)]
        if prev is not None:
            bd = prev.board
            if bd is not None:
                for i in range(0, 15):
                    for j in range(0, 15):
                        self.board[i][j] = bd[i][j]
        self.val = 0
        self.Uv = 0 if prev is None else prev.Uv
        self.Av = 0 if prev is None else prev.Av
        if givenbd != None:
            for i in range(0, 15):
                    for j in range(0, 15):
                        self.board[i][j] = givenbd[i][j]
        if givenVal != None:
            self.val = givenVal
        if prev is None:
            tmpset = set()
            self.neighbours = set()
            for i in self._genNeighbours(Action(7,7,False)):
                tmpset.add(i)
            self.neighbours = tmpset
        else:
            self.neighbours = prev.neighbours

    def play(self, action):
        ''' return a new Chessboard'''
        x = action.x
        y = action.y
        black = action.black
        rst = None
        if self.board[x][y] != 0:
            return None
        if black == True:
            # set black to 1
            rst = Chessboard(self)
            rst.board[x][y] = _BLACK
            rst.val = rst.evaluateAction(action)
            rst.neighbours = rst._genNeighbours(action)
        else:
            # set white to 2
            rst = Chessboard(self)
            rst.board[x][y] = _WHITE
            rst.val = rst.evaluateAction(action)
            rst.neighbours = rst._genNeighbours(action)
        return rst

    def gen(self, black):
        # generate potential actions

        rsts = self.neighbours
        actions = map(lambda ac: Action(ac[0], ac[1], black), rsts)
        # changing the value of 'reverse' to black makes it perform better.
        # Oops! the value of 'reverse' should be True!
        rsts = sorted(actions, key=self.evaluateAction,reverse=True)
        # if len(rsts) <=15:
        #     return rsts
        # else:
        #     return rsts[0:15]
        return rsts

    def _genNeighbours(self, action):
        prevNeighbours = self.neighbours
        x = action.x
        y = action.y
        if (x, y) in prevNeighbours:
            prevNeighbours.remove((x, y))
        for i in self.getNextCandidates(x, y):
            prevNeighbours.add(i)
        return prevNeighbours

    def getNextCandidates(self, x, y):
        def _checkEmpty(x, y):
            if x < 0 or x >= 15 or y < 0 or y >= 15:
                return False
            return self.board[x][y] == 0

        rsts = []
        if _checkEmpty(x-1, y):
            rsts.append((x-1,y))
        if _checkEmpty(x+1, y):
            rsts.append((x+1,y))
        if _checkEmpty(x, y-1):
            rsts.append((x,y-1))
        if _checkEmpty(x, y+1):
            rsts.append((x,y+1))
        if _checkEmpty(x-1, y-1):
            rsts.append((x-1, y-1))
        if _checkEmpty(x-1, y+1):
            rsts.append((x-1, y+1))
        if _checkEmpty(x+1, y-1):
            rsts.append((x+1, y-1))
        if _checkEmpty(x+1, y+1):
            rsts.append((x+1, y+1))
        return rsts
    
    def validation(self, x, y):
        if x < 0 or x >= 15 or y < 0 or y >= 15:
            return float('-inf')
        return self.board[x][y]
    

    def evaluateAction(self, action=None):
        '''
        evaluate each action!
        '''
        x = action.x
        y = action.y
        flag = _BLACK if action.black else _WHITE
        rst = 0
        countflag = 0
        # judge row
        if self.validation(x-1, y) == 0 and self.validation(x+1, y) == 0:
            rst += 20
            if self.validation(x-2, y) == flag or self.validation(x+2, y) == flag:
                rst += 100

        elif self.validation(x-1, y) == flag or self.validation(x+1, y) == flag:
            rst += 120
            count = 0
            m1 = 0
            end1 = 0
            for i in range(-4, 5):
                if self.validation(x+i, y) == flag:
                    count+=1
                    m1 = max(m1, count)
                    if m1 == 4:
                        end1 = i+1
                else:
                    count = 0
            if m1 == 5:
                rst += FIVE_POINT
            elif m1 == 3:
                rst += THREE_POINT
                countflag += 1
            elif m1 == 4:
                if self.validation(x+end1, y) == 0 and self.validation(x+end1-5, y) == 0:
                    rst += FOUR_POINT
                else:
                    rst += THREE_POINT
                    rst += 2000
                countflag += 1
        
        # judge column
        if self.validation(x, y-1) == 0 and self.validation(x, y+1) == 0:
            rst += 20
            if self.validation(x, y-2) == flag or self.validation(x, y+2) == flag:
                rst += 100
        elif self.validation(x, y-1) == flag or self.validation(x, y+1) == flag:
            rst += 120
            count = 0
            m1 = 0
            end1 = 0
            for i in range(-4, 5):
                if self.validation(x, y+i) == flag:
                    count+=1
                    m1 = max(m1, count)
                    if m1 == 4:
                        end1 = i+1
                else:
                    count = 0
            if m1 == 5:
                rst += FIVE_POINT
            elif m1 == 3:
                rst += THREE_POINT
                countflag += 1
            elif m1 == 4:
                countflag += 1
                if self.validation(x, y+end1) == 0 and self.validation(x, y+end1-5) == 0:
                    rst += FOUR_POINT
                else:
                    rst += THREE_POINT
                    rst += 2000

        # judge forward diagonal
        if self.validation(x+1, y-1) == 0 and self.validation(x-1, y+1) == 0:
            rst += 20
            if self.validation(x+2, y-2) == flag or self.validation(x-2, y+2) == flag:
                rst += 100
        elif self.validation(x+1, y-1) == flag or self.validation(x-1, y+1) == flag:
            rst += 120
            count = 0
            m1 = 0
            end1 = 0
            for i in range(-4, 5):
                if self.validation(x-i, y+i) == flag:
                    count+=1
                    m1 = max(m1, count)
                    if m1 == 4:
                        end1 = i+1
                else:
                    count = 0
            if m1 == 5:
                rst += FIVE_POINT
            elif m1 == 3:
                rst += THREE_POINT
                countflag += 1
            elif m1 == 4:
                countflag += 1
                if self.validation(x-end1, y+end1) == 0 and self.validation(x-end1+5, y+end1-5) == 0:
                    rst += FOUR_POINT
                else:
                    rst += THREE_POINT
                    rst += 2000

        #judge backward diagonal
        if self.validation(x-1, y-1) == 0 and self.validation(x+1, y+1) == 0:
            rst += 20
            if self.validation(x-2, y-2) == flag or self.validation(x+2, y+2) == flag:
                rst += 100
        elif self.validation(x-1, y-1) == flag or self.validation(x+1, y+1) == flag:
            rst += 120
            count = 0
            m1 = 0
            end1 = 0
            for i in range(-4, 5):
                if self.validation(x+i, y+i) == flag:
                    count+=1
                    m1 = max(m1, count)
                    if m1 == 4:
                        end1 = i+1
                else:
                    count = 0
            if m1 == 5:
                rst += FIVE_POINT
            elif m1 == 3:
                countflag += 1
                rst += THREE_POINT
            elif m1 == 4:
                countflag += 1
                if self.validation(x+end1, y+end1) == 0 and self.validation(x+end1-5, y+end1-5) == 0:
                    rst += FOUR_POINT
                else:
                    rst += THREE_POINT
                    rst += 2000
        if countflag > 1:
            rst += (countflag-1)*1500
        if action.black:
            self.Uv += rst
        else:
            self.Av += rst

        # Right Now! It's time to decrease opponent's point!

        oppoval = self.Av if action.black else self.Uv
        oppoflag = _WHITE if action.black else _BLACK
        # check row
        if self.validation(x-1, y) == oppoflag and self.validation(x+1, y) == oppoflag:
            oppoval -= THREE_POINT
            if (self.validation(x-2, y) == oppoflag and self.validation(x-3, y) == oppoflag) or (self.validation(x+2, y) == oppoflag and self.validation(x+3, y) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x-1, y) == oppoflag:
            if self.validation(x-2, y) == oppoflag and self.validation(x-3, y) == oppoflag:
                if self.validation(x-4, y) != flag:
                    oppoval -= FOUR_POINT

        elif self.validation(x+1, y) == oppoflag:
            if self.validation(x+2, y) == oppoflag and self.validation(x+3, y) == oppoflag:
                if self.validation(x+4, y) != flag:
                    oppoval -= FOUR_POINT
        # check column
        if self.validation(x, y-1) == oppoflag and self.validation(x, y+1) == oppoflag:
            oppoval -= THREE_POINT
            if (self.validation(x, y-2) == oppoflag and self.validation(x, y-3) == oppoflag) or (self.validation(x, y+2) == oppoflag and self.validation(x, y+3) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x, y-1) == oppoflag:
            if self.validation(x, y-2) == oppoflag and self.validation(x, y-3) == oppoflag:
                if self.validation(x, y-4) != flag:
                    oppoval -= FOUR_POINT
        elif self.validation(x, y+1) == oppoflag:
            if self.validation(x, y+2) == oppoflag and self.validation(x, y+3) == oppoflag:
                if self.validation(x, y+4) != flag:
                    oppoval -= FOUR_POINT
        # check forward diagonal
        if self.validation(x-1, y+1) == oppoflag and self.validation(x+1, y-1) == oppoflag:
            oppoval -= THREE_POINT
            if (self.validation(x-2, y+2) == oppoflag and self.validation(x-3, y+3) == oppoflag) or (self.validation(x+2, y+2) == oppoflag and self.validation(x+3, y+3) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x-1, y+1) == oppoflag:
            if self.validation(x-2, y+2) == oppoflag and self.validation(x-3, y+3) == oppoflag:
                if self.validation(x-4, y+4) != flag:
                    oppoval -= FOUR_POINT
        elif self.validation(x+1, y-1) == oppoflag:
            if self.validation(x+2, y-2) == oppoflag and self.validation(x+3, y-3) == oppoflag:
                if self.validation(x+4, y-4) != flag:
                    oppoval -= FOUR_POINT
        # check backward diagonal
        if self.validation(x-1, y-1) == oppoflag and self.validation(x+1, y+1) == oppoflag:
            oppoval -= THREE_POINT
            if (self.validation(x-2, y-2) == oppoflag and self.validation(x-3, y-3) == oppoflag) or (self.validation(x+2, y+2) == oppoflag and self.validation(x+3, y+3) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x-1, y-1) == oppoflag:
            if self.validation(x-2, y-2) == oppoflag and self.validation(x-3, y-3) == oppoflag:
                if self.validation(x-4, y-4) != flag:
                    oppoval -= FOUR_POINT
        elif self.validation(x+1, y+1) == oppoflag:
            if self.validation(x+2, y+2) == oppoflag and self.validation(x+3, y+3) == oppoflag:
                if self.validation(x+4, y+4) != flag:
                    oppoval -= FOUR_POINT
        if action.black:
            self.Av = oppoval
        else:
            self.Uv = oppoval
        
        return rst



    def evaluateBoard(self):
        return self.Av-self.Uv
  
    def isGameOver(self, depth, action):
        return depth == 0 or self.checkWin(action)

# ================Minimax========================

    def minimax(self, depth):
        cands = self.gen(False)
        if len(cands) == 0:
            return (None, None)
        best_move = None
        best_score = float('-inf')
        for c in cands:
            newchessboard = self.play(c)
            score = self.min_play(newchessboard, depth)
            if score > best_score:
                best_move = c
                best_score = score
                # best score is the board's score
        return (best_move, best_score)

    def max_play(self, state, depth):
        if self.isGameOver(depth):
            return state.evaluateBoard()
        cands = state.gen(False)
        best_score = float('-inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            newchessboard = state.play(c)
            score = state.min_play(newchessboard, depth-1)
            if score > best_score:
                best_score = score
        return best_score


    def min_play(self, state, depth):
        if self.isGameOver(depth):
            return state.evaluateBoard()
        cands = state.gen(True)
        best_score = float('inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            newchessboard = state.play(c)
            score = state.max_play(newchessboard, depth)
            if score < best_score:
                best_score = score
        return best_score

# ================Alpha-beta pruning========================

    def alpha_beta(self, depth):
        beta = float('inf')
        cands = self.gen(False)
        if len(cands) == 0:
            return (None, None)
        best_move = None
        best_score = float('-inf')
        for c in cands:
            newchessboard = self.play(c)
            # try to pass parameter to min_play2()
            score = self.min_play2(newchessboard, depth, best_score, beta, c)
            if score > best_score:
                best_move = c
                best_score = score
                # best score is the board's score
        print '(best_move:(%s, %s), %s): ' % (best_move.x, best_move.y, best_score)
        return (best_move, best_score)

    def max_play2(self, state, depth, alpha, beta, action):
        # 'action' is the previous action leading to the current state
        if self.isGameOver(depth, action):
            return state.evaluateBoard()
        cands = state.gen(False)
        best_score = float('-inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            newchessboard = state.play(c)
            score = state.min_play2(newchessboard, depth, alpha, beta, c)
            best_score = max(best_score, score)
            if best_score > beta:
                return best_score
            alpha = max(alpha, best_score)
        return best_score


    def min_play2(self, state, depth, alpha, beta, action):
        # 'action' is the previous action leading to the current state
        if self.isGameOver(depth, action):
            return state.evaluateBoard()
        cands = state.gen(True)
        best_score = float('inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            newchessboard = state.play(c)
            # try to pass action parameter to min_play2()
            score = state.max_play2(newchessboard, depth-1, alpha, beta, c)
            best_score = min(best_score, score)
            if best_score < alpha:
                return best_score
            beta = min(beta, best_score)
        return best_score
    

    def checkWin(self, action):
        b = action.black
        flag = _BLACK if action.black else _WHITE
        x = action.x
        y = action.y
        count = 0
        m1 = 0
        # judge row
        for i in range(-4, 5):
            if self.validation(x+i, y) == flag:
                count+=1
                m1 = max(m1, count)
            else:
                count = 0
        if m1 == 5:
            return True
        # judge column
        count = 0
        m1 = 0
        for i in range(-4, 5):
            if self.validation(x, y+i) == flag:
                count+=1
                m1 = max(m1, count)
            else:
                count = 0
        if m1 == 5:
            return True
        # judge forward diagonal
        count = 0
        m1 = 0
        for i in range(-4, 5):
            if self.validation(x-i, y+i) == flag:
                count+=1
                m1 = max(m1, count)
            else:
                count = 0
        if m1 == 5:
            return True
        # judge backward diagonal
        count = 0
        m1 = 0
        for i in range(-4, 5):
            if self.validation(x+i, y+i) == flag:
                count+=1
                m1 = max(m1, count)
            else:
                count = 0
        if m1 == 5:
            return True
        return

        

        
        
        
    