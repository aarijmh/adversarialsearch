'''
Created on Mar 25, 2019

@author: dr.aarij
'''
from com.ai.adversarial.sample.tictactoe.tictactoeState import TictactoeState
from com.ai.adversarial.sample.tictactoe.tictactoePlayer import TictactoePlayer

class TicTacToeGame(object):
    '''
    classdocs
    '''


    def __init__(self, move = 0):
        self._board = [[0,0,0],[0,0,0],[0,0,0]]
        self._move = move
        self._agents =[ TictactoePlayer("Player","X"),
                       TictactoePlayer("Opponent","O")]
        
    def getInitialState(self):
        return TictactoeState(self._board,self._move)
    
    def getPlayer(self,state):
        return self._agents[state._move]
    
    def getActions(self,state):
        actions = []
        
        for i in range(3):
            for j in range(3):
                if state._board[i][j] == 0:
                    actions.append(set(i,j))
                
        
        return actions

        