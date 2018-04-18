from app import _BLACK, _WHITE
from action import Action

FIVE_POINT = 70000

class Chessboard:
    isWin = None
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

        # tmp = set()
        # bd = self.board
        # if bd is None:
        #     tmp.append((7,7))
        #     return tmp
        # if bd is not None:
        #     for i in range(0, 15):
        #         for j in range(0, 15):
        #             if bd[i][j] != 0:
        #                 for k in self.getNextCandidates(i, j):
        #                     tmp.add(k)
        # rsts = set(tmp)
        # for r in tmp:
        #     for i in self.getNextCandidates(r[0], r[1]):
        #         rsts.add(i)
        rsts = self.neighbours
        actions = map(lambda ac: Action(ac[0], ac[1], black), rsts)
        rsts = sorted(actions, key=self.evaluateAction,reverse=True)
        if len(rsts) <=15:
            return rsts
        else:
            return rsts[0:15]
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
            return -1
        return self.board[x][y]
    

    def evaluateAction(self, action=None):
        '''
        evaluate each action!
        '''
        x = action.x
        y = action.y
        flag = _BLACK if action.black else _WHITE
        rst = 0

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
                rst += 600
            elif m1 == 4:
                if self.validation(x+end1, y) == 0 and self.validation(x+end1-5, y) == 0:
                    rst += 4320
                else:
                    rst += 600
        
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
                rst += 600
            elif m1 == 4:
                if self.validation(x, y+end1) == 0 and self.validation(x, y+end1-5) == 0:
                    rst += 4320
                else:
                    rst += 600

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
                rst += 600
            elif m1 == 4:
                if self.validation(x-end1, y+end1) == 0 and self.validation(x-end1+5, y+end1-5) == 0:
                    rst += 4320
                else:
                    rst += 600

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
                rst += 600
            elif m1 == 4:
                if self.validation(x+end1, y+end1) == 0 and self.validation(x+end1-5, y+end1-5) == 0:
                    rst += 4320
                else:
                    rst += 600

        if action.black:
            self.Uv += rst
        else:
            self.Av += rst
        # check win
        if rst > FIVE_POINT:
            Chessboard.isWin = False if action.black else True
        elif rst < FIVE_POINT and Chessboard.isWin is not None:
            Chessboard.isWin = None

        # Right Now! It's time to decrease opponent's point!

        oppoval = self.Av if action.black else self.Uv
        oppoflag = _WHITE if action.black else _BLACK
        # check row
        if self.validation(x-1, y) == oppoflag and self.validation(x+1, y) == oppoflag:
            oppoval -= 720
            if (self.validation(x-2, y) == oppoflag and self.validation(x-3, y) == oppoflag) or (self.validation(x+2, y) == oppoflag and self.validation(x+3, y) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x-1, y) == oppoflag:
            if self.validation(x-2, y) == oppoflag and self.validation(x-3, y) == oppoflag:
                if self.validation(x-4, y) == oppoflag and self.validation(x-5, y) == 0:
                    oppoval -= 3600
                elif self.validation(x-4, y) == 0:
                    if self.validation(x-5, y) != oppoflag:
                        oppoval -= 2720
        elif self.validation(x+1, y) == oppoflag:
            if self.validation(x+2, y) == oppoflag and self.validation(x+3, y) == oppoflag:
                if self.validation(x+4, y) == oppoflag and self.validation(x+5, y) == 0:
                    oppoval -= 3600
                elif self.validation(x+4, y) == 0:
                    if self.validation(x+5, y) != oppoflag:
                        oppoval -= 2720
        # check column
        if self.validation(x, y-1) == oppoflag and self.validation(x, y+1) == oppoflag:
            oppoval -= 720
            if (self.validation(x, y-2) == oppoflag and self.validation(x, y-3) == oppoflag) or (self.validation(x, y+2) == oppoflag and self.validation(x, y+3) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x, y-1) == oppoflag:
            if self.validation(x, y-2) == oppoflag and self.validation(x, y-3) == oppoflag:
                if self.validation(x, y-4) == oppoflag and self.validation(x, y-5) == 0:
                    oppoval -= 3600
                elif self.validation(x, y-4) == 0:
                    if self.validation(x, y-5) != oppoflag:
                        oppoval -= 2720
        elif self.validation(x, y+1) == oppoflag:
            if self.validation(x, y+2) == oppoflag and self.validation(x, y+3) == oppoflag:
                if self.validation(x, y+4) == oppoflag and self.validation(x, y+5) == 0:
                    oppoval -= 3600
                elif self.validation(x, y+4) == 0:
                    if self.validation(x, y+5) != oppoflag:
                        oppoval -= 2720
        # check forward diagonal
        if self.validation(x-1, y+1) == oppoflag and self.validation(x+1, y-1) == oppoflag:
            oppoval -= 720
            if (self.validation(x-2, y+2) == oppoflag and self.validation(x-3, y+3) == oppoflag) or (self.validation(x+2, y+2) == oppoflag and self.validation(x+3, y+3) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x-1, y+1) == oppoflag:
            if self.validation(x-2, y+2) == oppoflag and self.validation(x-3, y+3) == oppoflag:
                if self.validation(x-4, y+4) == oppoflag and self.validation(x-5, y+5) == 0:
                    oppoval -= 3600
                elif self.validation(x-4, y+4) == 0:
                    if self.validation(x-5, y+5) != oppoflag:
                        oppoval -= 2720
        elif self.validation(x+1, y-1) == oppoflag:
            if self.validation(x+2, y-2) == oppoflag and self.validation(x+3, y-3) == oppoflag:
                if self.validation(x+4, y-4) == oppoflag and self.validation(x+5, y-5) == 0:
                    oppoval -= 3600
                elif self.validation(x+4, y-4) == 0:
                    if self.validation(x+5, y-5) != oppoflag:
                        oppoval -= 2720
        # check backward diagonal
        if self.validation(x-1, y-1) == oppoflag and self.validation(x+1, y+1) == oppoflag:
            oppoval -= 720
            if (self.validation(x-2, y-2) == oppoflag and self.validation(x-3, y-3) == oppoflag) or (self.validation(x+2, y+2) == oppoflag and self.validation(x+3, y+3) == oppoflag):
                oppoval -= FIVE_POINT
        elif self.validation(x-1, y-1) == oppoflag:
            if self.validation(x-2, y-2) == oppoflag and self.validation(x-3, y-3) == oppoflag:
                if self.validation(x-4, y-4) == oppoflag and self.validation(x-5, y-5) == 0:
                    oppoval -= 3600
                elif self.validation(x-4, y-4) == 0:
                    if self.validation(x-5, y-5) != oppoflag:
                        oppoval -= 2720
        elif self.validation(x+1, y+1) == oppoflag:
            if self.validation(x+2, y+2) == oppoflag and self.validation(x+3, y+3) == oppoflag:
                if self.validation(x+4, y+4) == oppoflag and self.validation(x+5, y+5) == 0:
                    oppoval -= 3600
                elif self.validation(x+4, y+4) == 0:
                    if self.validation(x+5, y+5) != oppoflag:
                        oppoval -= 2720

        if action.black:
            self.Av = oppoval
        else:
            self.Uv = oppoval
        
        return rst



    def evaluateBoard(self):
        return self.Av-self.Uv

    '''
        need to modify Chessboard.isWin
    '''    
    def isGameOver(self, depth):
        return depth == 0 or (Chessboard.isWin is not None)

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
            score = self.min_play2(newchessboard, depth, best_score, beta)
            if score > best_score:
                best_move = c
                best_score = score
                # best score is the board's score
        print '(best_move, best_score): ', best_move, best_score
        return (best_move, best_score)

    def max_play2(self, state, depth, alpha, beta):
        if self.isGameOver(depth):
            return state.evaluateBoard()
        cands = state.gen(False)
        best_score = float('-inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            newchessboard = state.play(c)
            score = state.min_play2(newchessboard, depth-1, alpha, beta)
            best_score = max(best_score, score)
            if best_score > beta:
                return best_score
            alpha = max(alpha, best_score)
        return best_score


    def min_play2(self, state, depth, alpha, beta):
        if self.isGameOver(depth):
            return state.evaluateBoard()
        cands = state.gen(True)
        best_score = float('inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            newchessboard = state.play(c)
            score = state.max_play2(newchessboard, depth, alpha, beta)
            best_score = min(best_score, score)
            if best_score < alpha:
                return best_score
            beta = min(beta, best_score)
        return best_score

        

        
        
        
    