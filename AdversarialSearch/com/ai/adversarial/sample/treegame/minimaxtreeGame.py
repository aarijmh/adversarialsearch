'''
Created on Apr 3, 2019

@author: dr.aarij
'''
from com.ai.adversarial.elements.game import Game
from com.ai.adversarial.sample.treegame.adversarialNode import AdversarialNode
import sys
from com.ai.adversarial.search.minimax import Minimax


class MinimaxTreeGame(Game):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        
                                    A
                    B                C            D
                E    F    G    H    I    J    K    L    M
                3    12   8    2    4    6    14    5    2
        '''
        
        bottom1 = [AdversarialNode(3,"E",True,[]),
                   AdversarialNode(12,"F",True,[]),
                   AdversarialNode(8,"G",True,[])]
        
        bottom2 = [AdversarialNode(2,"H",True,[]),
                   AdversarialNode(4,"I",True,[]),
                   AdversarialNode(6,"J",True,[])]

        bottom3 = [AdversarialNode(14,"K",True,[]),
                   AdversarialNode(5,"L",True,[]),
                   AdversarialNode(2,"M",True,[])]
        
        b = AdversarialNode(-sys.maxsize - 1,"B",False,bottom1)
        c = AdversarialNode(-sys.maxsize - 1,"C",False,bottom2)
        d = AdversarialNode(-sys.maxsize - 1,"D",False,bottom3)
        
        a = AdversarialNode(-sys.maxsize - 1,"A",True,[b,c,d])
        
        self._root = a
        
    def getInitialState(self):
        return self._root
    
    def getPlayer(self,state):
        return state.isMax()
    
    def getActions(self,state):
        return [x for x  in range(len(state._children))]
         
    def getResult(self, state, action):
        return state._children[action]
     
    def terminalTest(self,state):
        return state.isLeaf()
     
    def utility(self,state,player):
        return state._value
            
    def getAgentCount(self): 
        return 2
    
    
if __name__ == "__main__":
    game = MinimaxTreeGame()    
    minimax = Minimax(game)
    action,value,state=minimax.minimax_decision(game.getInitialState(),  minimax.minvalue, lambda a,b: a > b) 
    print(state)
    