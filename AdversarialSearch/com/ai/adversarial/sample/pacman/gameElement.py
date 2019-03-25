'''
Created on Mar 16, 2019

@author: dr.aarij
'''
import copy

class GameElement(object):
    '''
    classdocs
    '''


    def __init__(self, name="", x =0, y=0,condition=0,direction=None):
        '''
        Constructor
        '''
        
        self._elementName = name
        self._x = x
        self._y = y
        self._condition = condition
        self._direction = direction
    
    def createCopy(self):
        return GameElement(self._elementName, self._x,self._y,self._condition,self._direction)
        
    def __str__(self):
        return ("(%s,%s)")%(self._x,self._y)