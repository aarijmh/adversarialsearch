'''
Created on Mar 16, 2019

@author: dr.aarij
'''
from com.ai.adversarial.elements.state import State

class PacmanState(State):
    '''
    classdocs
    '''


    def __init__(self, player, ghosts, dots, power, move=0,utility=0):
        self._player = player
        self._ghosts = ghosts
        self._dots = dots
        self._power = power
        self._move = move
        self._utility = utility
        self._action = None
    
    def createCopy(self):
        gh = []
        for ghsts in self._ghosts:
            gh.append(ghsts.createCopy())
        
        dots = {}
        for k,v in self._dots.items():
            dots[k] = v
            
        power = {}
        for k,v in self._power.items():
            power[k] = v
        
        return PacmanState(self._player.createCopy(),gh,dots,power,self._move,self._utility)
    
    def getTotalAgents(self):
        return len(self._ghosts) + 1 
    
    def isMax(self):   
        return self._move == 0
    
    def isNextAgentMax(self):
        return (self._move + 1) % (len(self._ghosts) + 1) == 0
    
    def getAction(self):
        return self._action
    
    def __str__(self):
        st = ""
        st += str(self._player)
        for gh in self._ghosts:
            st += str(gh)
        st += str(len(self._dots))
        return st