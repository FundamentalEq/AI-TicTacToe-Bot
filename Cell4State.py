
class Cell4State() :
        def __init__(self) :
            self.Empty = '-'
            self.Me = 'x'
            self.MeNu = 0
            self.Enemy = 'o'
            self.EnemyNu = 1
            self.Empty = '-'
            self.States = {}
            self.ForwardAd = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            self.BackwardAd = [ [ [-1,-1] for cell in range(4)] for state in range(81) ]
            self.CurrentActiveStates = 0
            self.CurState = [self.Empty,self.Empty,self.Empty,self.Empty]
            self.dfs(self.CurrentActiveStates)

        def dfs(self,StateNo) :
            # Add the state to the list of known states
            self.States[str(self.CurState)] = StateNo
            self.CurrentActiveStates += 1

            NextStateNo = -1
            for cell in range(4) :
                # check for Empty cell
                if self.CurState[cell] == self.Empty :
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

                    # Restore the cell
                    self.CurState[cell] = self.Empty

        def BlockToRow(self,move) :
            return move[1]

        def BlockToCol(self,move) :
            return move[0]

        def BlocktoDiag(self,move) :
            return move[0]

        def UpdateStateForward(self,CurStateNo,Cell,Player) :
            # print self.ForwardAd[CurStateNo][Cell][Player], self.States[self.ForwardAd[CurStateNo][Cell][Player]]
            return self.ForwardAd[CurStateNo][Cell][Player]

        def UpdateStateBack(self,CurStateNo,Cell,Player) :
            # print self.BackwardAd[CurStateNo][Cell][Player], self.States[self.BackwardAd[CurStateNo][Cell][Player]]
            return self.BackwardAd[CurStateNo][Cell][Player]


a = Cell4State()
b = [ "aak" for i in range(81)]
for state in a.States :
    b[a.States[state]] = state
for i in range(81) :
    print i, b[i]
# print a.States