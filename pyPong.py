from tkinter import *
from tkinter import ttk
from random import randint

player1Score=0
player2Score=0
twoplayer=False
BallSize = 20
BallSpeed = 30
blockSize=60
MoveSpeed = 60
centersize=80
width = height=750

class Ball():
    def __init__(self, Window, width, blockSize,Size, MoveSpeed,Block,Block2):
        self.window = Window
        self.Size = Size
        self.MoveSpeed = MoveSpeed
        self.width=width
        self.Block=Block
        self.Block2=Block2
        self.GameOver=False
        self.Moving=False
        self.threads=[]
        self.deltax=0
        self.x0 = width*0.5-(Size)
        self.x1 = width*0.5+(Size)
        self.y0 = (width -(blockSize)/4) - (Size)*2 - Size
        self.y1 = (width -(blockSize)/4) -Size

        self.Ball = Window.create_oval(self.x0,self.y0,self.x1,self.y1, fill="green")

    def firstAngle(self):
        self.deltax = randint(-8,8)
        self.deltay = 8
        self.GameOver=False
        if not self.Moving:
            self.Moving=True
            self.Move()
            self.Move()

    def Move(self):
        if not self.GameOver:
            self.window.move(self.Ball, -self.deltax, -self.deltay)
            self.checkCollision()
            self.window.after(self.MoveSpeed, self.Move)

    def checkCollision(self):
        positions= self.window.coords(self.Ball)
        if positions[0] <=0:
            self.deltax=-self.deltax
            #print("L")
        elif positions[2] >= self.width:
            self.deltax=-self.deltax
            #print("R")
        elif positions[1] <=0:
            #print("U")
            global player1Score
            player1Score+=1
            self.DoGameOver()
        elif positions[3] >=self.width:
            #print("D")
            self.DoGameOver()
            global player2Score
            player2Score+=1
        else:
            blockPos= self.window.coords(self.Block.Character)
            if positions[3] >= blockPos[1] and positions[0]+self.Size/2 >= blockPos[0] and positions[0]+self.Size/2 <=blockPos[2] and self.deltay<0:
                self.deltay=-self.deltay
                self.deltax = randint(-8,8)
                #print("one")
            blockPos= self.window.coords(self.Block2.Character)
            if positions[1] <= blockPos[3] and positions[0]+self.Size/2 >= blockPos[0] and positions[0]+self.Size/2 <=blockPos[2] and self.deltay>0:
                self.deltay=-self.deltay
                self.deltax = randint(-8,8)
                #print("two")

    def resetBall(self):
        self.GameOver=True
        self.window.delete(self.Ball)
        self.Ball = self.window.create_oval(self.x0,self.y0,self.x1,self.y1, fill="green")

    def DoGameOver(self):
        doGameOver(self.window,self,self.Block,self.width)


class Character():
    def __init__(self, Window, width, height, blockSize,MoveSpeed,BallSize):
        self.window = Window

        self.width=width
        self.MoveSpeed = MoveSpeed

        self.x0 = width*0.5-(blockSize)
        self.x1 = width*0.5+(blockSize)

        self.y0 = height -(blockSize)/4 -BallSize
        self.y1 = height-1 -BallSize

        self.Character = Window.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill="black")

    def Left(self,x,y):
        positions = []
        positions= self.window.coords(self.Character)
        if positions[0] + x< 0:
            self.window.move(self.Character, -positions[0], y)
        else:
            self.window.move(self.Character, x, y)

    def Right(self,x,y):
        positions = []
        positions= self.window.coords(self.Character)
        if positions[2] + x> self.width:
            self.window.move(self.Character, self.width-positions[2], y)
        else:
            self.window.move(self.Character, x, y)

    def resetCharacter(self):
        self.Character = self.window.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill="black")

