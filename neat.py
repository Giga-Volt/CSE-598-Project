# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 21:42:13 2020

@author: Gaurang Vichare
"""

import numpy as np
from random import random, choice, choices
from initialize import launchGame
from play import run

class NodeGene:
    def __init__(self, id, type, maxDistance):
        self.id = id
        self.type = type
        self.maxDistance = maxDistance
    
    def print(self):
        print(self.id, self.type, self.maxDistance)

class ConnectGene:
    def __init__(self, inId, outId, weight, enabled, innov):
        self.inId = inId
        self.outId = outId
        self.weight = weight
        self.enabled = enabled
        self.innov = innov
    def print(self):
        print(self.inId, self.outId, self.weight, self.enabled, self.innov)

class Genome:
    def __init__(self):
        self.maxId = 2502
        self.nodes = []
        for i in range(2500):
            self.nodes.append(NodeGene(i, 'Sensor', 0))
        for i in range(2500, 2503):
            self.nodes.append(NodeGene(i, 'Output', 1))
        
        self.connectGenes = []
        innov = 1
        for i in range(2500):
            for j in range(2500, 2503):
                weight = np.random.uniform(-1, 1)
                self.connectGenes.append(ConnectGene(i, j, weight, True, innov))
                innov += 1
    
    def mutateWeights(self):
        global pm
        for gene in self.connectGenes:
            rand = np.random
            if rand < pm:
                gene.weight = np.random.uniform(-1, 1)
    
    def addConnection(self):
        global innovation
        global innovationDict
        weight = np.random.uniform(-1, 1)
        nodePairs = []
        n = len(self.nodes)
        for i in range(n):
            for j in range(n):
                if i != j:
                    if self.nodes[i].type != 'Output' and self.nodes[j].type != 'Sensor' and self.nodes[i].maxDistance < self.nodes[j].maxDistance:
                        nodePairs.append((self.nodes[i].id, self.nodes[j].id))
                    elif self.nodes[j].type != 'Output' and self.nodes[i].type != 'Sensor' and self.nodes[j].maxDistance < self.nodes[i].maxDistance:
                        nodePairs.append((self.nodes[j].id, self.nodes[i].id))
        
        connectedPairs = []
        for gene in self.connectGenes:
            connectedPairs.append((gene.inId, gene.outId))
        
        setDifference = set(nodePairs) - set(connectedPairs)
        unconnectedPairs = list(setDifference)
        
        if not unconnectedPairs:
            return False
        connection = choice(unconnectedPairs)
        
        for innov, structure in innovationDict.items():
            if structure == (connection[0], connection[1], 'c'):
                self.connectGenes.append(ConnectGene(connection[0], connection[1], weight, True, innov))
                for node in self.nodes:
                    if node.id == connection[0]:
                        distance = node.maxDistance
                for node in self.nodes:
                    if node.id == connection[1]:
                        node.maxDistance = max(node.maxDistance, distance + 1)
                return True
        
        self.connectGenes.append(ConnectGene(connection[0], connection[1], weight, True, innovation))
        for node in self.nodes:
            if node.id == connection[0]:
                distance = node.maxDistance
        for node in self.nodes:
            if node.id == connection[1]:
                node.maxDistance = max(node.maxDistance, distance + 1)
        
        innovationDict[innovation] = (connection[0], connection[1], 'c')
        innovation += 1
        
        return True
    
    def addNode(self):
        global innovation
        global innovationDict
        gene = choice(self.connectGenes)
        inId = gene.inId
        outId = gene.outId
        oldWeight = gene.weight
        
        for node in self.nodes:
            if node.id == inId:
                inNode = node
            elif node.id == outId:
                outNode = node
        
        distance = inNode.maxDistance
        
        newId = self.maxId + 1
        self.maxId += 1
        self.nodes.append(NodeGene(newId, 'Hidden', distance + 1))
        
        outNode.maxDistance += 1
        
        flag = False
        for innov, structure in innovationDict.items():
            if structure == (inId, newId, 'n'):
                self.connectGenes.append(ConnectGene(inId, newId, 1, True, innov))
                flag = True
            elif structure == (newId, outId, 'n'):
                self.connectGenes.append(ConnectGene(newId, outId, oldWeight, True, innov))
                flag = True
        
        if flag == False:
            self.connectGenes.append(ConnectGene(inId, newId, 1, True, innovation))
            innovationDict[innovation] = (inId, newId, 'n')
            innovation += 1
            self.connectGenes.append(ConnectGene(newId, outId, oldWeight, True, innovation))
            innovationDict[innovation] = (newId, outId, 'n')
            innovation += 1
        
        gene.enabled = False
        
        return True
    
    def print(self):
        #print(len(self.nodes), len(self.connectGenes))
        for gene in self.connectGenes:
            gene.print()
            #if gene.inId == self.maxId or gene.outId == self.maxId:
            #    gene.print()
        #for node in self.nodes:
        #    if node.maxDistance > 0:
        #        node.print()

def crossover(parent1, parent2):
    return

innovation = 2500 * 3 + 1
innovationDict = {}
pc, pm, nga = 0.5, 0.01, 20
pAddNode, pAddConnection = 0.03, 0.1
g = Genome()
g.addNode()
g.addConnection()
g.print()
#browser, game_hwnd = launchGame();

#w = np.random.uniform(-1, 1, (2500, 3))

#fitness = run(w, browser, game_hwnd)
#print(fitness)

'''

def select(pk, fitnessValues):
    denominator = sum(fitnessValues)
    probability = fitnessValues / denominator
    q = np.cumsum(probability)
    
    parents = []
    for i in range(r):
        rand = random()
        for j in range(len(q)):
            if rand < q[j]:
                break
        parents.append(pk[j])
    parents = np.array(parents)
    return parents

def crossover(parent1, parent2):
    child1 = np.concatenate((parent1[0:3], parent2[3:5]), axis=None)
    child2 = np.concatenate((parent2[0:3], parent1[3:5]), axis=None)
    
    child1s = child1[0]
    child1v = child1[1:5]
    child2s = child2[0]
    child2v = child2[1:5]
    p = np.array([1 / 10, 1 / 100, 1 / 1000, 1 / 10000])
    p = p.T
    value1 = child1s * p @ child1v
    value2 = child2s * p @ child2v
    
    if value1 < -0.5 or value2 < -0.5:
        return False
    return child1, child2

def mutate(gene, i):
    if i == 0:
        newGene = np.random.randint(low=-1, high=1)
        if newGene == 0:
            newGene = 1
    else:
        newGene = np.random.randint(low=0, high=10)
    return newGene

pc, pm, nga = 0.5, 0.01, 20
# nga = number of iterations
r, m = 10, 20

numbers = 1.5 * np.random.random(m) - 0.5
numbers = np.around(numbers, decimals=4)
pk = []
for number in numbers:
    if number < 0:
        solution = [-1]
    else:
        solution = [1]
    num = abs(number * 10000)
    solution.append(int(num // 1000))
    num = num % 1000
    solution.append(int(num // 100))
    num = num % 100
    solution.append(int(num // 10))
    num = num % 10
    solution.append(int(num // 1))
    pk.append(solution)
pk = np.array(pk)



bestFitness = []
worstFitness = []
averageFitness = []
bestx = []

for k in range(nga):
    fitnessValues = np.apply_along_axis(fitness, 1, pk)
    
    bestFitness.append(np.max(fitnessValues))
    worstFitness.append(np.min(fitnessValues))
    averageFitness.append(np.average(fitnessValues))
    bestx.append(max(pk, key=fitness))
    
    parents = select(pk, fitnessValues)
    effectiveParents = []
    while not effectiveParents:
        for j in range(r):
            rand = random()
            if rand < pc:
                effectiveParents.append(parents[j])
    effectiveParents = np.array(effectiveParents)
    children = []
    for j in range((m - r) // 2):
        breeders = np.array(choices(effectiveParents, k=2))
        twins = crossover(breeders[0], breeders[1])
        if not twins:
            j -=1
            continue
        child1, child2 = twins
        children.append(child1)
        children.append(child2)
    children = np.array(children)
    for j in range(m - r):
        for i in range(n):
            rand = random()
            if rand < pm:
                newGene = mutate(children[j][i], i)
                mutant = np.copy(children[j])
                mutant[i] = newGene
                mutants = mutant[0]
                mutantv = mutant[1:5]
                p = np.array([1 / 10, 1 / 100, 1 / 1000, 1 / 10000])
                p = p.T
                value = mutants * p @ mutantv
                if value < -0.5:
                    i -= 1
                    continue
                children[j][i] = newGene
    pk = np.concatenate((parents, children))

fitnessValues = np.apply_along_axis(fitness, 1, pk)
bestFitness.append(np.max(fitnessValues))
worstFitness.append(np.min(fitnessValues))
averageFitness.append(np.average(fitnessValues))
bestx.append(max(pk, key=fitness))

bestIndividuals = []
for x in bestx:
    xs = x[0]
    xv = x[1:5]
    p = np.array([1 / 10, 1 / 100, 1 / 1000, 1 / 10000])
    p = p.T
    individual = xs * p @ xv
    bestIndividuals.append(individual)

plt.figure()

plt.subplot(211)
xs = range(nga + 1)
plt.plot(bestFitness, 'b-', label='Best Fitness')
for x, y in zip(xs, bestFitness):
    label = "{:.2f}".format(y)
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 15), ha='center', color='blue')
plt.plot(worstFitness, 'r-', label='Worst Fitness')
for x, y in zip(xs, worstFitness):
    label = "{:.2f}".format(y)
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, -15), ha='center', color='red')
plt.plot(averageFitness, 'g-', label='Average Fitness')
for x, y in zip(xs, averageFitness):
    label = "{:.2f}".format(y)
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 0), ha='center', color='green')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.xticks(np.arange(0, nga + 1, 1))
plt.legend(bbox_to_anchor=(0., 1.05, 1., .102), loc='lower left', ncol=3, mode="expand", borderaxespad=0.)

plt.subplot(212)
plt.plot(bestIndividuals, 'o')
for x, y in zip(xs, bestIndividuals):
    label = "{:.4f}".format(y)
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
plt.xlabel('Generation')
plt.ylabel('Best Individual')
plt.xticks(np.arange(0, nga + 1, 1))

plt.show()

'''