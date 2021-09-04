"""
gimkit_neuralnetwork2

Description: This is the second and successful implementation of a
             neural netowrk in gimkit. The bots are really dumb though
             so I would either need to change to genetic algorithm to
             the NEAT algorithm or train this bot for hours.

Devlog:
3/17/21 - Bare bones of the neural network have been finished.
3/18/21 - Reprogramming gimkit simulation to fit the neural network and
          connecting the neural network to the gimkit simulation.
          Major Error (Debugged): New generation of neural networks all 
          have the same weights and biases.
          Gimkit Simulation and the linking of neural network is finished.
3/19/21 - Improving messed up UI system and adding saving and loading
          best bot feature.
          UI system and saving and loading best bot feature is finished.
          Saving best bot feature is kinda messed up and shouldn't be
          used because Techsmart automatically logs you out.
          Also changed it from mutating from BestPlayer (Best bot of the
          generation) to BestPlayerEver (Best boy of all simulations).
3/20/21 - Issues trying to figure out a good equation for overallFitness
          value.
3/21/21 - Moved the neural network from TechSmart to my PC and the
          program is way faster. The save function is also way more
          reliable. I added 5 new inputs, miniUsed, megaUsed, quadUsed,
          totalQ, and simulationQ. Also deleted biases for input neurons
          since your actually not supposed have biases for them.
          Tried adding the BestPlayerOverall from the last generation to
          current generation to compare it to eachother, but many bugs
          such as simulations ending too quickly, questions go up by two,
          and BestPlayerOverall has terrible performance.
          (Debugged): Multiple BestPlayerOverall in PlayerList causing
          questions to go up by two and BestPlayerOverall being mutated
3/22/21 - Issue with fitness function. Some players have better fitness
          value, but have worse fitnessOverall
4/18/21 - Made it save BestPlayerOverall per each generation, I can go
          afk and it saves the best player without any inputs needed.
          It also is used to find out how long it takes for the bot to
          to get better because each of the saves tells which generation
          it was on. I was unable to find a better .overallFitness
          function, so I tried .fitness because the BestPlayerOverall
          is already going to be in the next generation, but it didn't
          really work because they were advancing less than using
          .overallFitness
"""
import random, json, copy
#import pygame
#pygame.init()
class User:
    #Gimkit shop values
    mpqValue = [1,5,50,100,500,2000,5000,10000,250000,1000000]
    streakValue = [1,3,10,50,250,1200,6500,35000,175000,1000000]
    multValue = [1,1.5,2,3,5,8,12,18,30,100]
    mpqCost = [0,10,100,1000,10000,75000,300000,1000000,10000000,100000000,999999999999]
    streakCost = [0,20,200,2000,20000,200000,2000000,20000000,200000000,2000000000,99999999999]
    multCost = [0,50,300,2000,12000,85000,700000,6500000,65000000,1000000000,999999999999]
    mEarnedSum = 0
    upgradeSum = 0
    def CreateNN(self,layernum):
        #-----Creating Neural Network-----#
        self.neurons = []
        self.bias = []
        self.weights = []
        self.layernum = layernum
        #Creates Neurons
        for i in range(len(layernum)):
            self.neurons.append([])
            for j in range(layernum[i]):
                self.neurons[i].append(0.0)
        #Sets biases for Neurons ###(Bias Structure: [layer2, layer3, ...])###
        for i in range(len(layernum)-1):
            self.bias.append([])
            for j in range(layernum[i+1]):
                self.bias[i].append(0.0)
        #Sets weights from layer to layer
        for i in range(len(layernum)-1):
            self.weights.append([])
            for j in range(layernum[i+1]):
                self.weights[i].append([])
                for b in range(layernum[i]):
                    self.weights[i][j].append(random.uniform(-1,1))        
    def think(self):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for b in range(len(self.weights[i][j])):
                    #Caltulates for the next neuron layer(self.neurons[i+1][j])
                    self.neurons[i+1][j] = self.relu(self.dot(self.neurons[i], self.weights[i][j]) + self.bias[i][j])
                    #print(self.dot(PlayerList[0].weights[0][0], PlayerList[0].neurons[0]) + PlayerList[0].bias[0][0])
    def mutate(self, mutationRate):
        #Replace nn with the best nn
        self.neurons = copy.deepcopy(BestPlayerOverall.neurons)
        self.weights = copy.deepcopy(BestPlayerOverall.weights)
        self.bias = copy.deepcopy(BestPlayerOverall.bias)
        #-----Mutation-----#
        #changing bias by mutation rate
        for i in range(len(self.neurons)-1):
            for j in range(len(self.neurons[i])):
                if random.randint(1,100) <= mutationRate * 100:
                    if random.randint(1,100) <= 10: #there's a 90% chance is changes the bias by a little bit
                        self.bias[i][j] = random.uniform(-1,1) #and a 10% chance it becomes a whole new bias
                    else:
                        self.bias[i][j]*=random.uniform(-2,2)
                        if self.bias[i][j] > 1:
                            self.bias[i][j] = 1
                        elif self.bias[i][j] < -1:
                            self.bias[i][j] = -1
        #changing weights by mutation rate
        for i in range(len(self.neurons)-1):
            for j in range(len(self.neurons[i+1])):
                for b in range(len(self.neurons[i])):
                    if random.randint(1,100) <= mutationRate * 100:
                        if random.randint(1,100) <= 10: 
                            self.weights[i][j][b]=random.uniform(-1,1)  
                        else:
                            self.weights[i][j][b]*=random.uniform(-2,2)
                            if self.weights[i][j][b] > 1:
                                self.weights[i][j][b] = 1
                            elif self.weights[i][j][b] < -1:
                                self.weights[i][j][b] = -1
    def __init__(self, index):
        self.level_ten = False
        self.question = 0
        self.totalQ = 0
        self.money = 0
        self.mEarned = 0
        self.mpqLevel = 1
        self.streakLevel = 1
        self.multLevel = 1
        self.miniUsed = False
        self.megaUsed = False
        self.quadUsed = False
        self.totalUpgrades = 0
        self.totalmEarned = 0
        self.overallFitness = 0.0
        self.fitness = 0.0
        self.index = index
        self.generation = 0
        self.output = []
    def __repr__(self):
        return "Player({})".format(self.index)
    def bonusCommand(self,cost, multiplierCost, string):
        self.money-=cost
        self.mEarned*=multiplierCost
        if commentsEnabled:
            print(string + " Bonus, Money " + str(self.money))
    def resetGimkit(self):
        self.level_ten = False
        self.question = 0
        self.totalQ = 0
        self.money = 0
        self.mEarned = 0
        self.mpqLevel = 1
        self.streakLevel = 1
        self.multLevel = 1
        self.fitness = 0.0
        self.overallFitness = 0.0
        self.totalUpgrades = 0
        self.totalmEarned = 0
        self.miniUsed = False
        self.megaUsed = False
        self.quadUsed = False
    @staticmethod
    def dot(list1,list2):
        try:
            total = 0
            for i in range(len(list1)):
                total += list1[i]*list2[i]
            return total
        except:
            print("List1: " +str(list1))
            print("List2: " +str(list2))
            print("ERROR: Lists are different lengths")
    @staticmethod
    def relu(x):
        return max(0,x)