class Character2():
    def __init__(self, Window, width, height, blockSize,MoveSpeed,BallSize):
        self.window = Window
        self.Ball=None
        self.BallSize=BallSize
        self.width=width
        self.MoveSpeed = 30

        self.x0 = width*0.5-(blockSize)
        self.x1 = width*0.5+(blockSize)

        self.y0 = BallSize-1
        self.y1 = BallSize+(blockSize)/4

        self.Character = Window.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill="black")

    def Move(self):
        if not twoplayer:
            positions= self.window.coords(self.Ball.Ball)
            blockPos= self.window.coords(self.Character)
            if self.Ball.deltay>0:
                if blockPos[0]>=positions[2]-self.BallSize:
                    self.Left(-self.MoveSpeed,0)

                elif blockPos[2]<=positions[2]-self.BallSize:
                    self.Right(self.MoveSpeed,0)
            self.window.after(40, self.Move)

    def Left(self,x,y):
        positions = []
        positions= self.window.coords(self.Character)
        if positions[0] + x< 0:
            self.window.move(self.Character, -positions[0], y)
        else:
            self.window.move(self.Character, x, y)

    def Right(self,x,y):
        positions = []
        positions= self.window.coords(self.Character)
        if positions[2] + x> self.width:
            self.window.move(self.Character, self.width-positions[2], y)
        else:
            self.window.move(self.Character, x, y)

    def resetCharacter(self):
        self.Character = self.window.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill="black")

def doGameOver(window,ball,player,width):
    ball.GameOver=True
    ball.Moving=False
    GameOverMenu = window.create_text(width/2 - 50,width/2 -20,anchor="nw")
    window.itemconfig(GameOverMenu, text="GAME OVER")
    startmenu = window.create_text(width/2 - 50,width/2,anchor="nw")
    window.itemconfig(startmenu, text="Press Enter to start...\nPress 'p' for two player")

def setBoard(board,width):
    board.delete("all")
    height=width
    blockSize=60
    MoveSpeed = 68
    centersize=80

    block2 = Character2(board, width, height, blockSize, MoveSpeed, BallSize)
    block = Character(board, width, height, blockSize, MoveSpeed, BallSize)
    ball = Ball(board,width,blockSize,BallSize,BallSpeed,block,block2)
    block2.Ball = ball
    board.create_line(0,height/2,width,height/2)
    board.create_oval(width/2-centersize,width/2-centersize,width/2+centersize,width/2+centersize)

    fontsize=15
    board.create_text(20,width/2 -fontsize*2,anchor="nw",text="0",font=("Purisa", fontsize))
    board.create_text(20,width/2 +fontsize,anchor="nw",text="0",font=("Purisa", fontsize))
    return block, ball, block2

if __name__ == "__main__":
    master = Tk()
    master.title("Game")
    master.resizable(False,False)

    window = Canvas(master, width=width, height=height)
    window.pack()

    block, ball, block2= setBoard(window,width)
    startmenu = window.create_text(width/2 - 50,height/2,anchor="nw")
    window.itemconfig(startmenu, text="Press Enter to start...\nPress 'p' for two player")

    def Left(key):
        block.Left(-MoveSpeed,0)
    def Right(key):
        block.Right(MoveSpeed,0)
    def Left2(key):
        block2.Left(-MoveSpeed,0)
    def Right2(key):
        block2.Right(MoveSpeed,0)
    def Start(key):
        global twoplayer
        twoplayer=False
        master.bind_all("<Left>", Left)
        master.bind_all("<Right>", Right)
        window.delete("all")
        window.create_line(0,height/2,width,height/2)
        window.create_oval(width/2-centersize,width/2-centersize,width/2+centersize,width/2+centersize)
        fontsize=15
        window.create_text(20,width/2 -fontsize*2,anchor="nw",text=str(player2Score),font=("Purisa", fontsize))
        window.create_text(20,width/2 +fontsize,anchor="nw",text=str(player1Score),font=("Purisa", fontsize))
        block2.resetCharacter()
        block.resetCharacter()
        ball.resetBall()
        ball.firstAngle()
        block2.Move()
    def TwoPlayer(key):
        global twoplayer
        twoplayer=True
        master.bind_all("<Left>", Left)
        master.bind_all("<Right>", Right)
        a= master.bind_all("<a>",Left2)
        b=master.bind_all("<d>",Right2)
        window.delete("all")
        window.create_line(0,height/2,width,height/2)
        window.create_oval(width/2-centersize,width/2-centersize,width/2+centersize,width/2+centersize)
        fontsize=15
        window.create_text(20,width/2 -fontsize*2,anchor="nw",text=str(player2Score),font=("Purisa", fontsize))
        window.create_text(20,width/2 +fontsize,anchor="nw",text=str(player1Score),font=("Purisa", fontsize))
        block2.resetCharacter()
        block.resetCharacter()
        ball.resetBall()
        ball.firstAngle()

    master.bind_all("<Return>", Start)
    master.bind_all("<p>", TwoPlayer)
    master.mainloop()
