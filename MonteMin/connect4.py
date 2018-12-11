# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Connect 4 Module
# February 27, 2012

import random
import os
import time
import copy
from minimax import Minimax
from controller import GetMoveM, SetMoveMi, GetMoveMi, SetMoveM
from mcts import Node, MCTS, Board


class Game(object):
    """ Game object that holds state of Connect 4 board and game values
    """
    
    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = u"Connecter Quatre\u2122" # U+2122 is "tm" this is a joke
    colors = ["x", "o"]
    
    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None
        
        # do cross-platform clear screen
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        print(u"Welcome to {0}!".format(self.game_name))
        name = "MinimaxBot"
        diff = 3 # @TODO: Probably means Depth for Minimax
        self.players[0] = AIPlayer(name, self.colors[0], 4,3)
        print("{0} will be {1}".format(self.players[0].name, self.colors[0]))

        # self.players[1] = AIPlayer("B", self.colors[1], 4,3)
        # name = 'MCTSBot' # @TODO: Change this line and next depending on who player2 is
        self.players[1] = MCTSPlayer(name, self.colors[1])

        print("{0} will be {1}".format(self.players[1].name, self.colors[1]))
        
    # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]
        
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')
    
    def newGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.finished = False
        self.winner = None
        
        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]
        
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        # there are only 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > 42:
            self.finished = True
            # this would be a stalemate :(
            return
        
        # move is the column that player want's to play
        move = player.move(self.board)

        for i in range(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return

        # if we get here, then the column is full
        print("Invalid move (column is full)")
        return
    
    def checkForFours(self):
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return
        
    def verticalCheck(self, row, col):
        #print("checking vert")
        fourInARow = False
        consecutiveCount = 0
    
        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
    
        return fourInARow
    
    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
        
        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow
    
    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope
    
    def findFours(self):
        """ Finds start i,j of four-in-a-row
            Calls highlightFours
        """
    
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)
    
    def highlightFour(self, row, col, direction, slope=None):
        """ This function enunciates four-in-a-rows by capitalizing
            the character for those pieces on the board
        """
        
        if direction == 'vertical':
            for i in range(4):
                self.board[row+i][col] = self.board[row+i][col].upper()
        
        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col+i] = self.board[row][col+i].upper()
        
        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row+i][col+i] = self.board[row+i][col+i].upper()
        
            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row-i][col+i] = self.board[row-i][col+i].upper()
        
        else:
            print("Error - Cannot enunciate four-of-a-kind")
    
    def printState(self):
        # cross-platform clear screen
        # os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        print(u"{0}!".format(self.game_name))
        print("Round: " + str(self.round))

        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")
                
def FindColumn(b1,b2):
	for x in range(0,6):
		for y in range(0,7):
			if(b1[x][y] != b2[x][y]):
				return y

class MCTSPlayer(object):
    type = None 
    name = None
    color = None
    def __init__(self, name, color, maxMinutes=1):
        self.maxMinutes = maxMinutes
        self.type = "MCTS"
        self.name = name
        self.color = color
        self.factor = 2.0
        self.board = Board([[0 for _ in range(7)] for _ in range(6)])

    def findBestMove(self):
    	# Returns the best move using MonteCarlo Tree Search
        o = Node(self.board)
        b1 = (self.board.board)
        ## BEST Move Param
        bestMove = MCTS(self.maxMinutes, o, self.factor)
        b = copy.deepcopy(bestMove.state)
        b2 = (b.board)
        col = FindColumn(b1, b2)
        print("MonteCarloColumn: " + str(col))
        print(b2)
        SetMoveM(col)
        return col

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        col = GetMoveMi()
        row = self.board.tryMove(col)
        if row == -1:
            raise EnvironmentError("FU")            
        return self.findBestMove()


class AIPlayer():
    """ AIPlayer object that extends Player
        The AI algorithm is minimax, the difficulty parameter is the depth to which 
        the search tree is expanded.
    """
    
    difficulty = None
    def __init__(self, name, color, difficulty=5,heuristic = 1):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        self.heuristic = heuristic
        
    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        
        m = Minimax(state)
        best_move, _ = m.bestMove(self.difficulty, state, self.color,self.heuristic)
        SetMoveMi(best_move)
        print(self.name + ": " + str(best_move))

        return best_move




