import sys

Me = 'x'
Enemy = 'o'
Empty = '-'
MaxSearchDepth = 5
Waste = (-1,-1)

Inf = 1000000

WinnerVal = 100000
DrawUtility = 100
ColValue = 10
RowValue = 10
DiagValue = 10

class Block() :
    def __init__(self) :
        self.block = [[Empty for j in range(4)] for i in range(4)]

    def Update(self,old_move,Player) :
        self.block[old_move[0]][old_move[1]] = Player

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

    def FindAvailableMoves(self) :
        AvailableMoves = []
        for i in range(4) :
            for j in range(4) :
                if self.block[i][j] == Empty :
                    AvailableMoves.append((i,j))
        return AvailableMoves

    def move(self,old_move) :
        # Update the opponents move on the block
        print "AB Bot got enemy move as ",old_move
        if old_move != Waste :
            self.Update(old_move,Enemy)

        new_move = Waste
        move_utility = 0
        (new_move,move_utility) = self.search(True,0,-Inf,Inf)
        self.Update(new_move,Me)
        return new_move

    def search(self,flag,depth,ParentAlpha,ParentBeta) :
        if depth == MaxSearchDepth :
            utility = self.utility()
            return (Waste,utility)

        ret = self.CheckWinStatus()
        if ret!=0 :
            return (Waste,ret)

        if self.CheckDraw() :
            return (Waste,DrawUtility)

        # get the list of the available Moves
        avail_store = self.FindAvailableMoves()

        # if this is a max node
        if flag :
            NodeBeta = ParentBeta
            NodeAlpha = -Inf
            Player = Me
        # this is a min node
        else :
            NodeBeta = Inf
            NodeAlpha = ParentAlpha
            Player = Enemy

        MoveUtility = 0
        ChoosenNode = Waste

        for move in avail_store :
            # do the move
            self.Update(move,Player)
            nextMove,MoveUtility = self.search(flag ^ 1 ,depth + 1 ,NodeAlpha,NodeBeta)

            # undo the move
            self.block[move[0]][move[1]] = Empty

            # if max node update NodeAlpha
            if flag :
                if MoveUtility > NodeAlpha :
                    NodeAlpha = MoveUtility
                    ChoosenNode = move

            # else update beta
            else :
                if NodeBeta > MoveUtility :
                    NodeBeta = MoveUtility
                    ChoosenNode = move

                    if NodeBeta <= NodeAlpha :
                        # this node returns a values  < than already promissed value
                        # no need to search furhter
                        return (Waste,NodeBeta)

        if flag:
            return (ChoosenNode,NodeAlpha)
        else:
            return (ChoosenNode,NodeBeta)



    def utility(self) :
        ans = 0
        for i in range(4) :
            CtMe = self.block[i].count(Me)
            CtEnemy = self.block[i].count(Enemy)
            if CtMe == 0 :
                ans -= RowValue ** CtEnemy
            elif CtEnemy == 0 :
                ans += RowValue ** CtMe

        for j in range(4) :
            col = [self.block[i][j] for i in range(4)]
            CtMe = col.count(Me)
            CtEnemy = col.count(Enemy)
            if CtMe == 0 :
                ans -= ColValue ** CtEnemy
            elif CtEnemy == 0:
                ans += ColValue ** CtMe

        diag = [self.block[i][i] for i in range(4)]
        CtMe = diag.count(Me)
        CtEnemy = diag.count(Enemy)
        if CtMe == 0 :
            ans -= DiagValue ** CtEnemy
        elif CtEnemy == 0 :
            ans += DiagValue ** CtMe

        diag = [self.block[i][3-i] for i in range(4)]
        CtMe = diag.count(Me)
        CtEnemy = diag.count(Enemy)
        if CtMe == 0 :
            ans -= DiagValue ** CtEnemy
        elif CtEnemy == 0 :
            ans += DiagValue ** CtMe

        # print "Bot's version"
        # for i in range(4) :
        #     print self.block[i]
        #
        # print "utility is ", ans
        return ans
