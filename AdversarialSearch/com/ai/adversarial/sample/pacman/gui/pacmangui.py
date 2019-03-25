'''
Created on Mar 21, 2019

@author: dr.aarij
'''
import threading
import time
from tkinter import Frame, Canvas, Tk, Label, Button

from com.ai.adversarial.sample.pacman import constants
from com.ai.adversarial.sample.pacman.constants import WALL, FOOD, POWER, PLAYER, \
    GHOSTS, EMPTY
from com.ai.adversarial.sample.pacman.pacmanGame import PacmanGame
from com.ai.adversarial.search.minimax import Minimax
from com.ai.adversarial.search.minimaxdepthlimited import MinimaxDepthLimited
import sys


class PacmanGUI(Frame):
    def __init__(self, parent, maze,screenHeight=600, screenWidth=800):
        '''size is the size of a square, in pixels'''

        Frame.__init__(self, parent)
        self.maze = maze
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.state = None
        
        self.colorList = ["red","pink","purple","orange","aqua"]
        self.ghostCount = 0

        
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0,
                                width=self.screenWidth, height=self.screenHeight, background="bisque")
        self.canvas.grid(row=0,column=0)
        self.refresh()
        
#         self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
#         self.pack()
        
    def setupagents(self,state):
        print(state)
    
    def createAgent(self,blockType,x1,y1,x2,y2):
        if blockType == WALL:
            self.createWallBlock(x1, y1, x2, y2)
        else:
            self.createEmptyBlock(x1, y1, x2, y2)            
    
    def createWallBlock(self,x1,y1,x2,y2):
        self.createEmptyBlock(x1,y1,x2,y2,"wall","blue")
            
    def createFoodBlock(self,x1,y1,x2,y2):
#         self.createEmptyBlock(x1,y1,x2,y2,"food")
        offset = int((x2-x1)*0.3)
        self.canvas.create_oval(x1+offset, y1+offset, x2-offset, y2-offset, outline="black", fill="white", tags="food")
                
    def createPowerBlock(self,x1,y1,x2,y2): 
        self.createEmptyBlock(x1,y1,x2,y2,"power")
        offset = int((x2-x1)*0.1)
        self.canvas.create_oval(x1+offset, y1+offset, x2-offset, y2-offset, outline="black", fill="white", tags="power")
        
    def createPacmanBlock(self,x1,y1,x2,y2): 
#         self.createEmptyBlock(x1,y1,x2,y2,"player")
        offset = int((y2-y1)*0.2)
        self.canvas.create_oval(x1+offset, y1+offset, x2-offset, y2-offset, outline="yellow", fill="yellow", tags="player")
                
    def createGhostBlock(self,x1,y1,x2,y2):
#         self.createEmptyBlock(x1,y1,x2,y2,"ghost")
        offset = int((x2-x1)*0.3)
        color = self.colorList[self.ghostCount % len(self.colorList)]
        self.ghostCount += 1
        self.canvas.create_rectangle(x1+offset, y1+offset, x2-offset, y2-offset, outline=color, fill=color, tags="ghost")
        
    def createEmptyBlock(self,x1,y1,x2,y2,tag="empty",color="black"):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="empty")
        
    def refresh(self):
#         self.canvas.delete("wall")
        self.canvas.delete("food")
        self.canvas.delete("power")
        self.canvas.delete("player")
        self.canvas.delete("ghost")
#         self.canvas.delete("empty")
        self.ghostCount = 0
        
        self.rows = len(self.maze)
        self.columns = len(self.maze[0])
        
        self.boxwidth = int(self.screenWidth / self.columns)
        self.boxheight = int(self.screenHeight / self.rows)
        
#         self.canvas.create_rectangle(0, 0, 100, 160, outline="yellow", fill="black", tags="empty")
#         self.canvas.create_rectangle(100, 0, 200, 160, outline="yellow", fill="black", tags="empty")
#         self.canvas.create_rectangle(0, 320, 160, 480, outline="yellow", fill="black", tags="empty")
        
        
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.boxwidth)
                y1 = (row * self.boxheight)
                x2 = x1 + self.boxwidth
                y2 = y1 + self.boxheight
                self.createAgent(self.maze[row][col],x1, y1, x2, y2)
        
        
        self.canvas.tag_raise("wall")
        self.canvas.tag_raise("food")
        self.canvas.tag_raise("power")
        self.canvas.tag_raise("player")
        self.canvas.tag_raise("ghost")
        self.canvas.tag_lower("empty")
    
    def drawState(self,state):
        self.ghostCount = 0
        self.canvas.delete("food")
        self.canvas.delete("power")
        self.canvas.delete("player")
        self.canvas.delete("ghost")
        
        
        x1 = (state._player._y * self.boxwidth)
        y1 = (state._player._x * self.boxheight)
        x2 = x1 + self.boxwidth
        y2 = y1 + self.boxheight
        self.createPacmanBlock(x1, y1, x2, y2)
        
        for gh in state._ghosts:
            x1 = (gh._y * self.boxwidth)
            y1 = (gh._x * self.boxheight)
            x2 = x1 + self.boxwidth
            y2 = y1 + self.boxheight
            self.createGhostBlock(x1, y1, x2, y2)
            
        for _,food in state._dots.items():
            x1 = (food[1] * self.boxwidth)
            y1 = (food[0] * self.boxheight)
            x2 = x1 + self.boxwidth
            y2 = y1 + self.boxheight
            self.createFoodBlock(x1, y1, x2, y2)
            
        self.canvas.tag_raise("wall")
        self.canvas.tag_raise("food")
        self.canvas.tag_raise("power")
        self.canvas.tag_raise("player")
        self.canvas.tag_raise("ghost")
        self.canvas.tag_lower("empty")
            
class GuiHandler(object):
    '''
    classdocs
    '''


    def __init__(self,file):
        self.root = Tk()
        self.game = PacmanGame(file)
        sys.setrecursionlimit(10000) 
        self.minimax = Minimax(self.game)
#         self.minimax = MinimaxDepthLimited(self.game,10)
        self.initializeGui()
        

    def initializeGui(self):
        self.board = PacmanGUI(self.root,self.game._maze)
        self.state = self.game.getInitialState()
        self.board.drawState(self.state)
        self.board.grid(row=0,column = 0)
        self.btn = Button(self.root, text="Click me")
        self.btn.grid(row=0,column = 1)
    
        self.btn.bind('<Button-1>',self.nextHandler)
    
    
        self.lb = Label(self.root,text="Algorithms", font=("Helvetica", 16))
        self.lb.grid(row=1, column=0,sticky="w")
    
        self.root.mainloop()
    
    def nextHandler(self,_):
        threading.Thread(name='c1', target=self.runAlgos, ).start()

            
            
    def runAlgos(self):
        while self.state._move != -1:
            fun = None
            lmb = None
            retValue = 0
            if self.state._move == 0:
                fun = self.minimax.minvalue
                lmb = lambda a,b: a >= b
                retValue = -1000000000000
            else:
                fun = self.minimax.maxvalue
                lmb = lambda a,b: a <= b
                retValue = 1000000000000
            _, valu, st = self.minimax.minimax_decision(self.state,  fun, lmb,retValue)
            self.state = st
            self.state._utility = 0
            self.board.drawState(self.state)
            self.lb['text'] = str(valu)
            time.sleep(.1)
    

if __name__ == "__main__":
    GuiHandler("..\\..\\..\\..\\..\\..\\layout\\custom2.lay")
        