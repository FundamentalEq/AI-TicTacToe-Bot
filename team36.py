
import time
class Cell4State() :
        def __init__(self) :
            self.Empty = '-'
            self.Me = 'x'
            self.Enemy = 'o'
            self.MeNu = 0
            self.EnemyNu = 1
            self.WinUtility = 10000
            self.NormalizationConstant = 10000
            self.PowersOf10 = [1,10,100,1000,10000]
            self.States = {}
            self.ForwardAd = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            self.BackwardAd = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            self.UtilityChangeForward = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            # self.NormalizedUCF = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            # self.NormalizedUCB = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            self.UtilityChangeBackward = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            self.CurrentActiveStates = 0
            self.CurState = [self.Empty,self.Empty,self.Empty,self.Empty]
            self.StateUtility = [ 0 for state in range(81) ]
            self.AvailableMoves = [ [] for state in range(81) ]
            self.dfs(self.CurrentActiveStates)
            self.WinState = self.States[str([self.Me,self.Me,self.Me,self.Me])]
            self.LoseState = self.States[str([self.Enemy,self.Enemy,self.Enemy,self.Enemy])]

        def dfs(self,StateNo) :
            # Add the state to the list of known states
            self.States[str(self.CurState)] = StateNo
            self.StateUtility[StateNo] = self.FindCurStateUtility()
            self.CurrentActiveStates += 1

            NextStateNo = -1
            for cell in range(4) :
                # check for Empty cell
                if self.CurState[cell] == self.Empty :
                    # Add the cell to list of available moves from the current state
                    self.AvailableMoves[StateNo].append(cell)

                    # if payed by me
                    self.CurState[cell] = self.Me

                    if str(self.CurState) not in self.States :
                        NextStateNo =  self.CurrentActiveStates
                        self.dfs(NextStateNo)
                    else :
                        NextStateNo = self.States[str(self.CurState)]

                    # Add a forward Edge
                    self.ForwardAd[StateNo][cell][self.MeNu] = NextStateNo
                    # Add a Backward Edge
                    self.BackwardAd[NextStateNo][cell][self.MeNu] = StateNo

                    # ForwardUtility Change
                    self.UtilityChangeForward[StateNo][cell][self.MeNu] = self.StateUtility[NextStateNo] - self.StateUtility[StateNo]
                    # Normalized ForwardUtility
                    # self.NormalizedUCF[StateNo][cell][self.MeNu] = 10**(float(self.UtilityChangeForward[StateNo][cell][self.MeNu])/float(self.NormalizationConstant))
                    # BackwardUtility Change
                    self.UtilityChangeBackward[NextStateNo][cell][self.MeNu] = self.StateUtility[StateNo] - self.StateUtility[NextStateNo]
                    # Normalized BackwardUtility
                    # self.NormalizedUCB[NextStateNo][cell][self.MeNu] = 10**(float(self.UtilityChangeBackward[NextStateNo][cell][self.MeNu])/float(self.NormalizationConstant))


                    # if plpayed by Enemy
                    self.CurState[cell] = self.Enemy

                    if str(self.CurState) not in self.States :
                        NextStateNo =  self.CurrentActiveStates
                        self.dfs(NextStateNo)
                    else :
                        NextStateNo = self.States[str(self.CurState)]

                    # Add a forward Edge
                    self.ForwardAd[StateNo][cell][self.EnemyNu] = NextStateNo
                    # Add a Backward Edge
                    self.BackwardAd[NextStateNo][cell][self.EnemyNu] = StateNo

                    # ForwardUtility Change
                    self.UtilityChangeForward[StateNo][cell][self.EnemyNu] = self.StateUtility[NextStateNo] - self.StateUtility[StateNo]
                    # Normalized ForwardUtility
                    # self.NormalizedUCF[StateNo][cell][self.EnemyNu] = 10**(float(self.UtilityChangeForward[StateNo][cell][self.EnemyNu])/float(self.NormalizationConstant))
                    # BackwardUtility Change
                    self.UtilityChangeBackward[NextStateNo][cell][self.EnemyNu] = self.StateUtility[StateNo] - self.StateUtility[NextStateNo]
                    # Normalized BackwardUtility
                    # self.NormalizedUCB[NextStateNo][cell][self.EnemyNu] = 10**(float(self.UtilityChangeBackward[NextStateNo][cell][self.EnemyNu])/float(self.NormalizationConstant))

                    # Restore the cell
                    self.CurState[cell] = self.Empty

        def FindCurStateUtility(self) :
            MeCount =  self.CurState.count(self.Me)
            EnemyCount =  self.CurState.count(self.Enemy)
            if MeCount == 0 and EnemyCount == 0 :
                return 0
            if MeCount == 0 :
                return -self.PowersOf10[EnemyCount]
            if EnemyCount == 0 :
                return self.PowersOf10[MeCount]
            return 0

