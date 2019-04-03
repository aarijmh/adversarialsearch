'''
Created on Apr 3, 2019

@author: dr.aarij
'''


class AdversarialNode(object):
    '''
    classdocs
    '''


    def __init__(self, value, name, isMax, children = []):
        '''
        Constructor
        '''
        self._name = name
        self._utility = value
        self._isMax = isMax
        self._children = children
        self._move = 1
        
    def isLeaf(self):
        return len(self._children) == 0

    def isMax(self):
        return self._isMax

    def addChild(self,child):
        self._children.append(child);
        
    def __str__(self):
        s = "Name is %s, value is %d" %(self._name,self._utility)
        s += "\n children are "
        for ch in range(len(self._children)):
            s+= str(self._children[ch])
        return s
        