#Functions
#NN Variables
PlayerList = []
FitnessList = []
BestPlayer = User("best") #The best player of a single generation
BestPlayerOverall = User("BEST") #The best player of all generations
BestPlayer.fitness = -1.0
BestPlayerOverall.fitness = -1.0
BPAttributes = { #For json file
  "neurons": [],
  "bias": [],
  "weights": [],
  "generation": 0
}
do_next = ''
commentsEnabled = False
PlayersExist = False
loadBest = input("Load Best? (1 = True, 0 = False) ")
if loadBest == '1':
    do_next = '2'
    with open("BestPlayerEver.json") as f:
        data = json.load(f)
        BestPlayer.CreateNN([6,20,33])
        BestPlayer.neurons = data["neurons"] 
        BestPlayer.bias = data["bias"]
        BestPlayer.generation = data["generation"]
        BestPlayer.weights = data["weights"]
    BestPlayerEver = copy.deepcopy(BestPlayer)
    PlayerList.append(copy.deepcopy(BestPlayer))
    PlayerList[0].resetGimkit()
    gen = 1
    popSize = 0
    commentsEnabled = True
else:
    gen = int(input("How many generations? "))
    popSize = int(input("What is the population size for each generation? "))
simulationQ = int(input("How many questions for training? "))
mutateRate = float(input("What is the mutation rate? "))
while True:
    #Creating objects and nn
    #if do_next was '1', playerlist would have been deleted
    #if do_next was '2', playerlist would contain the best bot
    if PlayerList == []: #if playerexsist == False:
        for i in range(popSize):
            PlayerList.append(User(i))
        for obj in PlayerList:
            obj.CreateNN([11,22,33])
    #If BestPlayer was already chosen and do_next isn't '2'(bestplayer replay), mutate then
    if BestPlayer.fitness != -1.0 and do_next != '2':
        for obj in PlayerList:
            obj.mutate(mutateRate)
            obj.resetGimkit()
    #Makes sure players exist
    PlayersExist = True
    if commentsEnabled:
        PlayersExist = False
    #-----Gimkit Simulation-----#
    for generation in range(gen):
        if do_next == '2':
            print("Generation:{}".format(PlayerList[0].generation))
        else:
            print("Generation:{}".format(generation+1))
            for obj in PlayerList:
                obj.generation = generation + 1
        gimkitGame = True
        while gimkitGame:
            for obj in PlayerList:
                #Checks if all 10 levels are unlocked
                obj.level_ten = obj.mpqLevel == 10 and obj.streakLevel == 10 and obj.multLevel == 10
                if not obj.level_ten:
                    obj.question+=1
                    obj.totalQ+=1
                if obj.totalQ == simulationQ:
                    gimkitGame = False
                #Puts inputs into the neurons
                obj.neurons[0][0] = obj.mpqLevel/10
                obj.neurons[0][1] = obj.streakLevel/10
                obj.neurons[0][2] = obj.multLevel/10
                obj.neurons[0][3] = obj.question/10
                obj.neurons[0][4] = obj.money/1000000000000 #1,000,000,000,000
                obj.neurons[0][5] = obj.mEarned/100000000 #100,000,000
                obj.neurons[0][6] = 1 if obj.miniUsed == True else 0
                obj.neurons[0][7] = 1 if obj.megaUsed == True else 0
                obj.neurons[0][8] = 1 if obj.quadUsed == True else 0
                obj.neurons[0][9] = float(obj.totalQ/simulationQ) #How much of the simulation question is done
                obj.neurons[0][10] = float(simulationQ/183) #183 is the number of questions of a human could get all level 10
                #print(obj.neurons[0])
                obj.think()
                #-----Buying Upgrade-----#
                #Puts last layer of neurons into list "output"
                obj.output = []
                #Trying to sort the last list of neurons into obj.output
                #repeats for the length of the last list in the neurons.
                for i in range(len(obj.neurons[len(obj.neurons)-1])): #(len(obj.neurons)-1) is the index of the last list in the neurons
                    obj.output.append([obj.neurons[len(obj.neurons)-1][i],i])
                obj.output.sort() #output = ([score of confidence, upgradeIndex])
                #Tries to find 'upgradeIndex,' the index of the most positive output neuron
                #   upgradeIndex corresponding to upgrades:
                #   [1-10]  --> mpqUpgrade to level [1-10]
                #   [11-20] --> streakUpgrade to level [11-20]
                #   [21-30] --> multUpgrade to level [21-30]
                #   [31-33] --> mini bonus, mega bonus, quadgrader (in order)
                for i in range(len(obj.neurons[len(obj.neurons)-1])): #(len(obj.neurons)-1) is the index of the last list in the neurons
                    obj.upgradeIndex = obj.output[len(obj.neurons[len(obj.neurons)-1])-1-i][1]
                    #len(obj.neurons[len(obj.neurons)-1]) is the length of the last list of neurons
                    #we are subtracting (-1-i) because index starts has to start at 0 (-1) and i (-i) is to sort through the output list
                    #checks if upgrade index is 1-30 which is mpq, streak, and mult upgrades
                    if obj.upgradeIndex >= 1 and obj.upgradeIndex <= 30:
                        #checks for mpq upgrade
                        if (obj.upgradeIndex >= 1 and obj.upgradeIndex <= 10 and #checks if upgrade index is for mpq
                            obj.mpqLevel < obj.upgradeIndex % 10): #checks upgrading to that level(upgradeIndex % 10) can actually be upgraded
                            if commentsEnabled:
                                print("Thinking about MPQ Level {}, Money {}".format(obj.upgradeIndex%10, obj.money))
                            if obj.money >= User.mpqCost[(obj.upgradeIndex % 10)-1]:
                                obj.money-=User.mpqCost[(obj.upgradeIndex % 10)-1]
                                obj.mpqLevel = obj.upgradeIndex % 10
                                obj.question = 1
                                if commentsEnabled:
                                    print("Upgrade MPQ to Level {}, Money {}".format(obj.upgradeIndex % 10, obj.money))
                            break
                        #checks for streak level
                        elif (obj.upgradeIndex >= 11 and obj.upgradeIndex <= 20 and 
                              obj.streakLevel < obj.upgradeIndex % 10):
                            if commentsEnabled:
                                print("Thinking about Streak Level {}, Money {}".format(obj.upgradeIndex%10, obj.money))
                            if obj.money >= User.streakCost[(obj.upgradeIndex % 10)-1]:
                                obj.money-=User.streakCost[(obj.upgradeIndex % 10)-1]
                                obj.streakLevel = obj.upgradeIndex % 10
                                obj.question = 1
                                if commentsEnabled:
                                    print("Upgrade Streak to Level {}, Money {}".format(obj.upgradeIndex % 10, obj.money))
                            break
                        #checks for mult level
                        elif (obj.upgradeIndex >= 21 and obj.upgradeIndex <= 30 and
                              obj.multLevel < obj.upgradeIndex % 10):
                            if commentsEnabled:
                                print("Thinking about Multiplier Level {}, Money {}".format(obj.upgradeIndex%10, obj.money))
                            if obj.money >= User.multCost[(obj.upgradeIndex % 10)-1]:
                                obj.money-=User.multCost[(obj.upgradeIndex % 10)-1]
                                obj.multLevel = obj.upgradeIndex % 10
                                obj.question = 1
                                if commentsEnabled:
                                    print("Upgrade Multiplier to Level {}, Money {}".format(obj.upgradeIndex % 10, obj.money))
                            break
                    #checks upgradeIndex for bonuses
                    elif obj.upgradeIndex == 31 and obj.miniUsed == False:
                        if commentsEnabled:
                            print("Thinking about x2 Mini Bonus, Money {}".format(obj.money))
                        if obj.money >= 85:
                            obj.bonusCommand(85,2,"x2 Mini")
                            obj.miniUsed = True
                        break
                    elif obj.upgradeIndex == 32 and obj.megaUsed == False:
                        if commentsEnabled:
                            print("Thinking about x5 Mega Bonus, Money {}".format(obj.money))
                        if obj.money >= 85:
                            obj.bonusCommand(85,5,"x5 Mega")
                            obj.megaUsed = True
                        break
                    elif obj.upgradeIndex == 33 and obj.quadUsed == False:
                        if commentsEnabled:
                            print("Thinking about Quadgrader, Money {}".format(obj.money))
                        if obj.money >= 1850:
                            obj.money-=1850
                            obj.mpqLevel+=1
                            obj.streakLevel+=1
                            obj.multLevel+=1
                            obj.mpqLevel = min(obj.mpqLevel, 10)
                            obj.streakLevel = min(obj.streakLevel, 10)
                            obj.multLevel = min(obj.multLevel, 10)
                            quadUsed = True
                            if commentsEnabled:
                                print("Quadgrader Used")
                        break
                #Calculates money for questions
                obj.mEarned = (((obj.question-1)*User.streakValue[obj.streakLevel-1])+User.mpqValue[obj.mpqLevel-1])*User.multValue[obj.multLevel-1]
                obj.money+=int(obj.mEarned) #adds money to question
                obj.totalmEarned+=obj.mEarned
                User.mEarnedSum+=obj.mEarned
                #Print out results or if all ten levels are unlocked
                if obj.level_ten:
                    print("All ten levels done. totalQ: " + str(obj.totalQ))
                    #do_next = input("Enter (1 = check level_ten, 2 = show events, 3 = show neuron, 4 = break)")
                else:
                    pass
                    #print()
                    #print("MPQ: " + str(mpqLevel))
                    #print("Streak: " + str(streakLevel))
                    #print("Mult: " + str(multLevel))
                    #print("QUESTION: " + str(question))
                    #print("------------")
                    #print("money: " + str(obj.money))
                    #print("mEarned: " + str(obj.mEarned))
                    #print("totalQ: " + str(totalQ))
            print(PlayerList[0].totalQ)
        #-----Gimkit Simulation Done-----#
        #Finding and calculating fittest NN
        User.upgradeSum = 0
        User.mEarnedSum = 0
        for obj in PlayerList: #The overall fitness is decided by the levels of it's upgrades and the money it's made 42697880
            obj.overallFitness = ((obj.mpqLevel-1) + (obj.streakLevel-1) + (obj.multLevel-1)) + (obj.totalmEarned/3837930) #maximum amount of money it can make in 100 questions
            #obj.overallFitness = ((obj.mpqLevel-1) + (obj.streakLevel-1) + (obj.multLevel-1))
            User.upgradeSum += ((obj.mpqLevel-1) + (obj.streakLevel-1) + (obj.multLevel-1))
            User.mEarnedSum += obj.totalmEarned
        if not User.upgradeSum: #if totalUpgrades == 0
            User.upgradeSum = 1 #so divided by 0 errors won't occur
        for obj in PlayerList:
            obj.fitness = float(( #calculates fitness using the number of upgrades and amount of money it's made
                                ((obj.mpqLevel-1 + obj.streakLevel-1 + obj.multLevel-1)/User.upgradeSum) + 
                                (obj.totalmEarned/User.mEarnedSum)
                                )/2)
        PlayerList.sort(key=lambda x: x.fitness, reverse=True)
        #if BestPlayer.index != "Best":
        BestPlayer = copy.deepcopy(PlayerList[0])
        BestPlayer.index = "Best"
        #Used to use .overallFitness
        if BestPlayerOverall.fitness == -1.0 or BestPlayer.overallFitness > BestPlayerOverall.overallFitness:
            print("New BestPlayerOverall.overallFitness: {}".format(BestPlayer.overallFitness))
        #if BestPlayerOverall.fitness == -1.0 or BestPlayer.fitness > BestPlayerOverall.fitness:
            #print("New BestPlayerOverall.fitness: {}, BestPlayerOverall.index: {}".format(BestPlayer.fitness, PlayerList[0].index))
            BestPlayerOverall = copy.deepcopy(BestPlayer)
            #Downloads BestPlayer per generation
            with open('BestPlayerGenerations/BestPlayerEver' + str(BestPlayerOverall.generation) + '.json', 'w') as f:
                BPAttributes['neurons'] = copy.deepcopy(BestPlayerOverall.neurons)
                BPAttributes['bias'] = copy.deepcopy(BestPlayerOverall.bias)
                BPAttributes['generation'] = copy.deepcopy(BestPlayerOverall.generation)
                BPAttributes['weights'] = copy.deepcopy(BestPlayerOverall.weights)
                json.dump(BPAttributes, f, indent=2)
        #Fitness list for UI
        del FitnessList[:]
        for obj in PlayerList:
            FitnessList.append([obj,obj.overallFitness,obj.fitness])
        print("\n"+str(FitnessList))
        #Preparing and Mutating NN
        if do_next != '2':
            for obj in PlayerList:
                obj.mutate(mutateRate)
                obj.resetGimkit()
            #adds and deletes best player to player list
            for i in range(len(PlayerList)):
                if PlayerList[i].index == "Best":
                    del PlayerList[i]
                    break
            PlayerList.append(copy.deepcopy(BestPlayerOverall))
            PlayerList[len(PlayerList)-1].resetGimkit()
    #-----Generation Trainging Over-----#
    #BestPlayer training variables
    commentsEnabled = False
    #Normal UI code
    do_next = ''
    while do_next != "1" and do_next != "2" and do_next != "6":
        do_next = input("(1 = Train Again, 2 = Best NN, 3 = Change NN, 4 = Save BestPlayerOverall, 5 = Load BestPlayerEver.json, 6 = Quit) ")
        if do_next == "1":
            gen = int(input("How many generations? "))
            popSize = int(input("What is the population size for each generation? "))
            simulationQ = int(input("How many questions for training? "))
            #deletes list to create new bots
            del PlayerList[:]
        elif do_next == "2":
            BPAttributes['neurons'] = copy.deepcopy(BestPlayerOverall.neurons)
            BPAttributes['bias'] = copy.deepcopy(BestPlayerOverall.bias)
            BPAttributes['generation'] = copy.deepcopy(BestPlayerOverall.generation)
            BPAttributes['weights'] = copy.deepcopy(BestPlayerOverall.weights)
            print(BPAttributes)
            #print("neurons = {}\nweights = {}\nbias = {}".format(BestPlayerOverall.neurons,BestPlayerOverall.weights, BestPlayerOverall.bias))
            del PlayerList[:]
            PlayerList.append(copy.deepcopy(BestPlayerOverall))
            PlayerList[0].resetGimkit()
            gen = 1
            popSize = 0
            commentsEnabled = True
        elif do_next == "3":
            mutateRate = float(input("Change mutation rate to: "))
        elif do_next =="4":
                with open('BestPlayerEver ' + str(BestPlayerOverall.generation) + '.json', 'w') as f:
                    BPAttributes['neurons'] = copy.deepcopy(BestPlayerOverall.neurons)
                    BPAttributes['bias'] = copy.deepcopy(BestPlayerOverall.bias)
                    BPAttributes['generation'] = copy.deepcopy(BestPlayerOverall.generation)
                    BPAttributes['weights'] = copy.deepcopy(BestPlayerOverall.weights)
                    json.dump(BPAttributes, f, indent=2)
    #Quit code if 6 was entered
    if do_next == "6":
        break
