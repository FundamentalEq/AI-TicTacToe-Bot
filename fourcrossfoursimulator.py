# from fourcrossfour import *
import MC
import fourcrossfourh
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

def main_game() :
    Empty = '-'
    Player1 = 'x'
    Player2 = 'o'
    block = [[Empty for j in range(4)] for i in range(4)]

    ob1 = fourcrossfour.Block()
    ob2 = fourcrossfourh.Block()
    Player = random.choice([True,False])
    move = (-1,-1)
    while True :
        if Player :
            move = ob2.move(move)
            print "ABh bot moving ",move
            block = UpdateBlock(block,move,Player2)

        else :
            move = ob1.move(move)
            print "AB bot moving ",move
            block = UpdateBlock(block,move,Player1)


        for i in range(4) :
            print block[i]

        ret = GameStatus(block,Player1,Player2)
        if ret == 1 :
            print "Player 1 Won + AB"
            return 1

        elif ret == 2 :
            print "Player 2 Won + ABh"
            return 2

        elif ret == 0 :
            print "Game Draw"
            return 0

        Player ^= 1

def main():
    ab=0
    abh=0
    draw=0
    for i in range(100):
        t=main_game()
        if(t==1) :
            ab+=1
        elif(t==0):
            draw+=1
        else:
            abh+=1
    print("abh",abh)
    print("ab",ab)
    print("draw",draw)

main()
