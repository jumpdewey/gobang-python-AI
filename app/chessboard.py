from app import _BLACK, _WHITE
from action import Action
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
        self.Uvr = 0 if prev is None else prev.Uvr
        self.Uvc = 0 if prev is None else prev.Uvc
        self.Uvf = 0 if prev is None else prev.Uvf
        self.Uvb = 0 if prev is None else prev.Uvb
        self.Avr = 0 if prev is None else prev.Avr
        self.Avc = 0 if prev is None else prev.Avc
        self.Avf = 0 if prev is None else prev.Avf
        self.Avb = 0 if prev is None else prev.Avb
        if givenbd != None:
            for i in range(0, 15):
                    for j in range(0, 15):
                        self.board[i][j] = givenbd[i][j]
        if givenVal != None:
            self.val = givenVal
        

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
        else:
            # set white to 2
            rst = Chessboard(self)
            rst.board[x][y] = _WHITE
            rst.val = rst.evaluateAction(action)
        return rst

    def gen(self):
        tmp = []
        bd = self.board
        if bd is None:
            tmp.append((7,7))
            return tmp
        if bd is not None:
            for i in range(0, 15):
                for j in range(0, 15):
                    if bd[i][j] != 0:
                        tmp.extend(self.getNextCandidates(i, j))
        rsts = set(tmp)
        for r in tmp:
            for i in self.getNextCandidates(r[0], r[1]):
                rsts.add(i)
        return sorted(rsts, reverse=True)
    
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
                rst += 50000
            elif m1 == 3:
                rst += 600
            elif m1 == 4:
                if self.validation(x+end1, y) == 0 and self.validation(x+end1-5, y) == 0:
                    rst += 4320
                else:
                    rst += 600
        tmpr = rst
        if flag:
            self.Uvr += tmpr
        else:
            self.Avr += tmpr
        
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
                rst += 50000
            elif m1 == 3:
                rst += 600
            elif m1 == 4:
                if self.validation(x, y+end1) == 0 and self.validation(x, y+end1-5) == 0:
                    rst += 4320
                else:
                    rst += 600
        tmpc = rst - tmpr
        if flag:
            self.Uvc += tmpc
        else:
            self.Avc += tmpc

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
                rst += 50000
            elif m1 == 3:
                rst += 600
            elif m1 == 4:
                if self.validation(x-end1, y+end1) == 0 and self.validation(x-end1+5, y+end1-5) == 0:
                    rst += 4320
                else:
                    rst += 600
            
        tmpf = rst - tmpc
        if flag:
            self.Uvf += tmpf
        else:
            self.Avf += tmpf

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
                rst += 50000
            elif m1 == 3:
                rst += 600
            elif m1 == 4:
                if self.validation(x+end1, y+end1) == 0 and self.validation(x+end1-5, y+end1-5) == 0:
                    rst += 4320
                else:
                    rst += 600
        tmpb = rst - tmpf
        if flag:
            self.Uvb += tmpb
        else:
            self.Avb += tmpb

        # check win
        # if rst > 50000:
        #     Chessboard.isWin = False if action.black else True
        return rst



    def evaluateBoard(self):
        '''
        return (UserVal, AgentVal) 
        '''
        UserVal = self.Uvb + self.Uvc + self.Uvf + self.Uvr
        AgentVal = self.Avb + self.Avc + self.Avf + self.Avr
        return AgentVal-UserVal
    
    # def evaluateBoardWithAction(self, ac):
    #     x = ac.x
    #     y = ac.y
    #     black = ac.black
    #     flag = _BLACK if black else _WHITE
    #     if black == True:
    #         # user's action, hence only increment self.U

    '''
        need to modify Chessboard.isWin
    '''    
    def isGameOver(self, depth):
        return depth == 0



    def minimax(self, depth):
        print 'minimax: ============='
        cands = self.gen()
        print 'minimax.gen(): =======', cands
        if len(cands) == 0:
            return (None, None)
        best_move = None
        best_score = float('-inf')
        for c in cands:
            tmp = Action(c[0], c[1], False)
            newchessboard = self.play(tmp)
            score = self.min_play(newchessboard, depth)
            if score > best_score:
                best_move = c
                best_score = score
                # best score is the board's score
        print '(best_move, best_score): ', best_move, best_score
        return (best_move, best_score)

    def max_play(self, state, depth):
        if self.isGameOver(depth):
            print '*************max_play depth is 0*************'
            return state.evaluateBoard()
        print 'max_play: ============='
        cands = state.gen()
        print 'max_play.gen(): =======', cands
        best_score = float('-inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            tmp = Action(c[0], c[1], False)
            newchessboard = state.play(tmp)
            score = state.min_play(newchessboard, depth)
            if score > best_score:
                best_score = score
        print 'max_play best_score:', best_score
        return best_score


    def min_play(self, state, depth):
        if self.isGameOver(depth):
            return state.evaluateBoard()
        print 'min_play: ============='
        cands = state.gen()
        print 'min_play.gen(): =======', cands
        best_score = float('inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            tmp = Action(c[0], c[1], True)
            newchessboard = state.play(tmp)
            score = state.max_play(newchessboard, depth-1)
            if score < best_score:
                best_score = score
        print 'min_play best_score:', best_score
        return best_score

# ================Alpha-beta pruning========================

    def alpha_beta(self, depth):
        beta = float('inf')
        cands = self.gen()
        if len(cands) == 0:
            return (None, None)
        best_move = None
        best_score = float('-inf')
        for c in cands:
            tmp = Action(c[0], c[1], False)
            newchessboard = self.play(tmp)
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
        cands = state.gen()
        best_score = float('-inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            tmp = Action(c[0], c[1], False)
            newchessboard = state.play(tmp)
            score = state.min_play2(newchessboard, depth, alpha, beta)
            best_score = max(best_score, score)
            if best_score >= beta:
                return best_score
            alpha = max(alpha, best_score)
        return best_score


    def min_play2(self, state, depth, alpha, beta):
        if self.isGameOver(depth):
            return state.evaluateBoard()
        cands = state.gen()
        best_score = float('inf')
        if len(cands) == 0:
            return best_score
        for c in cands:
            tmp = Action(c[0], c[1], True)
            newchessboard = state.play(tmp)
            score = state.max_play2(newchessboard, depth-1, alpha, beta)
            best_score = min(best_score, score)
            if best_score <= alpha:
                return best_score
            beta = min(beta, best_score)
        return best_score

        

        
        
        
    