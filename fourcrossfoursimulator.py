# from fourcrossfour import *
import MC
import fourcrossfour
import sys
import random

def GetHumanMove() :
    print "U play with o"
    mvp = raw_input()
    mvp = mvp.split()
    return (int(mvp[0]), int(mvp[1]))

def GameStatus(block,Player1,Player2) :
    for i in range(4) :
        if block[i].count(Player1) == 4 :
            return 1
        if block[i].count(Player2) == 4 :
            return 2

    for j in range(4) :
        col = [block[i][j] for i in range(4)]
        if col.count(Player1) == 4 :
            return 1
        if col.count(Player2) == 4 :
            return 2

    diag = [block[i][i] for i in range(4)]
    if diag.count(Player1) == 4 :
        return 1
    if diag.count(Player2) == 4 :
        return 2

    diag = [block[i][i] for i in range(4)]
    if diag.count(Player1) == 4 :
        return 1
    if diag.count(Player2) == 4 :
        return 2

    ans = 0
    for i in range(4) :
        ans += block[i].count('-')
    if ans == 0 :
        return 0
    return -1

def UpdateBlock(block,move,player) :
    block[move[0]][move[1]] = player
    return block

def main() :
    Empty = '-'
    Player1 = 'x'
    Player2 = 'o'
    block = [[Empty for j in range(4)] for i in range(4)]

    # ob1 = MC.Block()
    ob2 = fourcrossfour.Block()
    Player = random.choice([True,False])
    move = (-1,-1)
    while True :
        if Player :
            move = ob2.move(move)
            print "AB bot moving ",move
            block = UpdateBlock(block,move,Player2)

        else :
            move = GetHumanMove()
            print "Human bot moving ",move
            block = UpdateBlock(block,move,Player1)


        for i in range(4) :
            print block[i]

        ret = GameStatus(block,Player1,Player2)
        if ret == 1 :
            print "Player 1 Won + MC"
            sys.exit()

        elif ret == 2 :
            print "Player 2 Won + AB"
            sys.exit()

        elif ret == 0 :
            print "Game Draw"
            sys.exit()

        Player ^= 1

main()
