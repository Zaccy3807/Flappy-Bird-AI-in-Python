import random
#The evolutionary algorithm
class Evolution:
    def __init__(self, population, mutation_rate, population_size):
        self.mutation_rate = mutation_rate
        self.population = population
        self.population_size = population_size

    def mutate(self, network):
         if random.randint(1, self.mutation_rate) == 1:
            subject = random.choice(network)
            change = random.choice([subject.weights, subject.bias])
            if change == subject.weights:
                weight = random.choice(change)
                mutated_weight = random.uniform(-3, 3)
                change.insert(change.index(weight), mutated_weight)
                change.remove(weight)
                subject.weights = change
            else:
                subject.bias = random.uniform(-1, 1)

    def get_parents(self, population):
        parents = []
        for i in range(len(population)):
            p1 = random.choice(population)
            p2 = random.choice(population)
            if p1[1] >= p2[1]:
                population.remove(p1)
                parents.append(p1)
            else:
                population.remove(p2)
                parents.append(p2)
        return parents

    def get_child(self, parents, cls):
        p1 = random.choice(parents)
        p2 = random.choice(parents)
        p1 = p1[0]
        p2 = p2[0]
        child = [cls([], [random.choice([p1.weights[i], p2.weights[i]]) for i in range(3)], random.choice(p1))]