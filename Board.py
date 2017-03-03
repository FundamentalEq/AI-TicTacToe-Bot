from Block import *
from Cell4State import *
class Board() :
    def __init__(self) :

        self.Empty = '-'
        self.Me = 'x'
        self.Enemy = 'o'
        self.MeNu = 0
        self.EnemyNu = 1

        # 4x4 blocks on the board
        self.Blocks = [ Block.Block() for block in range(16) ]

        self.Normalize = 10000
        self.Rows = [ 0  for row in range(4) ]
        self.Cols = [ 0  for col in range(4) ]
        self.Diags = [ 0 for diag in range(4) ]
        self.Index = [ (blockno//4,blockno%4) for block in range(16) ]

        self.RowS = [ [0,0,0] for row in range(4) ]
        self.ColS = [ [0,0,0] for col in range(4) ]
        self.DiagS = [ [0,0,0] for diag in range(4) ]
        self.WinNu = 0
        self.LoseNu = 1
        self.DrawNu = 2
        self.Weights = [ 5 , 3 , 3 , 5 , 3 , 7  , 7 , 3 , 3 , 7 , 7 , 3 , 5 , 3 , 3 , 5 ]

        for block in range(16) :
            self.Rows[self.Index[block][0]] += self.Blocks[block].BlockUtility
            self.Cols[self.Index[block][1]] += self.Blocks[block].BlockUtility
            if self.Index[block][0] == self.Index[block][1] :
                self.Diags[0] += self.Blocks[block].BlockUtility
            if self.Index[block][0] + self.Index[block][1] == 3 :
                self.Diags[1] +=  self.Blocks[block].BlockUtility

        for row in range(4) :

        # Current BoardUtility
        self.BoardUtility = 0

        # WasteMove / NoMove
        self.WasteMove = (-1,-1)

        # Board status
        self.GameStatus = 0

    def UpdateEnemyMove(self,EnemyMove) :
        if EnemyMove == self.WasteMove :
            return -1

        BlockNo = (EnemyMove[0]//4) * 4 + (EnemyMove[1]//4)
        BlockRow = EnemyMove[0] % 4
        BlockCol = EnemyMove[1] % 4

        self.Blocks[BlockNo].UpdateForward((BlockRow,BlockCol),self.EnemyNu)
        self.MakeMove(BlockNo,(BlockRow,BlockCol),self.EnemyNu)

        return 4*BlockRow + BlockCol

    def move(self, board, old_move, flag):
        BlockNo = self.UpdateEnemyMove(old_move)
        return self.Move(BlockNo)

    def Move(self,BlockNo) :
        # Free Move
        if self.CurBlock == -1 :
            pass

        # We know the block where we are supposed to move

    def CheckGameOver(self) :
        Draws = 0
        for row in range(4) :
            if self.RowS[row][self.WinNu] == 4 or self.RowS[row][self.LoseNu] == 4 :
                return True
            Draws += self.RowS[row][self.DrawNu]
        for col in range(4) :
            if self.ColS[col][self.WinNu] == 4 or self.Cols[col][self.LoseNu] == 4 :
                return True
            Draws +=  self.RowS[self.DrawNu]
        for diag in range(2) :
            if self.DiagS[diag][self.WinNu] == 4 or self.DiagS[diag][self.LoseNu] == 4 :
                return True
            Draws += self.DiagS[diag][self.DrawNu]
        if Draws == 16 :
            return True
        return False

    def FindBoardUtility(self) :
        ans = 0
        # Board Based Utility
        for row in range(4) :
            if (self.RowS[row][self.WinNu] == 0 or self.RowS[row][self.LoseNu] == 0 ) and self.RowS[row][self.DrawNu] == 0 :
                ans += self.NUtility(self.Rows[row])
        for col in range(4) :
            if (self.ColS[col][self.WinNu] == 0 or self.Cols[col][self.LoseNu] == 0 ) and self.ColS[col][self.DrawNu] == 0 :
                ans += self.NUtility(self.Cols[col])

        for diag in range(2) :
            if (self.DiagS[diag][self.WinNu] == 0 or self.DiagS[diag][self.LoseNu] == 0 ) and self.DiagS[diag][self.DrawNu] == 0:
                ans += self.NUtility(self.Diags[diag])

        ans2 = 0
        # WeightedSUm
        for block in range(16) :
            ans2 += self.Weights[block] * self.Blocks[block].BlockUtility
        ans2 = float(ans2)/float(10)

        return ans + ans2
    def NUtility(self,val) :
        if val > 0 :
            sign = 1
        else :
            sign = -1
        return sign * 10**(float(abs(val))/float(self.Normalize))

    def MakeMove(self,BlockNo,Move,Player) :
        PrevVal = self.Blocks[BlockNo].BlockUtility

        self.Blocks[BlockNo].UpdateForward(Move,Player)

        if self.Blocks[BlockNo].Status == "Won" :
            self.RowS[self.Index[BlockNo][0]][self.WinNu] += 1
            self.ColS[self.Index[BlockNo][1]][self.WinNu] += 1

            if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
                self.DiagS[0][self.WinNu] += 1

            if self.Index[BlockNo][0] + self.Index[BlockNo][1]  == 3:
                self.DiagS[1][self.WinNu] += 1

        elif self.Blocks[BlockNo].Status == "Lost" :
            self.RowS[self.Index[BlockNo][0]][self.LoseNu] += 1
            self.ColS[self.Index[BlockNo][1]][self.LoseNu] += 1

            if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
                self.DiagS[0][self.LoseNu] += 1

            if self.Index[BlockNo][0] + self.Index[BlockNo][1]  == 3:
                self.DiagS[1][self.LoseNu] += 1

        elif self.Blocks[BlockNo].EmptyCells == 0 :
            self.RowS[self.Index[BlockNo][0]][self.DrawNu] += 1
            self.ColS[self.Index[BlockNo][1]][self.DrawNu] += 1

            if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
                self.DiagS[0][self.DrawNu] += 1

            if self.Index[BlockNo][0] + self.Index[BlockNo][1]  == 3:
                self.DiagS[1][self.DrawNu] += 1


        Change = self.Blocks[BlockNo].BlockUtility - PrevVal

        self.Rows[self.Index[BlockNo][0]] += Change
        self.Cols[self.Index[BlockNo][1]] += Change

        # is on Diagonal0
        if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
            self.Diags[0] += Change

        # is on Diagonal1
        if self.Index[BlockNo][0] + self.Index[BlockNo][1] == 3 :
            self.Diags[1] += Change


    def UndoMove(self,BlockNo,Move,Player) :
        PrevVal = self.Blocks[BlockNo].BlockUtility

        if self.Blocks[BlockNo].Status == "Won" :
            self.RowS[self.Index[BlockNo][0]][self.WinNu] -= 1
            self.ColS[self.Index[BlockNo][1]][self.WinNu] -= 1

            if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
                self.DiagS[0][self.WinNu] -= 1

            if self.Index[BlockNo][0] + self.Index[BlockNo][1]  == 3:
                self.DiagS[1][self.WinNu] -= 1

        elif self.Blocks[BlockNo].Status == "Lost" :
            self.RowS[self.Index[BlockNo][0]][self.LoseNu] -= 1
            self.ColS[self.Index[BlockNo][1]][self.LoseNu] -= 1

            if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
                self.DiagS[0][self.LoseNu] -= 1

            if self.Index[BlockNo][0] + self.Index[BlockNo][1]  == 3:
                self.DiagS[1][self.LoseNu] -= 1

        elif self.Blocks[BlockNo].EmptyCells == 0 :
            self.RowS[self.Index[BlockNo][0]][self.DrawNu] -= 1
            self.ColS[self.Index[BlockNo][1]][self.DrawNu] -= 1

            if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
                self.DiagS[0][self.DrawNu] -= 1

            if self.Index[BlockNo][0] + self.Index[BlockNo][1]  == 3:
                self.DiagS[1][self.DrawNu] -= 1


        self.Blocks[BlockNo].UpdateBackward(Move,Player)
        Change = self.Blocks[BlockNo].BlockUtility - PrevVal

        self.Rows[self.Index[BlockNo][0]] += Change
        self.Cols[self.Index[BlockNo][1]] += Change

        # is on Diagonal0
        if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
            self.Diags[0] += Change

        # is on Diagonal1
        if self.Index[BlockNo][0] + self.Index[BlockNo][1] == 3 :
            self.Diags[1] += Change


    def alphabetaRunner(self,depth,alpha,beta,playe,BlockNo) :

    def alphabeta(self,depth,alpha,beta,player,BlockNo) :

        if depth == 0 or self.CheckGameOver() :
            return self.FindBoardUtility()

        # order the moves in the required order
        if self.Blocks[BlockNo].Status == "War" :

            MoveSet = OrderMoves()

            self.MakeMove(BlockNo,MoveSet[0],player)

            # For the thought best move do the complete search
            current = -self.alpabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(BlockNo,MoveSet[0]))
            BestMove = MoveSet[0]

            self.UndoMove(BlockNo,MoveSet[0],player)

            for i in range(1,len(MoveSet)) :
                # Play according to assumption
                self.MakeMove(Blocks,MoveSet[i],player)

                score = -self.alpabeta(depth - 1,-alpha-1,-alpha,player^1,self.FindNextBlock(BlockNo,MoveSet[0]))

                # Case where our assumption fails
                if score > alpha and score < beta :
                    score = -alpabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(BlockNo,MoveSet[0]))

                self.UndoMove(Blocks,MoveSet[i],player)

                if score >= current :
                    current = score
                    BestMove = MoveSet[i]
                    if score > alpha :
                        alpha = score
                    if score > beta :
                        break

            return current

        # We are at a free node
        else :
            MoveSet = OrderBlocks()
            current = self.alpabeta(max(depth-1,2),alpha,beta,player,MoveSet[0])

            for i in range(1,len(MoveSet)) :
                score = self.alpabeta(max(depth-1,2),alpha,alpha+1,player,MoveSet[i])
                if score >= current :
                    current = score
                    if score > alpha :
                        alpha = score
                    if score > beta :
                        break

            return current
