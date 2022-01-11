""" Genetic Algorithm Module
"""
from functools import wraps

class EvolutiveAlgorithm:
    def __init__(self,population_size, Maxim= True) -> None:
        self.pipeline=[]
        self.population_size=population_size
        self.population = []
        self.function_check=["new_ind","data"]
        self.maximize= Maxim
        self.compare = lambda a,b:a["fit"]>b["fit"] if self.maximize else lambda a,b:a["fit"]<b["fit"]
        self.compare_list = max if self.maximize else min

    def add_func_to_pipeline(self,function):
        """ plugin funcitonality pipeline
        """
        self.pipeline.append(function)
        return function

    def map_process(self,function):
        """ fitness fuctionality on each step
        """
        @wraps(function)
        def wrapper(*argv, **kwargv):
            _population = function(*argv,**kwargv)
            return [{"fit":self.fitness(_ind,self.data),"ind":_ind} for _ind in _population]
        return wrapper

    def set_ind_func(self,function):
        """ new population decorator
        """
        self.new_ind = function
        return function

    def set_fitness(self,function):
        """ fitness plugin functionality
        """
        self.fitness = function
        return function

    def new_population(self):
        self.population.clear()
        for ind_index in range(self.population_size):
            temp_ind = self.new_ind()
            temp_ind["fit"]= self.fitness(temp_ind["ind"],self.data)
            self.population.append(temp_ind)
    
    def check_function_settigs(self):
        for _func_N in self.function_check:
            if not hasattr(self,_func_N):
                raise ValueError("No >> "+_func_N+" : from EvolutiveAlgorithm Class << funciton setted")

    def run(self,generations):
        compare = lambda a,b:a["fit"]>b["fit"] if self.maximize else lambda a,b:a["fit"]<b["fit"]
        compare_list = max if self.maximize else min
        self.check_function_settigs()
        self.new_population()
        self.fitness_evolution=[]
        self.best_all={"ind":None,"fit":0 if self.maximize else float('inf') }
        self.best_last=None
        for generation in range(generations): 
            if(100*(generation/generations)%10==0):
                print(100*(generation/generations),"%")
            for func_index in range(len(self.pipeline)):
                self.population = self.pipeline[func_index](self.population)
                # print(self.population)
                temp_best_fitness = compare_list(self.population,key=lambda a:a['fit'])
                self.best_last = temp_best_fitness
                if(compare(temp_best_fitness,self.best_all)):
                    self.best_all=self.best_last
                # self.fitness_evolution.append( (generation+func_index/len(self.pipeline),self.best_last['fit'] ) )
                self.fitness_evolution.append( (self.best_last["ind"],self.best_last['fit'] ) )

       
