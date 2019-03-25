'''
Created on Mar 25, 2019

@author: dr.aarij
'''
from copy import deepcopy

class TictactoeState(object):
    '''
    classdocs
    '''


    def __init__(self, board,move,utility=0):
        self._board = board
        self._move = move
        self._utility = utility
        
    def copy(self):
        return TictactoeState(deepcopy(self._board),self._move,self._utility)
    
    def __str__(self):
        return str(self._board)+"_"+str(self._move)