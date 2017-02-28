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

        # Line States
        # self.LineState = Cell4State.Cell4State()

        # Current Board
        self.Board = [ self.Empty for col in range(16) for row in range(16) ]

        # WasteMove / NoMove
        self.WasteMove = (-1,-1)
        # OpppoNents Move
        self.OppoMove = self.WasteMove

    def UpdateEnemyMove(self) :
        if self.OppoMove == self.WasteMove :
            return

        BlockNo = (self.OppoMove[0]//4) * 4 + (self.OppoMove[1]//4)
        BlockRow = self.OppoMove[0] % 4
        BlockCol = self.OppoMove[1] % 4

        self.BoardUtility -= self.Blocks[BlockNo].BlockUtility
        self.Blocks[BlockNo].UpdateForward((BlockRow,BlockCol),self.EnemyNu)
        self.BoardUtility += self.Blocks[BlockNo].BlockUtility


    def move(self, board, old_move, flag):
        self.OppoMove = old_move
        self.UpdateEnemyMove()
        return self.Move()

    def Move(self) :
