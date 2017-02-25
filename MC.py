import sys
import random

Me = 'x'
Enemy = 'o'
Empty = '-'
Waste = (-1,-1)

Inf = 1000000
WinnerVal = 1
Simulations = 10000

class Block() :
    def __init__(self) :
        self.block = [[Empty for j in range(4)] for i in range(4)]
        self.AvailableMoves = [(i,j) for i in range(4) for j in range(4)]

    def Update(self,old_move,Player) :
        self.block[old_move[0]][old_move[1]] = Player
        self.AvailableMoves.remove(old_move)

    def WinVal(self,flag) :
        if flag == Me :
            return WinnerVal
        else :
            return -10*WinnerVal

    def CheckWinStatus(self) :
        for i in range(4) :
            row = self.block[i]
            col = [self.block[i][j] for j in range(4)]
            if row.count(row[0]) == 4 and row[0]!= Empty :
                return self.WinVal(row[0])
            if col.count(col[0]) == 4 and col[0]!=Empty :
                return self.WinVal(col[0])
        diag = [self.block[i][i] for i in range(4)]
        if diag.count(diag[0]) == 4 and diag[0]!=Empty :
            return self.WinVal(diag[0])
        diag = [self.block[i][3-i] for i in range(4)]
        if diag.count(diag[0]) == 4 and diag[0]!=Empty :
            return self.WinVal(diag[0])

        return 0

    def CheckDraw(self) :
        ans = 0
        for i in range(4) :
            ans += self.block[i].count(Empty)
        if ans == 0 :
            return True
        return False

    def FindAvailableMoves(self) :
        AvailableMoves = []
        for i in range(4) :
            for j in range(4) :
                if self.block[i][j] == Empty :
                    AvailableMoves.append((i,j))
        return AvailableMoves

    def move(self,old_move) :
        # Update the opponents move on the block
        print "MC Bot got enemy move as ",old_move
        if old_move != Waste :
            self.Update(old_move,Enemy)

        new_move = (-1,-1)
        MaxWins = -Inf
        for move in self.AvailableMoves :
            Wins = 0
            self.Update(move,Me)
            for j in range(Simulations) :
                Wins += self.Simulate(False)

            # undo the move
            self.AvailableMoves.append(move)
            self.block[move[0]][move[1]] = Empty

            if Wins > MaxWins :
                new_move = move

        return new_move


    def Simulate(self,Flag) :
        if len(self.AvailableMoves) == 0 :
            return self.CheckWinStatus()

        move = random.choice(self.AvailableMoves)
        if Flag :
            self.Update(move,Me)
            ret = self.Simulate(Flag ^ 1)
        else :
            self.Update(move,Enemy)
            ret = self.Simulate(Flag ^ 1)

        # undo the move
        self.AvailableMoves.append(move)
        self.block[move[0]][move[1]] = Empty
        return ret
