'''
Created on Mar 16, 2019

@author: dr.aarij
'''
from com.ai.adversarial.elements.game import Game
from com.ai.adversarial.sample.pacman.gameElement import GameElement
from com.ai.adversarial.sample.pacman.constants import WALL_SYMBOL, WALL,\
    EMPTY_SYMBOL, EMPTY, PLAYER_SYMBOL, PLAYER, GHOST_SYMBOL, POWER_SYMBOL,\
    POWER, FOOD_SYMBOL, FOOD, GHOSTS, MOVES, STEP_COST, DOT_UTILITY, LOST_COST,\
    WIN_COST
from com.ai.adversarial.sample.pacman.pacmanState import PacmanState
import copy

class PacmanGame(Game):
    '''
    classdocs
    '''


    def __init__(self, mazefile, enemies=0):
        self._mazeFile = mazefile
        self._player = GameElement("player")
        self._enemies = []
        self._dots = {}
        self._power = {}
        for i in range(enemies):
            self._enemies.append(GameElement("Ghost "+str(i+1)))
        self.buildMazeFromFile()
            
    def getInitialState(self):
        return PacmanState(self._player, self._enemies, self._dots,self._power, 0, 0)
    
    def getPlayer(self,state):
        if state._move == 0:
            return self._player
        else:
            return self._enemies[state._move - 1]         
    
    def getActions(self,state):
        actions = []
        player = None
        if state._move == 0:
            player = state._player
        else:
            player = state._ghosts[state._move-1]
        
        for move in MOVES:
            if self._maze[player._x + move[0]][player._y + move[1]]  != WALL:
                actions.append(move)
        
        if state._move != 0:
            if player._direction == None:
                player._direction = actions[0]
            elif player._direction in actions:
                reverseAction = (player._direction[0]*-1,player._direction[1]*-1)
                if reverseAction in actions and len(actions) > 1:
                    actions.remove(reverseAction)
                actions.remove(player._direction)
                actions.append(player._direction)
            else:player._direction = actions[0]
                        
        return actions
    
    def getResult(self, state, action):
        newState = state.createCopy()
        if newState._move == 0:
            newState._player._x = newState._player._x + action[0]
            newState._player._y = newState._player._y + action[1]
            
            newState._utility = newState._utility + STEP_COST
            
            sst =  str(newState._player._x) +"_"+ str(newState._player._y)
            if sst in newState._dots:
                newState._utility = newState._utility + DOT_UTILITY
                del newState._dots[sst]
                if len(newState._dots) == 0:
                    newState._move = -1
                    newState._utility += WIN_COST
            
            for enemy in  state._ghosts:
                if newState._player._x == enemy._x and  newState._player._y == enemy._y:
                    newState._utility = newState._utility + LOST_COST
                    newState._move = -1
                    break
            if newState._move != -1 and len(newState._ghosts) > 0:
                newState._move += 1
        else:
            newState._ghosts[newState._move-1]._x = newState._ghosts[newState._move-1]._x + action[0]
            newState._ghosts[newState._move-1]._y = newState._ghosts[newState._move-1]._y + action[1]
            
            if newState._ghosts[newState._move-1]._x == newState._player._x and  newState._ghosts[newState._move-1]._y == newState._player._y:
                newState._utility = newState._utility + LOST_COST
                newState._move = -1
            if newState._move != -1:
                newState._move += 1
                newState._move = newState._move % (len(newState._ghosts) + 1)
        
        return newState
        
    
    def terminalTest(self,state):
        return state._move == -1
    
    def utility(self,state,player): 
        return state._utility
    
    def getAgentCount(self):
        return len(self._enemies) + 1
    
    def buildMazeFromFile(self):
        self._maze = []
        file_object  = open(self._mazeFile, 'r')
        row = 0
        ghostCount = 0 
        for line in file_object:
            rowElements = []
            column = 0 
            for c in line.lower():
                if c == WALL_SYMBOL:
                    rowElements.append(WALL)
                elif c == EMPTY_SYMBOL:
                    rowElements.append(EMPTY)
                elif c == PLAYER_SYMBOL:
                    rowElements.append(PLAYER)
                    self._player._x = row
                    self._player._y = column
                elif c == GHOST_SYMBOL:
                    rowElements.append(GHOSTS)
                    self._enemies.append(GameElement("Ghost "+str(ghostCount), row, column))
#                     self._enemies[ghostCount]._x = row
#                     self._enemies[ghostCount]._y = column
                    ghostCount+=1
                elif c == POWER_SYMBOL:
                    self._power[row+"_"+column]=(row,column)
                    rowElements.append(POWER)
                elif c == FOOD_SYMBOL:
                    self._dots[str(row)+"_"+str(column)]=(row,column)
                    rowElements.append(FOOD)
                column +=1
            self._maze.append(rowElements)
            row +=1 
