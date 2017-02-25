import sys

Me = 'x'
Enemy = 'o'
Empty = '-'
MaxSearchDepth = 5

ALPHA = -1000000
BETA = 1000000

WinnerVal = 10000
class Block() :
    def __init__(self) :
        self.block = [[Empty for j in range(4)] for i in range(4)]
        self.AvailableBlocks = [(i,j) for i in range(4) for j in range(4)]

    def Update(self,old_move) :
        self.block[old_move[0]][old_move[1]] = Enemy
        self.AvailableBlocks.remove((old_move[0],old_move[1]))

    def WinVal(self,flag) :
        if flag == Me :
            return WinnerVal
        else :
            return -WinnerVal

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

    def move(self,old_move) :
        depth = 0
        alpha = ALPHA
        beta = BETA
        new_move = old_move
        move_utility = 0
        (new_move,move_utility) = self.search(old_move,Me,depth,alpha,beta)

    def search(old_move,flag,depth,alpha,beta) :
        if depth == MaxSearchDepth :
            utility = self.utility()
            return (old_move,utility)

        ret = self.CheckWinStatus()
        if ret!=0 :
            return (old_move,ret)

        if self.CheckDraw() :
            return (old_move,0)

        avail_store = self.AvailableBlocks
