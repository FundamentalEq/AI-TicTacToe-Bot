from Cell4State imoort *
LineState = Cell4State()
class Block() :
    def __init__(self) :
        # Initially all are in State 0
        self.Rows = [ 0 for row in range(4)]
        self.Cols = [ 0 for col in range(4)]
        self.Diags = [ 0 for diag in range(2)]
        # Flags to indiacte blocks current state
        self.Won = False
        self.Lost = False
        self.War = True

        # No of Empty Cells
        self.EmptyCells = 16

        # Current Utility of the Block
        self.BlockUtility = 4*lineState.StateUtility[0]

  # [ Current State][ Cell No ][ Player No]
    def UpdateForward(self,Move,Player) :
        BoardUtilityChange = 1
        # Update Row State
        self.BlockUtility += LineState.UtilityChangeForward[ self.Rows[Move[0]] ][ Move[1] ][ Player ]
        BoardUtilityChange *= LineState.NormalizedUCF[ self.Rows[Move[0]] ][ Move[1] ][ Player ]
        self.Rows[Move[0]] = LineState.ForwardAd[ self.Rows[Move[0]] ][ Move[1] ][ Player ]
        # self.Won |= LineState.Won[ self.Rows[ Move[0]] ]
        # self.Lost |= LineState.Lost[ self.Rows[ Move[0] ] ]

        # Update Col State
        self.BlockUtility += LineState.UtilityChangeForward[ self.Cols[Move[1]] ][ Move[0] ][ Player ]
        BoardUtilityChange *= LineState.NormalizedUCF[ self.Cols[Move[1]] ][ Move[0] ][ Player ]
        self.Cols[Move[1]] = LineState.ForwardAd[ self.Cols[Move[1]] ][ Move[0] ][ Player ]
        # self.Won |= LineState.Won[ self.Rows[ Move[0] ] ]
        # self.Lost |= LineState.Lost[ self.Rows[ Move[0] ] ]

        # if this lies on diagonal 0
        if Move[0] == Move[1] :
            self.BlockUtility += LineState.UtilityChangeForward[ self.Diags[0] ][ Move[0] ][ Player ]
            BoardUtilityChange *= LineState.NormalizedUCF[ self.Diags[0] ][ Move[0] ][ Player ]
            self.Diags[0] = LineState.ForwardAd[ self.Diags[0] ][ Move[0] ][ Player ]

        # if this lies on diagonal 1
        if Move[0] + Move[1] == 3 :
            self.BlockUtility += LineState.UtilityChangeForward[ self.Diags[1] ][ Move[0] ][ Player ]
            BoardUtilityChange *= LineState.NormalizedUCF[ self.Diags[1] ][ Move[0] ][ Player ]
            self.Diags[1] = LineState.ForwardAd[ self.Diags[1] ][ Move[0] ][ Player ]

        # Decrement the number of Empty cells
        self.EmptyCells -= 1
        return BoardUtilityChange

    def UpdateBackward(self,Move,Player) :
        BoardUtilityChange = 1
        # Update Row State
        self.BlockUtility += LineState.UtilityChangeBackward[ self.Rows[Move[0]] ][ Move[1] ][ Player ]
        BoardUtilityChange *= LineState.NormalizedUCB[ self.Rows[Move[0]] ][ Move[1] ][ Player ]
        self.Rows[Move[0]] = LineState.BackwardAd[ self.Rows[Move[0]] ][ Move[1] ][ Player ]

        # Update Col State
        self.BlockUtility += LineState.UtilityChangeBackward[ self.Cols[Move[1]] ][ Move[0] ][ Player ]
        BoardUtilityChange *= LineState.NormalizedUCB[ self.Cols[Move[1]] ][ Move[0] ][ Player ]
        self.Cols[Move[1]] = LineState.BackwardAd[ self.Cols[Move[1]] ][ Move[0] ][ Player ]

        # if this lies on diagonal 0
        if Move[0] == Move[1] :
            self.BlockUtility += LineState.UtilityChangeBackward[ self.Diags[0] ][ Move[0] ][ Player ]
            BoardUtilityChange *= LineState.NormalizedUCB[ self.Diags[0] ][ Move[0] ][ Player ]
            self.Diags[0] = LineState.BackwardAd[ self.Diags[0] ][ Move[0] ][ Player ]

        # if this lies on diagonal 1
        if Move[0] + Move[1] == 3 :
            self.BlockUtility += LineState.UtilityChangeBackward[ self.Diags[1] ][ Move[0] ][ Player ]
            BoardUtilityChange *= LineState.NormalizedUCB[ self.Diags[1] ][ Move[0] ][ Player ]
            self.Diags[1] = LineState.BackwardAd[ self.Diags[1] ][ Move[0] ][ Player ]

        # Decrement the number of Empty cells
        self.EmptyCells += 1
        return BoardUtilityChange