LineState = Cell4State()
class Block() :
    def __init__(self) :
        # Initially all are in State 0
        self.Rows = [ 0 for row in range(4)]
        self.Cols = [ 0 for col in range(4)]
        self.Diags = [ 0 for diag in range(2)]
        self.History = [ [0  for col in range(4)] for row in range(4) ]
        # No of Empty Cells
        self.EmptyCells = 16

        # Current Utility of the Block
        self.BlockUtility = 10*LineState.StateUtility[0]

        self.Status = "War"

  # [ Current State][ Cell No ][ Player No]
    def UpdateForward(self,Move,Player) :
        # Update Row State
        self.BlockUtility += LineState.UtilityChangeForward[ self.Rows[Move[0]] ][ Move[1] ][ Player ]
        self.Rows[Move[0]] = LineState.ForwardAd[ self.Rows[Move[0]] ][ Move[1] ][ Player ]

        # Update Col State
        self.BlockUtility += LineState.UtilityChangeForward[ self.Cols[Move[1]] ][ Move[0] ][ Player ]
        self.Cols[Move[1]] = LineState.ForwardAd[ self.Cols[Move[1]] ][ Move[0] ][ Player ]

        # check for Block Status
        if self.Rows[Move[0]] == LineState.WinState or self.Cols[Move[1]] == LineState.WinState :
            self.Status = "Won"
        elif self.Rows[Move[0]] == LineState.LoseState or self.Cols[Move[1]] == LineState.LoseState :
            self.Status = "Lost"

        # if this lies on diagonal 0
        if Move[0] == Move[1] :
            self.BlockUtility += LineState.UtilityChangeForward[ self.Diags[0] ][ Move[0] ][ Player ]
            self.Diags[0] = LineState.ForwardAd[ self.Diags[0] ][ Move[0] ][ Player ]
            if self.Diags[0] == LineState.WinState :
                self.Status = "Won"
            elif self.Diags[0] == LineState.LoseState:
                self.Status = "Lost"

        # if this lies on diagonal 1
        if Move[0] + Move[1] == 3 :
            self.BlockUtility += LineState.UtilityChangeForward[ self.Diags[1] ][ Move[0] ][ Player ]
            self.Diags[1] = LineState.ForwardAd[ self.Diags[1] ][ Move[0] ][ Player ]
            if self.Diags[1] == LineState.WinState :
                self.Status = "Won"
            elif self.Diags[1] == LineState.LoseState:
                self.Status = "Lost"

        # Decrement the number of Empty cells
        self.EmptyCells -= 1

    def UpdateBackward(self,Move,Player) :
        # Update Block Stats if relevent
        if self.Rows[Move[0]] == LineState.WinState or self.Cols[Move[1]] == LineState.WinState :
            self.Status = "War"
        elif self.Rows[Move[0]] == LineState.LoseState or self.Cols[Move[1]] == LineState.LoseState :
            self.Status = "War"

        # Update Row State
        self.BlockUtility += LineState.UtilityChangeBackward[ self.Rows[Move[0]] ][ Move[1] ][ Player ]
        self.Rows[Move[0]] = LineState.BackwardAd[ self.Rows[Move[0]] ][ Move[1] ][ Player ]

        # Update Col State
        self.BlockUtility += LineState.UtilityChangeBackward[ self.Cols[Move[1]] ][ Move[0] ][ Player ]
        self.Cols[Move[1]] = LineState.BackwardAd[ self.Cols[Move[1]] ][ Move[0] ][ Player ]

        # if this lies on diagonal 0
        if Move[0] == Move[1] :
            if self.Diags[0] == LineState.WinState :
                self.Status = "War"
            elif self.Diags[0] == LineState.LoseState:
                self.Status = "War"

            self.BlockUtility += LineState.UtilityChangeBackward[ self.Diags[0] ][ Move[0] ][ Player ]
            self.Diags[0] = LineState.BackwardAd[ self.Diags[0] ][ Move[0] ][ Player ]

        # if this lies on diagonal 1
        if Move[0] + Move[1] == 3 :
            if self.Diags[1] == LineState.WinState :
                self.Status = "War"
            elif self.Diags[1] == LineState.LoseState:
                self.Status = "War"

            self.BlockUtility += LineState.UtilityChangeBackward[ self.Diags[1] ][ Move[0] ][ Player ]
            self.Diags[1] = LineState.BackwardAd[ self.Diags[1] ][ Move[0] ][ Player ]

        # Decrement the number of Empty cells
        self.EmptyCells += 1

