'''
Created on Mar 16, 2019

@author: dr.aarij
'''


from com.ai.adversarial.sample.pacman.pacmanGame import PacmanGame


class Minimax(object):
    '''
    classdocs
    '''


    def __init__(self, game, listeners = []):
        '''
        Constructor
        '''
        self._game = game
        self.listeners = listeners
        self._initialState = self._game.getInitialState()        
        self._expandedNodes = 0
        self._duplicateStates = {}
        
    def play(self):
        value = self.minimax_decision(self._initialState) 
        return value
    
    def minimax_decision(self,state, callfunc, comparator = lambda a,b: a< b, resultValue = -1000000000000):
        
        self._duplicateStates[str(state)] = state
        resultAction = None
        returnState = None
        player = self._game.getPlayer(state)
        actions = self._game.getActions(state)
        for action in actions:
            resultingState = self._game.getResult(state,action)
            value = callfunc(resultingState,player)
            if comparator(value, resultValue):
                resultValue = value
                resultAction = action
                returnState = resultingState
        return resultAction,resultValue,returnState
    
    def minvalue(self,state,player):
        ss = str(state)
        if ss in self._duplicateStates and self._duplicateStates[ss]._utility > state._utility:
            return state._utility
        else:
            self._duplicateStates[str(state)] = state
        self._expandedNodes += 1
        if self._game.terminalTest(state):
            return state._utility
        retValue = 1000000000000
        fun = None
        if state._move < len(state._ghosts):
            fun = self.minvalue
        else:
            fun = self.maxvalue
        for action in self._game.getActions(state):
            retValue = min(retValue, fun(self._game.getResult(state,action), player))        
        return retValue
            
    def maxvalue(self,state,player):
        ss = str(state)
        if ss in self._duplicateStates and self._duplicateStates[ss]._utility > state._utility:
            return state._utility
        else:
            self._duplicateStates[str(state)] = state
        self._expandedNodes += 1
        if self._game.terminalTest(state):
            return state._utility
        retValue = -1000000000000
        
        for action in self._game.getActions(state):
            if len(state._ghosts) > 0:
                retValue = max(retValue, self.minvalue(self._game.getResult(state,action), player))
            else:
                retValue = max(retValue, self.maxvalue(self._game.getResult(state,action), player))
        
        return retValue
    
if __name__ == "__main__":
    game = PacmanGame("..\\..\\..\\..\\layout\\boxSearch.lay")
    minimax = Minimax(game)
    print(minimax.minimax_decision(game.getInitialState(),  minimax.minvalue, lambda a,b: a > b))
