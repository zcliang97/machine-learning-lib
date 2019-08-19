from numpy import np
import random

class GeneticAlgorithm:
    def __init__(self, createIndividual, mutateIndividual, fitnessFunction, crossoverFunction, population_size=1000, crossoverProb=0.6, mutateProb=0.4, alpha=0.5):
        self.create = createIndividual
        self.mutate = mutateIndividual
        self.fitness = fitnessFunction
        self.populationSize = population_size
        self.crossoverProb = crossoverProb
        self.mutateProb = mutateProb
        self.crossoverAlpha = alpha
        self.crossover = crossoverFunction
        
        # create the population of solutions using the create function
        self.population = [self.create() for i in range(population_size)]
    
    def run(self, numGenerations):
        bestSolution = []
        for i in range(numGenerations):
            # calculate the fitness of each individual in the population
            fitness = self.population.map(lambda solution: (self.fitness(solution), solution))

            # get the best 2 solutions
            best = sorted(fitness, key=lambda x: x[0])[:2]

            # put the best solution into the output
            bestSolution.append(best[0])

            # select the parents with Baker's Stochastic Universal Sampling Algorithm
            totalFitness = sum(val for val, sol in fitness)
            rouletteGap = totalFitness/(self.populationSize - 2)
            randomOffset = random.uniform(0, 1) * rouletteGap
            parents = []
            for j in range(self.populationSize - 2):
                rouletteValue = rouletteGap * j + randomOffset
                currSum = 0
                index = 0
                while currSum < rouletteValue:
                    currSum += fitness[index]
                    index += 1
                parents.append(self.population[index])

            # perform crossover
            children = []
            for j in range(0, self.populationSize - 2, 2):
                parents = self.population[j:j+2]
                # if perform crossover, then get the new chromosomes using the alpha to mix parents
                if random.uniform(0, 1) < self.crossoverProb:
                    childs = self.crossover(parents, self.crossoverAlpha)
                # else append the parents as the next generation's children
                else:
                    childs = parents[:]
                children += childs
            
            # perform mutation
            for child in children:
                # if perform mutation, mutate specific genes in the child
                if random.uniform(0, 1) < self.mutateProb:
                    self.mutate(child)

            # survivor selection using Elistism
            self.population = children + best
        return bestSolution
                