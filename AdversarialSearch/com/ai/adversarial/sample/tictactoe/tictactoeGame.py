'''
Created on Mar 25, 2019

@author: dr.aarij
'''
from com.ai.adversarial.sample.tictactoe import tictactoeState
from com.ai.adversarial.sample.tictactoe.tictactoeState import TictactoeState

class TicTacToeGame(object):
    '''
    classdocs
    '''


    def __init__(self, move = 0):
        self._board = [[0,0,0],[0,0,0],[0,0,0]]
        self._move = move
        
    def getInitialState(self):
        return TictactoeState(self._board,self._move)

        