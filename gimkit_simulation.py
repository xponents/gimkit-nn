"""
gimkit

Description: This was the start of the gimkit neural network. This
was a simulation of gimkit that cacluated upgrades, powerups, and
the number of questions answered. The only difference is from the
first neural network test was that I forgot to code the rebooter 
into this.
"""
#import pygame, tsapp
#pygame.init()
question = 0
totalQ = 0
totalmEarned = 0
money = 0
mEarned = 0
mpqLevel = 1
streakLevel = 1
multLevel = 1
mpqValue = [1,5,50,100,500,2000,5000,10000,250000,1000000]
streakValue = [1,3,10,50,250,1200,6500,35000,175000,1000000]
multValue = [1,1.5,2,3,5,8,12,18,30,100]
mpqCost = [0,10,100,1000,10000,75000,300000,1000000,10000000,100000000,999999999999]
streakCost = [0,20,200,2000,20000,200000,2000000,20000000,200000000,2000000000,99999999999]
multCost = [0,50,300,2000,12000,85000,700000,6500000,65000000,1000000000,999999999999]
while True:
    #Checks if all 10 levels are unlocked
    level_ten = mpqLevel == 10 and streakLevel == 10 and multLevel == 10
    if not level_ten:
        question+=1
        totalQ+=1
    #Buying Upgrade
    if money >= streakCost[streakLevel]:
        money-=streakCost[streakLevel]
        streakLevel+=1
        question=1
        print("Streak is now level " + str(streakLevel))
    elif money >= multCost[multLevel]:
        money-=multCost[multLevel]
        multLevel+=1
        question=1
        print("Multiplier is now level " + str(multLevel))
    elif money >= mpqCost[mpqLevel]:
        money-=mpqCost[mpqLevel]
        mpqLevel+=1
        question=1
        print("MPQ is now level " + str(mpqLevel))
    #Calculates money for questions
    if question > 1:
        mEarned = (((question-1)*streakValue[streakLevel-1])+mpqValue[mpqLevel-1])*multValue[multLevel-1]
    if question == 1:
        mEarned = (mpqValue[mpqLevel-1])*multValue[multLevel-1]
    #adds money to question
    mEarned = int(mEarned)
    money+=mEarned
    totalmEarned+=mEarned
    #Using Power Ups
    if mpqLevel == 4 and streakLevel == 3 and multLevel == 3 and money >= 85:
        money-=85
        mEarned = mEarned*10
        money+=mEarned
        print("x10 Mutiplier Bonus")
    if mpqLevel == 4 and streakLevel == 4 and multLevel == 4 and money >= 2000:
        money-=2000
        mpqLevel += 1
        streakLevel += 1
        multLevel += 1
        question = 1
        print("QuadGrader has been used")
    #if mpqLevel == 5 and streakLevel == 5 and multLevel == 5 and money >= 3200:
        #money-=3200
        #mpqLevel += 1
        #streakLevel += 1
        #multLevel += 1
        #question = 1
        #print("QuadGrader has been used")
    #if mpqLevel == 8 and streakLevel == 6 and multLevel == 7 and money >= 1000 and question == 3:
        #money-=1000
        #mEarned = mEarned*10
        #money+=mEarned
        #print("x10 Mutiplier Bonus")
    #Print out results or if all ten levels are unlocked
    if level_ten:
        print("All ten levels done. totalQ: " + str(totalQ))
        do_next = input("Enter (1 = check level_ten, 2 = show events, 3 = show neuron, 4 = break)")
    #else:
    elif totalQ == 100:
        print()
        print("MPQ: " + str(mpqLevel))
        print("Streak: " + str(streakLevel))
        print("Mult: " + str(multLevel))
        print("QUESTION: " + str(question))
        print("------------")
        print("money: " + str(money))
        print("mEarned: " + str(mEarned))
        print("totalmEarned: " + str(totalmEarned))
        print("totalQ: " + str(totalQ))
    #pygame.time.wait(0)
