import math
from EvolutiveAlgorithm import EvolutiveAlgorithm

from numpy import arange
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi

import matplotlib.pyplot as plt
import decimal

import random
from datetime import datetime
random.seed(datetime.now())


POPULATION_SIZE = 50
GENERATIONS     = 1000

SELECTION_RATE = 0.2
CROSSOVER_RATE = 0.2
MUTATION_RATE = 0.2
MUTATION_HILLCLIMBING_RATE=0.1

MAXIMIZE = True

evol = EvolutiveAlgorithm( POPULATION_SIZE, MAXIMIZE )
evol.data = [0,1,2,3,4]

@evol.set_fitness
def fitness(x,data):
    # return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 -7)**2
    # return x[0]**2.0 + x[1]**2.0
    # return -20.0 * exp(-0.2 * sqrt(0.5 * (x[0]**2 + x[1]**2))) - exp(0.5 * (cos(2 * pi * x[0]) + cos(2 * pi * x[1]))) + e + 20
    # return math.sin(10*x[0])*(20-(x[0]-5)**2)
    return (20-(x[0]-5)**2)

@evol.add_func_to_pipeline
@evol.map_process
def selection(population):
    compare = lambda a,b:a>b if MAXIMIZE else lambda a,b:a<b
    new_population=[]
    for ind in population:
        parent1 = random.randint(0,len(population)-1)
        if random.random()<SELECTION_RATE:
            parent2 = random.randint(0,len(population)-1)
            parent1 = population[parent1]
            parent2 = population[parent2]
            new_population.append( parent1["ind"] if compare(parent1["fit"],parent2["fit"]) else parent2["ind"] )
        else:
            new_population.append(population[parent1]["ind"])
    return new_population

@evol.add_func_to_pipeline
@evol.map_process
def crossover(population):
    new_population=[]
    compare_list = max if MAXIMIZE else min
    compare = lambda a,b:a["fit"]>b["fit"] if MAXIMIZE else lambda a,b:a["fit"]<b["fit"]
    for ind in population:
        parent1 = random.randint(0,len(population)-1)
        if random.random()<CROSSOVER_RATE:    
            parent2 = random.randint(0,len(population)-1)
            parent1 = population[parent1]
            parent2 = population[parent2]
            sesgo = [parent1["fit"],parent2["fit"]]
            total = sum(sesgo)
            sesgo = [i/total for i in sesgo]
            # child = [sesgo[0]*parent1["ind"][0]+sesgo[1]*parent2["ind"][0],sesgo[0]*parent1["ind"][1]+sesgo[1]*parent2["ind"][1]]
            # child = [sesgo[0]*parent1["ind"][0]+sesgo[1]*parent2["ind"][0]]
            max_parent = parent1["ind"] if compare(parent1,parent2) else parent2["ind"]
            min_parent = parent1["ind"] if not compare(parent1,parent2) else parent2["ind"]
            child = [random.random()*(max_p-min_p)+min_p for max_p,min_p in zip(max_parent,min_parent)]
            new_population.append( child )
        else:
            new_population.append( population[parent1]["ind"] )
    return new_population

@evol.add_func_to_pipeline
@evol.map_process
def mutation(population):
    new_population=[]
    compare_list = max if MAXIMIZE else min
    compare = lambda a,b:a["fit"]>b["fit"] if MAXIMIZE else lambda a,b:a["fit"]<b["fit"]
    temp_best = compare_list(population,key=lambda a:a['fit'])
    child=None
    dir_vect=[]
    for ind in population:
        parent1 = random.randint(0,len(population)-1)
        if(random.random()<MUTATION_RATE):
            if(random.random()<MUTATION_HILLCLIMBING_RATE):
                # dir_vect = [temp_best['ind'][0]-population[parent1]['ind'][0],temp_best['ind'][1]-population[parent1]['ind'][1]] 
                dir_vect = [temp_best['ind'][0]-population[parent1]['ind'][0]] 
                dir_mod = 1 if compare(temp_best,population[parent1]) else -1
                dir_vect=[i*dir_mod for i in dir_vect]
            else:
                mod = random.random()     
                dir_vect.append((0.5 if random.random()>0.5 else -0.5)*mod)
                dir_vect.append((0.5 if random.random()>0.5 else -0.5)*mod)
            # child = [population[parent1]["ind"][0]+dir_vect[0]*random.random(),population[parent1]["ind"][1]+dir_vect[1]*random.random()]
            child = [population[parent1]["ind"][0]+dir_vect[0]]
            new_population.append( child )
        else:
            new_population.append( population[parent1]["ind"] )
    return new_population

@evol.set_ind_func
def new_ind():
    # return {"ind":[random.random(),random.random()*8-4],"fit":0}
    return {"ind":[random.random()*10],"fit":0}


evol.run( generations=GENERATIONS )
print(evol.best_all)
print(evol.best_last)

_x = [i[0] for i in evol.fitness_evolution]
_y = [i[1] for i in evol.fitness_evolution]

# print(_x)
# print(_y)

plt.scatter(x=_x,y=_y)
plt.show()