class Player36() :
    def __init__(self) :
        # print "Board formed"
        self.Empty = '-'
        self.Me = 'x'
        self.Enemy = 'o'
        self.MeNu = 0
        self.EnemyNu = 1

        # 4x4 blocks on the board
        self.Blocks = [ Block() for block in range(16) ]

        self.Normalize = 10000
        self.Rows = [ 0  for row in range(4) ]
        self.Cols = [ 0  for col in range(4) ]
        self.Diags = [ 0 for diag in range(4) ]
        self.Index = [ (blockno//4,blockno%4) for blockno in range(16) ]

        self.RowS = [ [0,0,0] for row in range(4) ]
        self.ColS = [ [0,0,0] for col in range(4) ]
        self.DiagS = [ [0,0,0] for diag in range(4) ]
        self.WinNu = 0
        self.LoseNu = 1
        self.DrawNu = 2
        self.Weights = [ 5 , 3 , 3 , 5 , 3 , 7  , 7 , 3 , 3 , 7 , 7 , 3 , 5 , 3 , 3 , 5 ]
        self.BlockWeight = 0.5
        self.Maxdepth = 5
        for block in range(16) :
            self.Rows[self.Index[block][0]] += self.Blocks[block].BlockUtility
            self.Cols[self.Index[block][1]] += self.Blocks[block].BlockUtility
            if self.Index[block][0] == self.Index[block][1] :
                self.Diags[0] += self.Blocks[block].BlockUtility
            if self.Index[block][0] + self.Index[block][1] == 3 :
                self.Diags[1] +=  self.Blocks[block].BlockUtility
        self.PowersOf2 = [2**i for i in range(30)]
        self.ExtensionGiven = False

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

        # self.Blocks[BlockNo].UpdateForward((BlockRow,BlockCol),self.EnemyNu)
        self.MakeMove(BlockNo,(BlockRow,BlockCol),self.EnemyNu)

        return 4*BlockRow + BlockCol

    def move(self, board, old_move, flag):
        start = time.time()
        # print "my bot called with" , old_move
        BlockNo = self.UpdateEnemyMove(old_move)
        # print "Block no" ,BlockNo
        move,val = self.alphabetaRunner(self.Maxdepth,-100000,100000,self.MeNu,BlockNo)
        print "returning move ",move
        self.MakeMove((move[0]//4) * 4 + (move[1]//4),(move[0]%4,move[1]%4),self.MeNu)
        print "Time taken : ", time.time() - start
        return move
    def CheckGameOver(self) :
        # print "Inside CheckGameOver "
        Draws = 0
        for row in range(4) :
            if self.RowS[row][self.WinNu] == 4 or self.RowS[row][self.LoseNu] == 4 :
                return True
            Draws += self.RowS[row][self.DrawNu] + self.RowS[row][self.WinNu] + self.RowS[row][self.LoseNu]
        for col in range(4) :
            if self.ColS[col][self.WinNu] == 4 or self.ColS[col][self.LoseNu] == 4 :
                return True
            # Draws +=  self.ColS[col][self.DrawNu] + self.ColS[col][self.WinNu] + self.ColS[col][self.LoseNu]
        for diag in range(2) :
            if self.DiagS[diag][self.WinNu] == 4 or self.DiagS[diag][self.LoseNu] == 4 :
                return True
            # Draws += self.DiagS[diag][self.DrawNu] + self.DiagS[diag][self.WinNu] + self.DiagS[diag][self.LoseNu]
        if Draws == 16 :
            return True
        # print "Returning False"
        return False

    def FindBoardUtility(self) :
        ans = 0
        # Board Based Utility
        for row in range(4) :
            if (self.RowS[row][self.WinNu] == 0 or self.RowS[row][self.LoseNu] == 0 ) and self.RowS[row][self.DrawNu] == 0 :
                ans += self.NUtility(self.Rows[row])
        for col in range(4) :
            if (self.ColS[col][self.WinNu] == 0 or self.ColS[col][self.LoseNu] == 0 ) and self.ColS[col][self.DrawNu] == 0 :
                ans += self.NUtility(self.Cols[col])

        for diag in range(2) :
            if (self.DiagS[diag][self.WinNu] == 0 or self.DiagS[diag][self.LoseNu] == 0 ) and self.DiagS[diag][self.DrawNu] == 0:
                ans += self.NUtility(self.Diags[diag])

        ans2 = 0
        # WeightedSUm
        for block in range(16) :
            ans2 += self.Weights[block] * self.Blocks[block].BlockUtility
        ans2 = float(ans2)/float(10)
        # print "BoardUtility is " ,ans + ans2
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
        # print " in undo "
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


    def MoveSet(self,BlockNo) :
        # print "Moveset inside BlockNo : ",BlockNo
        AvailableMoves = []
        for row in range(4) :
            for col in LineState.AvailableMoves[ self.Blocks[BlockNo].Rows[row] ] :
                AvailableMoves.append((row,col))
        # print AvailableMoves
        def comp(move1,move2) :
            if self.Blocks[BlockNo].History[move1[0]][move1[1]] < self.Blocks[BlockNo].History[move2[0]][move2[1]] :
                return -1
            if self.Blocks[BlockNo].History[move1[0]][move1[1]] > self.Blocks[BlockNo].History[move2[0]][move2[1]] :
                return 1
            return 0

        AvailableMoves = sorted(AvailableMoves,comp)
        if len(AvailableMoves) == 0 :
            print "this one is empty " ,BlockNo
            for row in range(4) :
                print self.Blocks[BlockNo].Rows[row]," ",LineState.AvailableMoves[ self.Blocks[BlockNo].Rows[row] ]
                print self.Blocks[BlockNo].Cols[row]," ",LineState.AvailableMoves[ self.Blocks[BlockNo].Cols[row] ]
        return AvailableMoves

    def BlockVal(self,BlockNo) :
        ans = self.Rows[self.Index[BlockNo][0]] + self.Cols[self.Index[BlockNo][1]]
        if self.Index[BlockNo][0] == self.Index[BlockNo][1] :
            ans += self.Diags[0]
        if self.Index[BlockNo][0] + self.Index[BlockNo][1] == 3 :
            ans += self.Diags[1]

        ans += self.Blocks[BlockNo].BlockUtility
        # print "for block ",BlockNo," ans = ",ans
        return ans

    def BlockSet(self,player) :
        AvailableMoves = []
        for block in range(16) :
            if self.Blocks[block].Status == "War" and self.Blocks[block].EmptyCells > 0 :
                AvailableMoves.append(block)

        def comp(block1,block2) :
            val1 = self.BlockVal(block1)
            val2 = self.BlockVal(block2)
            if val1 < val2 :
                return -1
            if val1 > val2 :
                return 1
            return 0
        AvailableMoves = sorted(AvailableMoves,comp)

        if player == self.EnemyNu :
            AvailableMoves.reverse()

        return AvailableMoves

    def FindNextBlock(self,Move) :
        return 4*Move[0] + Move[1]
    def alphabetaRunner(self,depth,alpha,beta,player,BlockNo) :
        if BlockNo != -1 and self.Blocks[BlockNo].Status == "War" and self.Blocks[BlockNo].EmptyCells > 0:
            # print "inside Ruuner War BlockNo : ",BlockNo
            MoveSet = self.MoveSet(BlockNo)
            self.MakeMove(BlockNo,MoveSet[0],player)
            # print "Made 1st best move"
            # For the thought best move do the complete search
            current = -self.alphabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(MoveSet[0]))
            # print "Finished"
            BestMove = MoveSet[0]

            self.UndoMove(BlockNo,MoveSet[0],player)

            if current > alpha :
                if current >= beta :
                    self.Blocks[BlockNo].History[BestMove[0]][BestMove[1]] += self.PowersOf2[depth]
                    return current
                alpha = current


            for i in range(1,len(MoveSet)) :
                # Play according to assumption
                self.MakeMove(BlockNo,MoveSet[i],player)
                # print "Runner At depth ",depth ," making move ",i
                score = -self.alphabeta(depth - 1,-alpha-1,-alpha,player^1,self.FindNextBlock(MoveSet[i]))
                # print "Finished ",i

                # Case where our assumption fails
                if score > alpha and score < beta :
                    score = -self.alphabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(MoveSet[i]))

                self.UndoMove(BlockNo,MoveSet[i],player)

                if score > current :
                    current = score
                    BestMove = MoveSet[i]
                    if score > alpha :
                        alpha = score
                    if score >= beta :
                        break

            BestMove = (BestMove[0] + 4*self.Index[BlockNo][0] , BestMove[1] + 4*self.Index[BlockNo][1])
            return (BestMove,current)

        # We are at a free node
        else :
            # print "Inside Runner Free node"
            MoveSet = self.BlockSet(player)
            BestMove = self.WasteMove
            for i in range(len(MoveSet)) :
                if depth < 2 and not self.ExtensionGiven :
                    self.ExtensionGiven = True
                    move,score = self.alphabetaRunner(2,alpha,beta,player,MoveSet[i])
                    self.ExtensionGiven = False
                else :
                    move,score = self.alphabetaRunner(depth-1,alpha,beta,player,MoveSet[i])
                if score >= alpha :
                    BestMove = move
                    alpha = score
                if score >= beta :
                    break
            return BestMove,alpha

    def alphabeta(self,depth,alpha,beta,player,BlockNo) :

        # print "Inside alphabeta BlockNo : ",BlockNo," Player : ",player," depth : ",depth
        if depth == 0 or self.CheckGameOver() :
            # print "FindBoardUtility"
            return self.FindBoardUtility()

        # order the moves in the required order
        if self.Blocks[BlockNo].Status == "War" and self.Blocks[BlockNo].EmptyCells > 0 :
            # print "alphabeta - Inside War"
            MoveSet = self.MoveSet(BlockNo)

            self.MakeMove(BlockNo,MoveSet[0],player)

            # For the thought best move do the complete search
            current = -self.alphabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(MoveSet[0]))
            BestMove = MoveSet[0]
            self.UndoMove(BlockNo,MoveSet[0],player)

            if current > alpha :
                if current >= beta :
                    self.Blocks[BlockNo].History[BestMove[0]][BestMove[1]] += self.PowersOf2[depth]
                    return current
                alpha = current

            # print "alphabeta - done making 1st move"

            for i in range(1,len(MoveSet)) :
                # Play according to assumption
                self.MakeMove(BlockNo,MoveSet[i],player)

                # print "alphabeta at depth ",depth," making move ",i
                score = -self.alphabeta(depth - 1,-alpha-1,-alpha,player^1,self.FindNextBlock(MoveSet[i]))
                # print "Got score ",score

                # Case where our assumption fails
                if score > alpha and score < beta :
                    # print "inside false assumption"
                    score = -self.alphabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(MoveSet[i]))

                self.UndoMove(BlockNo,MoveSet[i],player)
                # print "undo"
                if score > current :
                    current = score
                    BestMove = MoveSet[i]
                    if score > alpha :
                        alpha = score
                    if score >= beta :
                        break

            # Update History Table
            self.Blocks[BlockNo].History[BestMove[0]][BestMove[1]] += self.PowersOf2[depth]
            # print "Returning current as ",current
            return current

        # We are at a free node
        else :
            # print "Inside Not runners freenode"
            MoveSet = self.BlockSet(player)

            for i in range(len(MoveSet)) :
                if depth-1 < 2 and not self.ExtensionGiven :
                    self.ExtensionGiven = True
                    score = self.alphabeta(2,alpha,beta,player,MoveSet[i])
                    self.ExtensionGiven = False
                else :
                    score = self.alphabeta(depth-1,alpha,beta,player,MoveSet[i])

                if score >= alpha :
                    alpha = score
                if alpha >= beta :
                    break
            return alpha
