

from time import sleep
from math import inf
from random import randint

import time ## need to delete
class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.expandedNodesList=[]
        self.currPlayer=True

    ##### helper functions by hf
    def allSpotsInBoard(self,currBoardIdx):
        # return all spots in a local board
        xy = self.globalIdx[currBoardIdx]
        x = xy[0]
        y = xy[1]
        result = []
        for i in range(0,3):
            for j in range(0,3):
                result.append((x+i, y+j))
        return result
    def emptySpotsInBoard(self, currBoardIdx):
        # return all empty spots in a local board
        xy = self.globalIdx[currBoardIdx]
        x = xy[0]
        y = xy[1]
        result = []
        for i in range(0,3):
            for j in range(0,3):
                if self.board[x+i][y+j] == '_':
                    result.append((x+i, y+j))
        return result
    def makeMove(self, location, isMax):
        if isMax == 1:
            self.board[location[0]][location[1]] = 'X'
        elif isMax == 0:
            self.board[location[0]][location[1]] = '_'
        elif isMax == -1:
            self.board[location[0]][location[1]] = 'O'
    def ec_winlist(self):
        eclist = [0,0,0,0,0,0,0,0,0]
        for lineidx in range(9):
            local = int(int(lineidx) / 3)
            line = self.board[lineidx]
            if (line[0] == line[1] == line[2] == self.maxPlayer) or (line[3] == line[4] == line[5] == self.maxPlayer) or (line[6] == line[7] == line[8] == self.maxPlayer):
                eclist[local] = 1
            if (line[0] == line[1] == line[2] == self.minPlayer) or (line[3] == line[4] == line[5] == self.minPlayer) or (line[6] == line[7] == line[8] == self.minPlayer):
                eclist[local] = -1
        #check column wins
        for idx in range(9):
            start = self.globalIdx[idx]
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.maxPlayer:
                eclist[idx] = 1
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.minPlayer:
                eclist[idx] = -1
            if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.maxPlayer:
                eclist[idx] = 1
            if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.minPlayer:
                eclist[idx] = -1
            if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                eclist[idx] = 1
            if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                eclist[idx] = -1
        #check diagonal wins:
        for idx in range(9):
            start = self.globalIdx[idx]
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                eclist[idx] = 1
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                eclist[idx] = -1
            if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.maxPlayer:
                eclist[idx] = 1
            if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.minPlayer:
                eclist[idx] = -1
        #no winner:
        return eclist
    def ec_checkwin(self, eclist):
        if (eclist[0] == eclist[1] == eclist[2] == 1) :
            return 1
        if (eclist[0] == eclist[1] == eclist[2] == -1) :
            return -1
        if (eclist[3] == eclist[4] == eclist[5] == 1) :
            return 1
        if (eclist[3] == eclist[4] == eclist[5] == -1) :
            return -1
        if (eclist[6] == eclist[7] == eclist[8] == 1) :
            return 1
        if (eclist[6] == eclist[7] == eclist[8] == -1) :
            return -1
        #column
        if (eclist[0] == eclist[3] == eclist[6] == 1) :
            return 1
        if (eclist[0] == eclist[3] == eclist[6] == -1) :
            return -1
        if (eclist[1] == eclist[4] == eclist[7] == 1) :
            return 1
        if (eclist[1] == eclist[4] == eclist[7] == -1) :
            return -1
        if (eclist[2] == eclist[5] == eclist[8] == 1) :
            return 1
        if (eclist[2] == eclist[5] == eclist[8] == -1) :
            return -1
        #diagonal
        if (eclist[0] == eclist[4] == eclist[8] == 1) :
            return 1
        if (eclist[0] == eclist[4] == eclist[8] == -1) :
            return -1
        if (eclist[2] == eclist[4] == eclist[6] == 1) :
            return 1
        if (eclist[2] == eclist[4] == eclist[6] == -1) :
            return -1
        return 0
    #####
    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')
    def num_twos(self, player, opponent):
        """
        This is a helper function to count unblocked two-in-a-rows and prevented two-in-a-rows
        for the evaluation functions.
        110 MEANS PLAYER, PLAYER, OPPONENT!! (opponent blocks the two owned by player)
        :param player: either self.maxPlayer(X) or minPlayer(O)
        :param opponent: when opponent is '_', we are checking unblocked two-in-a-rows
                         or opponent is either 'X' or 'O'
        :return: number of unblocked two-in-a-rows owned by player
        """
        count = 0
        for start in self.globalIdx:
            if self.board[start[0]][start[1]] == player and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
                count += 1      #first row 110
            if self.board[start[0]][start[1]] == opponent and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
                count += 1      #first row 011
            if self.board[start[0]][start[1]] == player and self.board[start[0]][start[1] + 1] == opponent and self.board[start[0]][start[1] + 2] == player:
                count += 1      #first row 101
            if self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == opponent:
                count += 1      #second row 110
            if self.board[start[0] + 1][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == player:
                count += 1      #second row 011
            if self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 1][start[1] + 2] == player:
                count += 1      #second row 101
            if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
                count += 1      #third row 110
            if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1      #third row 011
            if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 2][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1      #third row 101
            # on cols (9 cases)
            if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == opponent:
                count += 1      #first col 110
            if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == player:
                count += 1      #first col 011
            if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1]] == opponent and self.board[start[0] + 2][start[1]] == player:
                count += 1      #first col 101
            if self.board[start[0]][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == opponent:
                count += 1      #second col 110
            if self.board[start[0]][start[1] + 1] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == player:
                count += 1      #second col 011
            if self.board[start[0]][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 1] == player:
                count += 1      #second col 101
            if self.board[start[0]][start[1] + 2] == player and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
                count += 1      #third col 110
            if self.board[start[0]][start[1] + 2] == opponent and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1      #third col 011
            if self.board[start[0]][start[1] + 2] == player and self.board[start[0] + 1][start[1] + 2] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1      #third col 101
            # on diagonals (6 cases)
            if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
                count += 1
            if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1
            if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
                count += 1
            if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
                count += 1
            if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
                count += 1
            if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0]][start[1] + 2] == player:
                count += 1
        return count
    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0.0
        if isMax:
            if self.checkWinner() == 1:
                return 10000.0
            #second rule:
            score += self.num_twos(self.maxPlayer, '_') * 500
            score += self.num_twos(self.minPlayer, self.maxPlayer) * 100
            if score != 0:
                return score
            #third rule: check corners
            for start in self.globalIdx:
                if self.board[start[0]][start[1]] == self.maxPlayer:
                    score += 30
                if self.board[start[0] + 2][start[1]] == self.maxPlayer:
                    score += 30
                if self.board[start[0]][start[1] + 2] == self.maxPlayer:
                    score += 30
                if self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                    score += 30
        else:
            if self.checkWinner() == -1:
                return -10000.0
            #second rule:
            score -= self.num_twos(self.minPlayer, '_') * 100
            score -= self.num_twos(self.maxPlayer, self.minPlayer) * 500
            if score != 0:
                return score
            #third rule: check corners
            for start in self.globalIdx:
                if self.board[start[0]][start[1]] == self.minPlayer:
                    score -= 30
                if self.board[start[0] + 2][start[1]] == self.minPlayer:
                    score -= 30
                if self.board[start[0]][start[1] + 2] == self.minPlayer:
                    score -= 30
                if self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                    score -= 30
        return score
    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0
        if self.checkWinner() == 1:
            return 10000
        if self.checkWinner() == -1:
            return -10000
        #second rule:
        score += self.num_twos(self.maxPlayer, '_') * 500
        score += self.num_twos(self.minPlayer, self.maxPlayer) * 100
        score -= self.num_twos(self.minPlayer, '_') * 500
        score -= self.num_twos(self.maxPlayer, self.minPlayer) * 100
        if score != 0:
            return score
        #third rule: check corners
        for start in self.globalIdx:
            if self.board[start[0]][start[1]] == self.maxPlayer:
                score += 30
            if self.board[start[0] + 2][start[1]] == self.maxPlayer:
                score += 30
            if self.board[start[0]][start[1] + 2] == self.maxPlayer:
                score += 30
            if self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                score += 30

        for start in self.globalIdx:
            if self.board[start[0]][start[1]] == self.minPlayer:
                score -= 30
            if self.board[start[0] + 2][start[1]] == self.minPlayer:
                score -= 30
            if self.board[start[0]][start[1] + 2] == self.minPlayer:
                score -= 30
            if self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                score -= 30
        return score
    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for line in self.board:
            for slot in line:
                if slot == '_':
                    return True
        return False
    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        #check row wins
        for line in self.board:
            if (line[0] == line[1] == line[2] == self.maxPlayer) or (line[3] == line[4] == line[5] == self.maxPlayer) or (line[6] == line[7] == line[8] == self.maxPlayer):
                return 1
            if (line[0] == line[1] == line[2] == self.minPlayer) or (line[3] == line[4] == line[5] == self.minPlayer) or (line[6] == line[7] == line[8] == self.minPlayer):
                return -1
        #check column wins
        for start in self.globalIdx:
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.minPlayer:
                return -1
            if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.minPlayer:
                return -1
            if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                return -1
        #check diagonal wins:
        for start in self.globalIdx:
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
                return 1
            if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
                return -1
            if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.maxPlayer:
                return 1
            if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.minPlayer:
                return -1
        #no winner:
        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if depth >= self.maxDepth:
            #self.printGameBoard()
            #print('eval',self.evaluatePredifined(not isMax),not isMax)
            self.expandedNodes += 1
            return self.evaluatePredifined(not isMax)
        if isMax: #maxPlayer
            allSpots = self.allSpotsInBoard(currBoardIdx)
            bestValue = -100000.0
            for i,spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot,1)
                    nextBoardIdx=spot[0]%3*3+(spot[1])%3
                    bestValue = max(bestValue,self.alphabeta(depth+1, nextBoardIdx, alpha, beta, False)) #minPlayer next
                    alpha = max(alpha, bestValue)
                    self.makeMove(spot,0)
                    if beta<=alpha:
                        break
        else: #minPlayer
            allSpots = self.allSpotsInBoard(currBoardIdx)
            bestValue=100000.0
            for i,spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot,-1)
                    nextBoardIdx=spot[0]%3*3+spot[1]%3
                    bestValue = min(bestValue,self.alphabeta(depth+1, nextBoardIdx, alpha, beta, True)) #maxPlayer next
                    beta = min(beta, bestValue)
                    self.makeMove(spot,0)
                    if beta<=alpha:
                        break
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        if depth >= self.maxDepth:
            self.expandedNodes += 1
            return self.evaluatePredifined(not isMax)
        if isMax: #maxPlayer
            allSpots = self.allSpotsInBoard(currBoardIdx)
            bestValue = -100000
            for i,spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot,1)
                    nextBoardIdx=spot[0]%3*3+(spot[1])%3
                    currValue = self.minimax(depth + 1, nextBoardIdx, False) #minPlayer next
                    bestValue = max(currValue, bestValue)
                    self.makeMove(spot,0)

        else: #minPlayer
            allSpots = self.allSpotsInBoard(currBoardIdx)
            bestValue=100000
            for i,spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':

                    self.makeMove(spot,-1)
                    nextBoardIdx=spot[0]%3*3+spot[1]%3
                    currValue = self.minimax(depth + 1, nextBoardIdx, True) #maxPlayer next
                    bestValue = min(currValue, bestValue)
                    self.makeMove(spot,0)
        return bestValue
    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE　
        print("playGamePredifinedAgent")
        turn = 1 # 1 for maxPlayer, -1 for minPlayer
        if (not maxFirst) :
            turn = -1
        currBoardIdx = self.startBoardIdx
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        alpha = -100000.0
        beta = 100000.0
        while self.checkWinner() == 0:
            alpha = -100000.0
            beta = 100000.0
            self.expandedNodes = 0
            if (turn == 1) :

                bestValueList = []
                bestMoveList  = []
                allSpots = self.allSpotsInBoard(currBoardIdx)
                for i, spot in enumerate(allSpots):
                    if self.board[spot[0]][spot[1]] == '_':

                        self.makeMove(spot, turn)
                        if (isMinimaxOffensive):
                            result = self.minimax(1, i, False)    #(spot[0]-spot[0]%3)*3+spot[1]-(spot[1])%3
                        else :
                            result = self.alphabeta(1,i,alpha,beta,False)
                            alpha = max(alpha, result)
                        #print("line275", i, spot, result)
                        bestValueList.append(result)
                        bestMoveList.append(spot)
                        self.makeMove(spot, 0)      # undo the makeMove

                best_value = max(bestValueList)
                index = bestValueList.index(best_value)
                best_move = bestMoveList[index]

            else :


                bestValueList = []
                bestMoveList  = []
                allSpots = self.allSpotsInBoard(currBoardIdx)
                for i, spot in enumerate(allSpots):
                    if self.board[spot[0]][spot[1]] == '_':

                        self.makeMove(spot, turn)
                        if (isMinimaxDefensive):
                            result = self.minimax(1, i, True)    #(spot[0]-spot[0]%3)*3+spot[1]-(spot[1])%3
                        else :
                            result = self.alphabeta(1,i,alpha,beta,True)
                            beta = min(beta, result)
                        bestValueList.append(result)
                        bestMoveList.append(spot)
                        self.makeMove(spot, 0)      # undo the makeMove

                best_value = min(bestValueList)
                index = bestValueList.index(best_value)
                best_move = bestMoveList[index]
            nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
            currBoardIdx = nextBoardIdx

            self.makeMove(best_move, turn)
            # self.printGameBoard()
            bestMove.append(best_move)
            bestValue.append(best_value)
            gameBoards.append(self.board.copy())
            # time.sleep(1)
            turn = -turn
            self.expandedNodesList.append(self.expandedNodes)


        winner = self.checkWinner()
        expandedNodes = self.expandedNodesList
        self.printGameBoard()
        print(type(bestMove[0]))
        print(type(bestValue[0]))
        print(type(expandedNodes[0]))
        return gameBoards, bestMove, expandedNodes, bestValue, winner
    def alphabeta_imp(self, depth, currBoardIdx,alpha,beta, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """

        #YOUR CODE HERE
        bestValue=0.0
        if depth == 0:
            return self.evaluateDesigned(isMax)
        else :
            turn = 1
            if not isMax:
                turn = -1
            bestValueList = []
            bestMoveList  = []
            allSpots = self.allSpotsInBoard(currBoardIdx)
            for i, spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot, turn)
                    if (self.checkWinner()+1)/2==isMax:
                        self.makeMove(spot, 0)
                        return 100000*(isMax*2-1), spot
                    result = self.alphabeta_recursive_imp(depth - 1, i, alpha, beta, not isMax)#(spot[0]-spot[0]%3)*3+spot[1]-(spot[1])%3
                    bestValueList.append(result)
                    bestMoveList.append(spot)
                    self.makeMove(spot, 0)      # undo the makeMove
            if (isMax) :
                bestValue = max(bestValueList)
            else :
                bestValue = min(bestValueList)
            #print(bestValue,bestValueList)
            #print(bestMoveList)
            index = bestValueList.index(bestValue)
            bestMove = bestMoveList[index]
        return bestValue, bestMove

    def alphabeta_recursive_imp(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        if depth == 0:
            #self.printGameBoard()
            #print('eval',self.evaluatePredifined(not isMax),not isMax)
            self.expandedNodes += 1
            return self.evaluateDesigned(not isMax)
        if isMax: #maxPlayer
            allSpots = self.allSpotsInBoard(currBoardIdx)
            bestValue = -100000
            for i,spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot,1)
                    nextBoardIdx=spot[0]%3*3+(spot[1])%3
                    bestValue = max(bestValue,self.alphabeta_recursive_imp(depth-1, nextBoardIdx, alpha, beta, False)) #minPlayer next
                    alpha = max(alpha, bestValue)
                    self.makeMove(spot,0)
                    if beta<=alpha:
                        break
        else: #minPlayer
            allSpots = self.allSpotsInBoard(currBoardIdx)
            bestValue=100000
            for i,spot in enumerate(allSpots):
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot,-1)
                    nextBoardIdx=spot[0]%3*3+spot[1]%3
                    bestValue = min(bestValue,self.alphabeta_recursive_imp(depth-1, nextBoardIdx, alpha, beta, True)) #maxPlayer next
                    beta = min(beta, bestValue)
                    self.makeMove(spot,0)
                    if beta<=alpha:
                        break
        return bestValue
    def alphabeta_imp_ec(self, depth, currBoardIdx,alpha,beta, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """

        #YOUR CODE HERE
        bestValue=0.0
        if depth == 0:
            return self.evaluateDesigned(isMax)
        else :
            turn = 1
            if not isMax:
                turn = -1
            bestValueList = []
            bestMoveList  = []
            allSpots = self.allSpotsInBoard(currBoardIdx)
            for i, spot in enumerate(allSpots):
                eclist = self.ec_winlist()
                if eclist[i] != 0:
                    continue
                if self.board[spot[0]][spot[1]] == '_':
                    self.makeMove(spot, turn)
                    if (self.checkWinner()+1)/2==isMax:
                        self.makeMove(spot, 0)
                        return 100000*(isMax*2-1), spot
                    result = self.alphabeta_recursive_imp(depth - 1, i, alpha, beta, not isMax)#(spot[0]-spot[0]%3)*3+spot[1]-(spot[1])%3
                    bestValueList.append(result)
                    bestMoveList.append(spot)
                    self.makeMove(spot, 0)      # undo the makeMove
            if (isMax) :
                bestValue = max(bestValueList)
            else :
                bestValue = min(bestValueList)
            #print(bestValue,bestValueList)
            #print(bestMoveList)
            index = bestValueList.index(bestValue)
            bestMove = bestMoveList[index]
        return bestValue, bestMove
    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        maxFirst = randint(0,1)==1
        startBoardIdx = randint(0,8)
        print("maxFirst", maxFirst, "startBoardIdx", startBoardIdx)
        turn = 1 # 1 for maxPlayer, -1 for minPlayer
        if (not maxFirst) :
            turn = -1
        currBoardIdx = startBoardIdx
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        alpha = -100000
        beta = 100000

        self.expandedNodesList = []
        while self.checkWinner() == 0:
            #self.printGameBoard()
            alpha = -100000.0
            beta = 100000.0
            self.expandedNodes = 0
            if (turn == 1) :
                #if (isPredefinedOffensive):
                bestValueList = []
                bestMoveList  = []
                allSpots = self.allSpotsInBoard(currBoardIdx)
                for i, spot in enumerate(allSpots):
                    if self.board[spot[0]][spot[1]] == '_':

                        self.makeMove(spot, turn)

                        result = self.alphabeta(1,i,alpha,beta,False)
                        alpha = max(alpha, result)
                        bestValueList.append(result)
                        bestMoveList.append(spot)
                        self.makeMove(spot, 0)      # undo the makeMove

                best_value = max(bestValueList)
                index = bestValueList.index(best_value)
                best_move = bestMoveList[index]

            else :

                best_value, best_move = self.alphabeta_imp(self.maxDepth,currBoardIdx,alpha,beta,False)
            nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
            currBoardIdx = nextBoardIdx

            self.makeMove(best_move, turn)
            #self.printGameBoard()
            bestMove.append(best_move)
            bestValue.append(best_value)
            gameBoards.append(self.board.copy())
            #time.sleep(1)
            turn = -turn
            self.expandedNodesList.append(self.expandedNodes)
        winner = self.checkWinner()
        self.printGameBoard()
        return gameBoards, bestMove, winner

    def checkValid(self, x, y, currBoardIdx):
        if (x >= 9 or x < 0 or y >= 9 or y < 0):
            print("Index out of bound! Please enter again.")
            return False
        if (self.board[x][y] != '_') :
            print("The spot has been put! Please enter again.")
            return False
        cx = self.globalIdx[currBoardIdx][0]
        cy = self.globalIdx[currBoardIdx][1]
        if (x < cx or x >= cx + 3 or y < cy or y >= cy + 3):
            print("You need to put in local board ", currBoardIdx, "! Please enter again.")
            return False
        return True
    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        print("playGameHuman")
        maxFirst = True
        isMinimaxOffensive = True
        turn = 1 # 1 for maxPlayer, -1 for minPlayerß
        currBoardIdx = self.startBoardIdx
        bestMove=[]
        gameBoards=[]
        while self.checkWinner() == 0:
            alpha = -100000.0
            beta = 100000.0
            if (turn == 1) :
                best_value, best_move = self.alphabeta_imp(self.maxDepth,currBoardIdx,alpha,beta,False)

            else :
                print("waiting for human move")
                valid = False
                x = 0
                y = 0
                while not valid:

                    x = int(input("enter the row you want to put: "))
                    y = int(input("enter the column you want to put: "))
                    valid = self.checkValid(x,y, currBoardIdx)
                best_move = (x,y)



            #print(best_move)
            nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
            currBoardIdx = nextBoardIdx

            self.makeMove(best_move, turn)
            self.printGameBoard()
            bestMove.append(best_move)
            gameBoards.append(self.board.copy())
            #time.sleep(1)
            turn = -turn


        winner = self.checkWinner()
        self.printGameBoard()
        return gameBoards, bestMove, winner
    def ec(self):
        maxFirst = randint(0,1)==1
        startBoardIdx = randint(0,8)
        print("maxFirst", maxFirst, "startBoardIdx", startBoardIdx)
        turn = 1 # 1 for maxPlayer, -1 for minPlayer
        if (not maxFirst) :
            turn = -1
        currBoardIdx = startBoardIdx
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        alpha = -100000
        beta = 100000

        self.expandedNodesList = []
        eclist = [0,0,0,0,0,0,0,0,0]
        while self.ec_checkwin(eclist) == 0:
            #self.printGameBoard()
            alpha = -100000.0
            beta = 100000.0
            self.expandedNodes = 0
            if (turn == 1) :
                #if (isPredefinedOffensive):
                best_value, best_move = self.alphabeta_imp_ec(self.maxDepth,currBoardIdx,alpha,beta,False)

            else :

                best_value, best_move = self.alphabeta_imp_ec(self.maxDepth,currBoardIdx,alpha,beta,False)
            nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
            currBoardIdx = nextBoardIdx

            self.makeMove(best_move, turn)
            #self.printGameBoard()
            bestMove.append(best_move)
            bestValue.append(best_value)
            gameBoards.append(self.board.copy())
            #time.sleep(1)
            turn = -turn
            self.expandedNodesList.append(self.expandedNodes)
            eclist = self.ec_winlist()
            if eclist[currBoardIdx] != 0 :
                break
        winner = self.ec_checkwin(eclist)
        self.printGameBoard()
        return gameBoards, bestMove, winner
if __name__=="__main__":


    uttt=ultimateTicTacToe()
    #gameBoards, bestMove, winner = uttt.ec()
    gameBoards, bestMove, winner=uttt.playGameYourAgent()
    #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,False,True)
    #print(gameBoards)
    print(bestMove)
    # print(expandedNodes)
    # print(bestValue)
    print(winner)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
# if __name__=="__main__":
#     uttt=ultimateTicTacToe()
#     #gameBoards, bestMove, winner=uttt.playGameHuman()
#     #gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
#
#     '''if winner == 1:
#         print("The winner is maxPlayer!!!")
#     elif winner == -1:
#         print("The winner is minPlayer!!!")
#     else:
#         print("Tie. No winner:(")
#         numPlay = 50'''
#     print('MaxPlayerWinRate:',win/numPlay*100,'%')
#     if win/numPlay*100 > 50:
#         print("The final winner is maxPlayer!!!")
#     elif win/numPlay*100 < 50:
#         print("The final winner is minPlayer!!!")
#     else:
#         print("Tie. No winner:(")
# from time import sleep
# from math import inf
# from random import randint
#
# import time ## need to delete
# class ultimateTicTacToe:
#     def __init__(self):
#         """
#         Initialization of the game.
#         """
#         self.board=[['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_'],
#                     ['_','_','_','_','_','_','_','_','_']]
#         self.maxPlayer='X'
#         self.minPlayer='O'
#         self.maxDepth=3
#         #The start indexes of each local board
#         self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]
#
#         #Start local board index for reflex agent playing
#         self.startBoardIdx=4
#         #self.startBoardIdx=randint(0,8)
#
#         #utility value for reflex offensive and reflex defensive agents
#         self.winnerMaxUtility=10000
#         self.twoInARowMaxUtility=500
#         self.preventThreeInARowMaxUtility=100
#         self.cornerMaxUtility=30
#
#         self.winnerMinUtility=-10000
#         self.twoInARowMinUtility=-100
#         self.preventThreeInARowMinUtility=-500
#         self.cornerMinUtility=-30
#
#         self.expandedNodes=0
#         self.currPlayer=True
#
#     ##### helper functions by hf
#     def allSpotsInBoard(self,currBoardIdx):
#         # return all spots in a local board
#         xy = self.globalIdx[currBoardIdx]
#         x = xy[0]
#         y = xy[1]
#         result = []
#         for i in range(0,3):
#             for j in range(0,3):
#                 result.append((x+i, y+j))
#         return result
#     def emptySpotsInBoard(self, currBoardIdx):
#         # return all empty spots in a local board
#         xy = self.globalIdx[currBoardIdx]
#         x = xy[0]
#         y = xy[1]
#         result = []
#         for i in range(0,3):
#             for j in range(0,3):
#                 if self.board[x+i][y+j] == '_':
#                     result.append((x+i, y+j))
#         return result
#     def makeMove(self, location, isMax):
#         if isMax == 1:
#             self.board[location[0]][location[1]] = 'X'
#         elif isMax == 0:
#             self.board[location[0]][location[1]] = '_'
#         elif isMax == -1:
#             self.board[location[0]][location[1]] = 'O'
#     #####
#     def printGameBoard(self):
#         """
#         This function prints the current game board.
#         """
#         print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
#         print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
#         print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')
#     def num_twos(self, player, opponent):
#         """
#         This is a helper function to count unblocked two-in-a-rows and prevented two-in-a-rows
#         for the evaluation functions.
#         110 MEANS PLAYER, PLAYER, OPPONENT!! (opponent blocks the two owned by player)
#         :param player: either self.maxPlayer(X) or minPlayer(O)
#         :param opponent: when opponent is '_', we are checking unblocked two-in-a-rows
#                          or opponent is either 'X' or 'O'
#         :return: number of unblocked two-in-a-rows owned by player
#         """
#         count = 0
#         for start in self.globalIdx:
#             if self.board[start[0]][start[1]] == player and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
#                 count += 1      #first row 110
#             if self.board[start[0]][start[1]] == opponent and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
#                 count += 1      #first row 011
#             if self.board[start[0]][start[1]] == player and self.board[start[0]][start[1] + 1] == opponent and self.board[start[0]][start[1] + 2] == player:
#                 count += 1      #first row 101
#             if self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == opponent:
#                 count += 1      #second row 110
#             if self.board[start[0] + 1][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == player:
#                 count += 1      #second row 011
#             if self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 1][start[1] + 2] == player:
#                 count += 1      #second row 101
#             if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
#                 count += 1      #third row 110
#             if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
#                 count += 1      #third row 011
#             if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 2][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
#                 count += 1      #third row 101
#             # on cols (9 cases)
#             if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == opponent:
#                 count += 1      #first col 110
#             if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == player:
#                 count += 1      #first col 011
#             if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1]] == opponent and self.board[start[0] + 2][start[1]] == player:
#                 count += 1      #first col 101
#             if self.board[start[0]][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == opponent:
#                 count += 1      #second col 110
#             if self.board[start[0]][start[1] + 1] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == player:
#                 count += 1      #second col 011
#             if self.board[start[0]][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 1] == player:
#                 count += 1      #second col 101
#             if self.board[start[0]][start[1] + 2] == player and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
#                 count += 1      #third col 110
#             if self.board[start[0]][start[1] + 2] == opponent and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == player:
#                 count += 1      #third col 011
#             if self.board[start[0]][start[1] + 2] == player and self.board[start[0] + 1][start[1] + 2] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
#                 count += 1      #third col 101
#             # on diagonals (6 cases)
#             if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
#                 count += 1
#             if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
#                 count += 1
#             if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
#                 count += 1
#             if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
#                 count += 1
#             if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
#                 count += 1
#             if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0]][start[1] + 2] == player:
#                 count += 1
#         return count
#     def dangerous_num_twos(self, player, currBoardIdx):
#         """
#         This is a helper function to count unblocked two-in-a-rows and prevented two-in-a-rows
#         for the evaluation functions.
#         110 MEANS PLAYER, PLAYER, OPPONENT!! (opponent blocks the two owned by player)
#         :param player: either self.maxPlayer(X) or minPlayer(O)
#         :param opponent: when opponent is '_', we are checking unblocked two-in-a-rows
#                          or opponent is either 'X' or 'O'
#         :return: number of unblocked two-in-a-rows owned by player
#         """
#         opponent = '_'
#         count = 0
#         start = self.globalIdx[currBoardIdx]
#         # on rows (9 cases)
#         if self.board[start[0]][start[1]] == player and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
#             count += 1      #first row 110
#         if self.board[start[0]][start[1]] == opponent and self.board[start[0]][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
#             count += 1      #first row 011
#         if self.board[start[0]][start[1]] == player and self.board[start[0]][start[1] + 1] == opponent and self.board[start[0]][start[1] + 2] == player:
#             count += 1      #first row 101
#         if self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == opponent:
#             count += 1      #second row 110
#         if self.board[start[0] + 1][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 2] == player:
#             count += 1      #second row 011
#         if self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 1][start[1] + 2] == player:
#             count += 1      #second row 101
#         if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
#             count += 1      #third row 110
#         if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 2][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
#             count += 1      #third row 011
#         if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 2][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
#             count += 1      #third row 101
#         # on cols (9 cases)
#         if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == opponent:
#             count += 1      #first col 110
#         if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1]] == player and self.board[start[0] + 2][start[1]] == player:
#             count += 1      #first col 011
#         if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1]] == opponent and self.board[start[0] + 2][start[1]] == player:
#             count += 1      #first col 101
#         if self.board[start[0]][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == opponent:
#             count += 1      #second col 110
#         if self.board[start[0]][start[1] + 1] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 1] == player:
#             count += 1      #second col 011
#         if self.board[start[0]][start[1] + 1] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 1] == player:
#             count += 1      #second col 101
#         if self.board[start[0]][start[1] + 2] == player and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
#             count += 1      #third col 110
#         if self.board[start[0]][start[1] + 2] == opponent and self.board[start[0] + 1][start[1] + 2] == player and self.board[start[0] + 2][start[1] + 2] == player:
#             count += 1      #third col 011
#         if self.board[start[0]][start[1] + 2] == player and self.board[start[0] + 1][start[1] + 2] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
#             count += 1      #third col 101
#         # on diagonals (6 cases)
#         if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == opponent:
#             count += 1
#         if self.board[start[0]][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0] + 2][start[1] + 2] == player:
#             count += 1
#         if self.board[start[0]][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0] + 2][start[1] + 2] == player:
#             count += 1
#         if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == opponent:
#             count += 1
#         if self.board[start[0] + 2][start[1]] == opponent and self.board[start[0] + 1][start[1] + 1] == player and self.board[start[0]][start[1] + 2] == player:
#             count += 1
#         if self.board[start[0] + 2][start[1]] == player and self.board[start[0] + 1][start[1] + 1] == opponent and self.board[start[0]][start[1] + 2] == player:
#             count += 1
#         return count
#     ## helper
#     def evaluatePredifined(self, isMax):
#         """
#         This function implements the evaluation function for ultimate tic tac toe for predifined agent.
#         input args:
#         isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
#                      True for maxPlayer, False for minPlayer
#         output:
#         score(float): estimated utility score for maxPlayer or minPlayer
#         """
#         #YOUR CODE HERE
#         score = 0
#         if isMax:
#             if self.checkWinner() == 1:
#                 return 10000
#             #second rule:
#             score += self.num_twos(self.maxPlayer, '_') * 500
#             score += self.num_twos(self.minPlayer, self.maxPlayer) * 100
#             if score != 0:
#                 return score
#             #third rule: check corners
#             for start in self.globalIdx:
#                 if self.board[start[0]][start[1]] == self.maxPlayer:
#                     score += 30
#                 if self.board[start[0] + 2][start[1]] == self.maxPlayer:
#                     score += 30
#                 if self.board[start[0]][start[1] + 2] == self.maxPlayer:
#                     score += 30
#                 if self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
#                     score += 30
#         else:
#             if self.checkWinner() == -1:
#                 return -10000
#             #second rule:
#             score -= self.num_twos(self.minPlayer, '_') * 100
#             score -= self.num_twos(self.maxPlayer, self.minPlayer) * 500
#             if score != 0:
#                 return score
#             #third rule: check corners
#             for start in self.globalIdx:
#                 if self.board[start[0]][start[1]] == self.minPlayer:
#                     score -= 30
#                 if self.board[start[0] + 2][start[1]] == self.minPlayer:
#                     score -= 30
#                 if self.board[start[0]][start[1] + 2] == self.minPlayer:
#                     score -= 30
#                 if self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
#                     score -= 30
#         return score
#     def evaluateDesigned(self, isMax):
#         """
#         This function implements the evaluation function for ultimate tic tac toe for your own agent.
#         input args:
#         isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
#                      True for maxPlayer, False for minPlayer
#         output:
#         score(float): estimated utility score for maxPlayer or minPlayer
#         """
#         #YOUR CODE HERE
#         score = 0
#         if self.checkWinner() == 1:
#             return 10000
#         if self.checkWinner() == -1:
#             return -10000
#         #second rule:
#         score += self.num_twos(self.maxPlayer, '_') * 500
#         score += self.num_twos(self.minPlayer, self.maxPlayer) * 100
#         score -= self.num_twos(self.minPlayer, '_') * 500
#         score -= self.num_twos(self.maxPlayer, self.minPlayer) * 100
#         if score != 0:
#             return score
#         #third rule: check corners
#         for start in self.globalIdx:
#             if self.board[start[0]][start[1]] == self.maxPlayer:
#                 score += 30
#             if self.board[start[0] + 2][start[1]] == self.maxPlayer:
#                 score += 30
#             if self.board[start[0]][start[1] + 2] == self.maxPlayer:
#                 score += 30
#             if self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
#                 score += 30
#
#         for start in self.globalIdx:
#             if self.board[start[0]][start[1]] == self.minPlayer:
#                 score -= 30
#             if self.board[start[0] + 2][start[1]] == self.minPlayer:
#                 score -= 30
#             if self.board[start[0]][start[1] + 2] == self.minPlayer:
#                 score -= 30
#             if self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
#                 score -= 30
#         return score
#     ## helper
#     def evaluateDangerous(self, isMax, currBoardIdx):
#         if (isMax):
#             if self.dangerous_num_twos('O', currBoardIdx):
#                 return -10000
#             else :
#                 return 0
#         else :
#             if self.dangerous_num_twos('X', currBoardIdx):
#                 return 10000
#             else :
#                 return 0
#         return 0
#     def checkMovesLeft(self):
#         """
#         This function checks whether any legal move remains on the board.
#         output:
#         movesLeft(bool): boolean variable indicates whether any legal move remains
#                         on the board.
#         """
#         #YOUR CODE HERE
#         for line in self.board:
#             for slot in line:
#                 if slot == '_':
#                     return True
#         return False
#     def checkWinner(self):
#         #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
#         """
#         This function checks whether there is a winner on the board.
#         output:
#         winner(int): Return 0 if there is no winner.
#                      Return 1 if maxPlayer is the winner.
#                      Return -1 if miniPlayer is the winner.
#         """
#         #YOUR CODE HERE
#         #check row wins
#         for line in self.board:
#             if (line[0] == line[1] == line[2] == self.maxPlayer) or (line[3] == line[4] == line[5] == self.maxPlayer) or (line[6] == line[7] == line[8] == self.maxPlayer):
#                 return 1
#             if (line[0] == line[1] == line[2] == self.minPlayer) or (line[3] == line[4] == line[5] == self.minPlayer) or (line[6] == line[7] == line[8] == self.minPlayer):
#                 return -1
#         #check column wins
#         for start in self.globalIdx:
#             if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.maxPlayer:
#                 return 1
#             if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] ] == self.board[start[0]+ 2 ][start[1]] == self.minPlayer:
#                 return -1
#             if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.maxPlayer:
#                 return 1
#             if self.board[start[0]][start[1] + 1] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 1] == self.minPlayer:
#                 return -1
#             if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
#                 return 1
#             if self.board[start[0]][start[1] + 2] == self.board[start[0] + 1][start[1] + 2] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
#                 return -1
#         #check diagonal wins:
#         for start in self.globalIdx:
#             if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.maxPlayer:
#                 return 1
#             if self.board[start[0]][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0] + 2][start[1] + 2] == self.minPlayer:
#                 return -1
#             if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.maxPlayer:
#                 return 1
#             if self.board[start[0] + 2][start[1]] == self.board[start[0] + 1][start[1] + 1] == self.board[start[0]][start[1] + 2] == self.minPlayer:
#                 return -1
#         #no winner:
#         return 0
#     def alphabeta(self, depth, currBoardIdx,alpha,beta, isMax):
#         """
#         This function implements minimax algorithm for ultimate tic-tac-toe game.
#         input args:
#         depth(int): current depth level
#         currBoardIdx(int): current local board index
#         alpha(float): alpha value
#         beta(float): beta value
#         isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
#                      True for maxPlayer, False for minPlayer
#         output:
#         bestValue(float):the bestValue that current player may have
#         """
#
#         #YOUR CODE HERE
#         bestValue=0.0
#         if depth == 0:
#             return self.evaluatePredifined(isMax)
#         else :
#             turn = 1
#             if not isMax:
#                 turn = -1
#             bestValueList = []
#             bestMoveList  = []
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             for i, spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#                     self.makeMove(spot, turn)
#                     result = self.alphabeta_recursive(depth - 1, i, alpha, beta, not isMax)#(spot[0]-spot[0]%3)*3+spot[1]-(spot[1])%3
#                     bestValueList.append(result)
#                     bestMoveList.append(spot)
#                     self.makeMove(spot, 0)      # undo the makeMove
#             if (isMax) :
#                 bestValue = max(bestValueList)
#             else :
#                 bestValue = min(bestValueList)
#             #print(bestValue,bestValueList)
#             #print(bestMoveList)
#             index = bestValueList.index(bestValue)
#             bestMove = bestMoveList[index]
#         return bestValue, bestMove
#
#     def alphabeta_recursive(self,depth,currBoardIdx,alpha,beta,isMax):
#         """
#         This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
#         input args:
#         depth(int): current depth level
#         currBoardIdx(int): current local board index
#         alpha(float): alpha value
#         beta(float): beta value
#         isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
#                      True for maxPlayer, False for minPlayer
#         output:
#         bestValue(float):the bestValue that current player may have
#         """
#         #YOUR CODE HERE
#         if depth == 0:
#             #self.printGameBoard()
#             #print('eval',self.evaluatePredifined(not isMax),not isMax)
#             return self.evaluatePredifined(not isMax)
#         if isMax: #maxPlayer
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             bestValue = -100000
#             for i,spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#
#                     self.makeMove(spot,1)
#                     nextBoardIdx=spot[0]%3*3+(spot[1])%3
#                     bestValue = max(bestValue,self.alphabeta_recursive(depth-1, nextBoardIdx, alpha, beta, False)) #minPlayer next
#                     alpha = max(alpha, bestValue)
#                     self.makeMove(spot,0)
#                     if beta<=alpha:
#                         break
#         else: #minPlayer
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             bestValue=100000
#             for i,spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#
#                     self.makeMove(spot,-1)
#                     nextBoardIdx=spot[0]%3*3+spot[1]%3
#                     bestValue = min(bestValue,self.alphabeta_recursive(depth-1, nextBoardIdx, alpha, beta, True)) #maxPlayer next
#                     beta = min(beta, bestValue)
#                     self.makeMove(spot,0)
#                     if beta<=alpha:
#                         break
#         return bestValue
#     def alphabeta_imp(self, depth, currBoardIdx,alpha,beta, isMax):
#         """
#         This function implements minimax algorithm for ultimate tic-tac-toe game.
#         input args:
#         depth(int): current depth level
#         currBoardIdx(int): current local board index
#         alpha(float): alpha value
#         beta(float): beta value
#         isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
#                      True for maxPlayer, False for minPlayer
#         output:
#         bestValue(float):the bestValue that current player may have
#         """
#
#         #YOUR CODE HERE
#         bestValue=0.0
#         if depth == 0:
#             return self.evaluatePredifined(isMax)
#         else :
#             turn = 1
#             if not isMax:
#                 turn = -1
#             bestValueList = []
#             bestMoveList  = []
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             for i, spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#                     self.makeMove(spot, turn)
#                     result = self.alphabeta_recursive_imp(depth - 1, i, alpha, beta, not isMax)#(spot[0]-spot[0]%3)*3+spot[1]-(spot[1])%3
#                     bestValueList.append(result)
#                     bestMoveList.append(spot)
#                     self.makeMove(spot, 0)      # undo the makeMove
#             if (isMax) :
#                 bestValue = max(bestValueList)
#             else :
#                 bestValue = min(bestValueList)
#             #print(bestValue,bestValueList)
#             #print(bestMoveList)
#             index = bestValueList.index(bestValue)
#             bestMove = bestMoveList[index]
#         return bestValue, bestMove
#
#     def alphabeta_recursive_imp(self,depth,currBoardIdx,alpha,beta,isMax):
#         """
#         This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
#         input args:
#         depth(int): current depth level
#         currBoardIdx(int): current local board index
#         alpha(float): alpha value
#         beta(float): beta value
#         isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
#                      True for maxPlayer, False for minPlayer
#         output:
#         bestValue(float):the bestValue that current player may have
#         """
#         #YOUR CODE HERE
#         if depth == 0:
#             #self.printGameBoard()
#             #print('eval',self.evaluatePredifined(not isMax),not isMax)
#             danger =  self.evaluateDangerous(isMax, currBoardIdx)
#             if danger != 0:
#                 return danger
#             return self.evaluateDesigned(not isMax)
#         if isMax: #maxPlayer
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             bestValue = -100000
#             for i,spot in enumerate(allSpots):
#
#                 if self.board[spot[0]][spot[1]] == '_':
#
#                     self.makeMove(spot,1)
#                     nextBoardIdx=spot[0]%3*3+(spot[1])%3
#                     bestValue = max(bestValue,self.alphabeta_recursive_imp(depth-1, nextBoardIdx, alpha, beta, False)) #minPlayer next
#                     alpha = max(alpha, bestValue)
#                     self.makeMove(spot,0)
#                     if beta<=alpha:
#                         break
#         else: #minPlayer
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             bestValue=100000
#             for i,spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#
#                     self.makeMove(spot,-1)
#                     nextBoardIdx=spot[0]%3*3+spot[1]%3
#                     bestValue = min(bestValue,self.alphabeta_recursive_imp(depth-1, nextBoardIdx, alpha, beta, True)) #maxPlayer next
#                     beta = min(beta, bestValue)
#                     self.makeMove(spot,0)
#                     if beta<=alpha:
#                         break
#         return bestValue
#     def minimax(self, depth, currBoardIdx, isMax):
#         #YOUR CODE HERE
#         bestValue=0.0
#         if depth == 0:
#
#             return self.evaluatePredifined(isMax)
#         else :
#             turn = 1
#             if not isMax:
#                 turn = -1
#             bestValueList = []
#             bestMoveList  = []
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             for i, spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#
#                     self.makeMove(spot, turn)
#                     result = self.minimax_recursive(depth - 1, i, not isMax)#(spot[0]-spot[0]%3)*3+spot[1]-(spot[1])%3
#                     print("line275", i, spot, result)
#                     bestValueList.append(result)
#                     bestMoveList.append(spot)
#                     if spot == (4,4):
#                         print("line 564", bestValue)
#                     self.makeMove(spot, 0)      # undo the makeMove
#             if (isMax) :
#                 bestValue = max(bestValueList)
#             else :
#                 bestValue = min(bestValueList)
#             #print(bestValue,bestValueList)
#             #print(bestMoveList)
#             index = bestValueList.index(bestValue)
#             bestMove = bestMoveList[index]
#             print("line572", bestValue, bestMove)
#         return bestValue, bestMove
#     ### recursive helper by hf
#     # def minimax(self, depth, currBoardIdx, isMax):
#     #     bestValue=0.0
#     #     if depth == 1:
#     #         return self.evaluatePredifined(isMax)
#     #     else :
#     #         bestValueList = []
#     #         bestMoveList  = []
#     #         allSpots = self.allSpotsInBoard(currBoardIdx)
#     #         if isMax:
#     #             for i, spot in enumerate(allSpots):
#     #                 if self.board[spot[0]][spot[1]] == '_':
#     #                     self.makeMove(spot, 1)
#     #                     bestValue_max, bestValue_min = self.minimax_recursive(depth - 1, i, not isMax)
#     #                     bestValueList.append(bestValue_max)
#     #                     bestMoveList.append(spot)
#     #                     self.makeMove(spot, 0)      # undo the makeMove
#     #             bestValue = max(bestValueList)
#     #         else:
#     #             for i, spot in enumerate(allSpots):
#     #                 if self.board[spot[0]][spot[1]] == '_':
#     #                     self.makeMove(spot, -1)
#     #                     bestValue_max, bestValue_min = self.minimax_recursive(depth - 1, i, not isMax)
#     #                     bestValueList.append(bestValue_min)
#     #                     bestMoveList.append(spot)
#     #                     self.makeMove(spot, 0)      # undo the makeMove
#     #             bestValue = min(bestValueList)
#     #             print("line 289", bestValue)
#     #         index = bestValueList.index(bestValue)
#     #         bestMove = bestMoveList[index]
#     #     print("line 311", bestValue, isMax)
#     #     return bestValue, bestMove
#     # def minimax_recursive(self, depth, currBoardIdx, isMax):
#     #     bestValue=0.0
#     #     if depth == 0:
#     #
#     #
#     #         bestValue_max = self.evaluatePredifined(True)
#     #         bestValue_min = self.evaluatePredifined(False)
#     #
#     #         return bestValue_max, bestValue_min
#     #     else :
#     #         bestValueList_max = []
#     #         bestValueList_min = []
#     #         allSpots = self.allSpotsInBoard(currBoardIdx)
#     #         if isMax:
#     #             for i, spot in enumerate(allSpots):
#     #                 if self.board[spot[0]][spot[1]] == '_':
#     #                     self.makeMove(spot, 1)
#     #                     bestValue_max, bestValue_min = self.minimax_recursive(depth - 1, i, not isMax)
#     #                     bestValueList_max.append(bestValue_max)
#     #                     bestValueList_min.append(bestValue_min)
#     #                     self.makeMove(spot, 0)      # undo the makeMove
#     #             bestValue_max = max(bestValueList_max)
#     #             index = bestValueList_max.index(bestValue_max)
#     #             bestValue_min = bestValueList_min[index]
#     #         else:
#     #             for i, spot in enumerate(allSpots):
#     #                 if self.board[spot[0]][spot[1]] == '_':
#     #                     self.makeMove(spot, -1)
#     #                     bestValue_max, bestValue_min = self.minimax_recursive(depth - 1, i, not isMax)
#     #
#     #                     bestValueList_max.append(bestValue_max)
#     #                     bestValueList_min.append(bestValue_min)
#     #                     self.makeMove(spot, 0)      # undo the makeMove
#     #             bestValue_min = min(bestValueList_min)
#     #             index = bestValueList_min.index(bestValue_min)
#     #             bestValue_max = bestValueList_max[index]
#     #         #print("line 353", bestValue_max,bestValue_min)
#     #     return bestValue_max, bestValue_min
#     def minimax_recursive(self, depth, currBoardIdx, isMax):
#         if depth == 0:
#             #self.printGameBoard()
#             #print('eval',self.evaluatePredifined(not isMax),not isMax)
#             if (self.evaluatePredifined(isMax) == -500):
#                 print("line547")
#                 self.printGameBoard()
#             return self.evaluatePredifined(not isMax)
#         if isMax: #maxPlayer
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             bestValue = -100000
#             for i,spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#
#                     self.makeMove(spot,1)
#                     nextBoardIdx=spot[0]%3*3+(spot[1])%3
#                     currValue = self.minimax_recursive(depth-1, nextBoardIdx, False) #minPlayer next
#                     bestValue = max(currValue, bestValue)
#                     if (depth == 2 and currBoardIdx == 4) :
#                         print("line664", i, spot, bestValue)
#                     self.makeMove(spot,0)
#
#         else: #minPlayer
#             allSpots = self.allSpotsInBoard(currBoardIdx)
#             bestValue=100000
#             for i,spot in enumerate(allSpots):
#                 if self.board[spot[0]][spot[1]] == '_':
#
#                     self.makeMove(spot,-1)
#                     nextBoardIdx=spot[0]%3*3+spot[1]%3
#                     currValue = self.minimax_recursive(depth-1, nextBoardIdx, True) #maxPlayer next
#                     bestValue = min(currValue, bestValue)
#                     self.makeMove(spot,0)
#         if (depth == 2 and currBoardIdx == 4) :
#             print("depth == 2 and currBoardIdx == 4",  bestValue)
#         return bestValue
#     def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
#         """
#         This function implements the processes of the game of predifined offensive agent vs defensive agent.
#         input args:
#         maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
#                         True for maxPlayer plays first, and False for minPlayer plays first.
#         isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
#                         True is minimax and False is alpha-beta.
#         isMinimaxDefensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
#                         True is minimax and False is alpha-beta.
#         output:
#         bestMove(list of tuple): list of bestMove coordinates at each step
#         bestValue(list of float): list of bestValue at each move
#         expandedNodes(list of int): list of expanded nodes at each move
#         gameBoards(list of 2d lists): list of game board positions at each move
#         winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
#         """
#         #YOUR CODE HERE　
#         print("playGamePredifinedAgent")
#         turn = 1 # 1 for maxPlayer, -1 for minPlayer
#         if (not maxFirst) :
#             turn = -1
#         currBoardIdx = self.startBoardIdx
#         bestMove=[]
#         bestValue=[]
#         gameBoards=[]
#         alpha = -100000
#         beta = 100000
#         while self.checkWinner() == 0:
#             #self.printGameBoard()
#             if (turn == 1) :
#                 if (isMinimaxOffensive):
#                     best_value, best_move = self.minimax(self.maxDepth, currBoardIdx, True)
#                 else :
#                     best_value, best_move = self.alphabeta(self.maxDepth,currBoardIdx,alpha,beta,True) ## not implemented yet
#
#             else :
#
#                 if (isMinimaxDefensive):
#                     best_value, best_move = self.minimax(self.maxDepth, currBoardIdx, False)
#                 else :
#                     best_value, best_move = self.alphabeta(self.maxDepth,currBoardIdx,alpha,beta,False) ## not implemented yet
#             print(best_move)
#             nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
#             currBoardIdx = nextBoardIdx
#
#             self.makeMove(best_move, turn)
#             self.printGameBoard()
#             print("=======================new move ==============")
#             bestMove.append(best_move)
#             bestValue.append(best_value)
#             gameBoards.append(self.board.copy())
#             time.sleep(1)
#             turn = -turn
#
#
#         winner = self.checkWinner()
#         expandedNodes = 0
#         self.printGameBoard()
#         return gameBoards, bestMove, expandedNodes, bestValue, winner
#
#     def playGameYourAgent(self):
#         """
#         This function implements the processes of the game of your own agent vs predifined offensive agent.
#         input args:
#         output:
#         bestMove(list of tuple): list of bestMove coordinates at each step
#         gameBoards(list of 2d lists): list of game board positions at each move
#         winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
#         """
#         #YOUR CODE HERE
#         maxFirst = randint(0,1)==1
#         startBoardIdx = randint(0,8)
#         maxFirst = 1
#         startBoardIdx = 2
#         bestMove=[]
#         gameBoards=[]
#         winner=0
#
#         turn = 1 # 1 for maxPlayer, -1 for minPlayer
#         if (not maxFirst) :
#             turn = -1
#         currBoardIdx = startBoardIdx
#
#         alpha = -100000
#         beta = 100000
#         while self.checkWinner() == 0:
#             #self.printGameBoard()
#             if (turn == 1) :
#                 best_value, best_move = self.alphabeta(self.maxDepth,currBoardIdx,alpha,beta,True)
#             else :
#                 best_value, best_move = self.alphabeta_imp(self.maxDepth,currBoardIdx,alpha,beta,False)
#             print(best_move)
#             nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
#             currBoardIdx = nextBoardIdx
#
#             self.makeMove(best_move, turn)
#             #self.printGameBoard()
#             bestMove.append(best_move)
#
#             gameBoards.append(self.board.copy())
#             #time.sleep(1)
#             turn = -turn
#
#
#         winner = self.checkWinner()
#         expandedNodes = 0
#         self.printGameBoard()
#         return gameBoards, bestMove, winner
#
#     def checkValid(self, x, y, currBoardIdx):
#         if (x >= 9 or x < 0 or y >= 9 or y < 0):
#             print("Index out of bound! Please enter again.")
#             return False
#         if (self.board[x][y] != '_') :
#             print("The spot has been put! Please enter again.")
#             return False
#         cx = self.globalIdx[currBoardIdx][0]
#         cy = self.globalIdx[currBoardIdx][1]
#         if (x < cx or x >= cx + 3 or y < cy or y >= cy + 3):
#             print("You need to put in local board ", currBoardIdx, "! Please enter again.")
#             return False
#         return True
#     def playGameHuman(self):
#         """
#         This function implements the processes of the game of your own agent vs a human.
#         output:
#         bestMove(list of tuple): list of bestMove coordinates at each step
#         gameBoards(list of 2d lists): list of game board positions at each move
#         winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
#         """
#         #YOUR CODE HERE
#         print("playGameHuman")
#         maxFirst = True
#         isMinimaxOffensive = True
#         turn = 1 # 1 for maxPlayer, -1 for minPlayerß
#         currBoardIdx = self.startBoardIdx
#         bestMove=[]
#         gameBoards=[]
#         while self.checkWinner() == 0:
#             #self.printGameBoard()
#             if (turn == 1) :
#                 if (isMinimaxOffensive):
#                     best_value, best_move = self.minimax(self.maxDepth, currBoardIdx, True)
#                 else :
#                     best_value, best_move = self.alphabeta(self.maxDepth,currBoardIdx,alpha,beta,True) ## not implemented yet
#
#             else :
#                 print("waiting for human move")
#                 valid = False
#                 x = 0
#                 y = 0
#                 while not valid:
#
#                     x = int(input("enter the row you want to put: "))
#                     y = int(input("enter the column you want to put: "))
#                     valid = self.checkValid(x,y, currBoardIdx)
#                 best_move = (x,y)
#
#
#
#             print(best_move)
#             nextBoardIdx = (best_move[0] - self.globalIdx[currBoardIdx][0])* 3 + best_move[1] - self.globalIdx[currBoardIdx][1]
#             currBoardIdx = nextBoardIdx
#
#             self.makeMove(best_move, turn)
#             self.printGameBoard()
#             bestMove.append(best_move)
#             gameBoards.append(self.board.copy())
#             time.sleep(1)
#             turn = -turn
#
#
#         winner = self.checkWinner()
#         self.printGameBoard()
#         return gameBoards, bestMove, winner
#
