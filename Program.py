import time

import numpy as np
from helpers import *
from random import randint
from deap import base, algorithms
from deap import creator
from deap import tools

POPULATION_SIZE = 1000
TOURNAMENT_SIZE = 3
INDPB = 0.02
CXPB = 0.8
MUTPB = 0.2


class Program:
    def __init__(self, grid, start, end, max_time):
        self.time = time
        self.grid = grid
        self.end = end
        self.start = start
        self.width = grid.shape[0]
        self.height = grid.shape[1]
        self.time = max_time
        self.generations = int((self.width + self.height) * 1.5)


    def run(self):
        chromosome_size = self.width + self.height
        maze = Maze(self.grid, self.start, self.end)
        def eval_maze(i): return compute_fitness(i, maze),


        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("attr_gene", randint, 0, 3)
        toolbox.register("individual",
                         tools.initRepeat,
                         creator.Individual,
                         toolbox.attr_gene,
                         chromosome_size)

        toolbox.register("population",
                         tools.initRepeat,
                         list, toolbox.individual)


        toolbox.register("evaluate", eval_maze)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate",
                         tools.mutUniformInt,
                         low=0, up=3,
                         indpb=INDPB)

        toolbox.register("select",
                         tools.selTournament,
                         tournsize=TOURNAMENT_SIZE)

        stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(len)
        mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        mstats.register("avg", np.mean)
        mstats.register("std", np.std)
        mstats.register("min", np.min)
        mstats.register("max", np.max)


        hof = tools.HallOfFame(1)
        start_time = time.time()
        runs = 0

        while time.time() - start_time < self.time:
            runs += 1
            pop = toolbox.population(n=POPULATION_SIZE)
            pop, log = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB,
                                           self.generations,
                                           stats=mstats,
                                           halloffame=hof, verbose=True)


        path = extract_path(hof[0], maze)
        score = compute_fitness(hof[0], maze)
        repr = maze_repr(hof[0], maze)
        score = f"Fitness: {score} (smaller is better)\n"
        execution = "Execution time: {:.2f}s".format(time.time() - start_time)
        print(f"\n{runs} runs\n{execution}\nBest run:\n{score}\n{repr}")

        return path
