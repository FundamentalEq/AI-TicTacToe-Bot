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

        # Current BoardUtility
        self.BoardUtility = 0
        for block in self.Blocks :
            self.BoardUtility += block.BlockUtility

        # Current Board
        # self.Board = [ self.Empty for col in range(16) for row in range(16) ]

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
        # **********************************************
        # Need to implement change of the Board Utility
        # **********************************************

        return 4*BlockRow + BlockCol

    def move(self, board, old_move, flag):
        BlockNo = self.UpdateEnemyMove(old_move)
        return self.Move(BlockNo)

    def Move(self,BlockNo) :
        # Free Move
        if self.CurBlock == -1 :
            pass

        # We know the block where we are supposed to move

    def CheckGameOver() :
        pass

    def UpdateBoardUtility() :
        pass

    def alpabeta(self,depth,alpha,beta,player,BlockNo) :

        if depth == 0 or self.CheckGameOver() :
            return self.BoardUtility

        # order the moves in the required order
        if self.BlockAvailable(BlockNo) :

            MoveSet = OrderMoves()

            self.Blocks[ BlockNo ].UpdateForward( MoveSet[0] , player )
            # For the thought best move do the complete search
            current = -self.alpabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(BlockNo,MoveSet[0]))
            BestMove = MoveSet[0]
            self.Blocks[ BlockNo ].UpdateBackward( MoveSet[0] , player)

            for i in range(1,len(MoveSet)) :
                # Play according to assumption
                self.Blocks[ BlockNo ].UpdateForward( MoveSet[i] , player )
                score = -self.alpabeta(depth - 1,-alpha-1,-alpha,player^1,self.FindNextBlock(BlockNo,MoveSet[0]))

                # Case where our assumption fails
                if score > alpha and score < beta :
                    score = -alpabeta(depth - 1,-beta,-alpha,player^1,self.FindNextBlock(BlockNo,MoveSet[0]))

                self.Blocks[ BlockNo ].UpdateBackward( MoveSet[0] , player)

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
