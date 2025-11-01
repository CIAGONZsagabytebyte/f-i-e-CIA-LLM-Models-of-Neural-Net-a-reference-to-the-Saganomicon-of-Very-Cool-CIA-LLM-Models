"""
Genetic Engine - Core genetic algorithm implementation

Implements evolutionary principles inspired by cosmic natural selection
and the saga of life's emergence across the universe.
"""

import random
from typing import Any, Callable, List, Optional, Dict, Tuple
import copy


class Individual:
    """An individual in the genetic algorithm population"""

    def __init__(self, genome: List[Any], fitness: Optional[float] = None):
        self.genome = genome
        self.fitness = fitness
        self.age = 0
        self.generation = 0
        self.lineage = []  # Track evolutionary history

    def mutate(self, mutation_rate: float, mutation_func: Callable = None) -> 'Individual':
        """Mutate the individual's genome"""
        if mutation_func is None:
            mutation_func = self._default_mutation

        new_genome = []
        for gene in self.genome:
            if random.random() < mutation_rate:
                new_genome.append(mutation_func(gene))
            else:
                new_genome.append(gene)

        return Individual(new_genome, fitness=None)

    def _default_mutation(self, gene: Any) -> Any:
        """Default mutation: perturb numeric genes or flip boolean genes"""
        if isinstance(gene, (int, float)):
            return gene + random.uniform(-1, 1)
        elif isinstance(gene, bool):
            return not gene
        elif isinstance(gene, str):
            return gene + random.choice('abcdefghijklmnopqrstuvwxyz')
        return gene

    def crossover(self, other: 'Individual', crossover_func: Callable = None) -> Tuple['Individual', 'Individual']:
        """Perform crossover with another individual"""
        if crossover_func is None:
            crossover_func = self._single_point_crossover

        return crossover_func(self, other)

    def _single_point_crossover(self, other: 'Individual') -> Tuple['Individual', 'Individual']:
        """Single-point crossover"""
        if len(self.genome) != len(other.genome):
            return copy.deepcopy(self), copy.deepcopy(other)

        point = random.randint(1, len(self.genome) - 1)

        child1_genome = self.genome[:point] + other.genome[point:]
        child2_genome = other.genome[:point] + self.genome[point:]

        child1 = Individual(child1_genome)
        child2 = Individual(child2_genome)

        child1.lineage = self.lineage + [self.genome[:3]]
        child2.lineage = other.lineage + [other.genome[:3]]

        return child1, child2

    def __repr__(self):
        fitness_str = f"{self.fitness:.4f}" if self.fitness is not None else "None"
        return f"Individual(genome={self.genome[:3]}..., fitness={fitness_str}, gen={self.generation})"

    def __lt__(self, other):
        """Enable sorting by fitness"""
        if self.fitness is None:
            return True
        if other.fitness is None:
            return False
        return self.fitness < other.fitness


class FitnessFunction:
    """Wrapper for fitness evaluation functions"""

    def __init__(self, func: Callable[[List[Any]], float], name: str = "fitness"):
        self.func = func
        self.name = name
        self.evaluations = 0
        self.best_fitness = None
        self.worst_fitness = None

    def evaluate(self, genome: List[Any]) -> float:
        """Evaluate fitness of a genome"""
        fitness = self.func(genome)
        self.evaluations += 1

        if self.best_fitness is None or fitness > self.best_fitness:
            self.best_fitness = fitness

        if self.worst_fitness is None or fitness < self.worst_fitness:
            self.worst_fitness = fitness

        return fitness

    def __call__(self, genome: List[Any]) -> float:
        return self.evaluate(genome)

    def __repr__(self):
        return f"FitnessFunction(name={self.name}, evals={self.evaluations})"


class Population:
    """A population of individuals undergoing evolution"""

    def __init__(self, size: int, genome_length: int, fitness_function: FitnessFunction,
                 gene_initializer: Callable = None):
        self.size = size
        self.genome_length = genome_length
        self.fitness_function = fitness_function
        self.gene_initializer = gene_initializer or (lambda: random.random())

        # Initialize population
        self.individuals = []
        for _ in range(size):
            genome = [self.gene_initializer() for _ in range(genome_length)]
            self.individuals.append(Individual(genome))

        self.generation = 0
        self.best_individual = None
        self.average_fitness_history = []

    def evaluate_fitness(self) -> None:
        """Evaluate fitness for all individuals"""
        for individual in self.individuals:
            individual.fitness = self.fitness_function.evaluate(individual.genome)
            individual.generation = self.generation

        # Sort by fitness (descending)
        self.individuals.sort(reverse=True)

        # Update best
        self.best_individual = self.individuals[0]

        # Track statistics
        avg_fitness = sum(ind.fitness for ind in self.individuals) / len(self.individuals)
        self.average_fitness_history.append(avg_fitness)

    def select_parents(self, selection_method: str = 'tournament') -> Tuple[Individual, Individual]:
        """Select two parents for reproduction"""
        if selection_method == 'tournament':
            return self._tournament_selection(), self._tournament_selection()
        elif selection_method == 'roulette':
            return self._roulette_selection(), self._roulette_selection()
        elif selection_method == 'rank':
            return self._rank_selection(), self._rank_selection()
        else:
            # Random selection
            return random.choice(self.individuals), random.choice(self.individuals)

    def _tournament_selection(self, tournament_size: int = 3) -> Individual:
        """Tournament selection"""
        tournament = random.sample(self.individuals, min(tournament_size, len(self.individuals)))
        return max(tournament, key=lambda ind: ind.fitness)

    def _roulette_selection(self) -> Individual:
        """Roulette wheel selection"""
        total_fitness = sum(ind.fitness for ind in self.individuals)
        if total_fitness == 0:
            return random.choice(self.individuals)

        pick = random.uniform(0, total_fitness)
        current = 0
        for individual in self.individuals:
            current += individual.fitness
            if current >= pick:
                return individual

        return self.individuals[-1]

    def _rank_selection(self) -> Individual:
        """Rank-based selection"""
        ranks = list(range(len(self.individuals), 0, -1))
        total = sum(ranks)
        pick = random.uniform(0, total)

        current = 0
        for individual, rank in zip(self.individuals, ranks):
            current += rank
            if current >= pick:
                return individual

        return self.individuals[-1]

    def get_statistics(self) -> Dict[str, Any]:
        """Get population statistics"""
        fitnesses = [ind.fitness for ind in self.individuals if ind.fitness is not None]

        return {
            'generation': self.generation,
            'size': len(self.individuals),
            'best_fitness': max(fitnesses) if fitnesses else None,
            'worst_fitness': min(fitnesses) if fitnesses else None,
            'average_fitness': sum(fitnesses) / len(fitnesses) if fitnesses else None,
            'fitness_std': self._calculate_std(fitnesses) if fitnesses else None
        }

    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if not values:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5

    def __repr__(self):
        return f"Population(size={self.size}, gen={self.generation}, best_fitness={self.best_individual.fitness if self.best_individual else None})"


class GeneticAlgorithm:
    """Main genetic algorithm coordinator"""

    def __init__(self, population: Population,
                 mutation_rate: float = 0.01,
                 crossover_rate: float = 0.7,
                 elitism_count: int = 2):
        self.population = population
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count

        self.mutation_func = None
        self.crossover_func = None
        self.selection_method = 'tournament'

    def set_mutation_function(self, func: Callable[[Any], Any]) -> 'GeneticAlgorithm':
        """Set custom mutation function"""
        self.mutation_func = func
        return self

    def set_crossover_function(self, func: Callable[[Individual, Individual], Tuple[Individual, Individual]]) -> 'GeneticAlgorithm':
        """Set custom crossover function"""
        self.crossover_func = func
        return self

    def set_selection_method(self, method: str) -> 'GeneticAlgorithm':
        """Set selection method: 'tournament', 'roulette', 'rank'"""
        self.selection_method = method
        return self

    def evolve_generation(self) -> None:
        """Evolve one generation"""
        # Evaluate current population
        self.population.evaluate_fitness()

        # Create new population
        new_individuals = []

        # Elitism: keep best individuals
        elite = self.population.individuals[:self.elitism_count]
        new_individuals.extend([copy.deepcopy(ind) for ind in elite])

        # Generate offspring
        while len(new_individuals) < self.population.size:
            # Select parents
            parent1, parent2 = self.population.select_parents(self.selection_method)

            # Crossover
            if random.random() < self.crossover_rate:
                if self.crossover_func:
                    child1, child2 = self.crossover_func(parent1, parent2)
                else:
                    child1, child2 = parent1.crossover(parent2)
            else:
                child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)

            # Mutation
            if self.mutation_func:
                child1 = child1.mutate(self.mutation_rate, self.mutation_func)
                child2 = child2.mutate(self.mutation_rate, self.mutation_func)
            else:
                child1 = child1.mutate(self.mutation_rate)
                child2 = child2.mutate(self.mutation_rate)

            new_individuals.append(child1)
            if len(new_individuals) < self.population.size:
                new_individuals.append(child2)

        # Replace population
        self.population.individuals = new_individuals[:self.population.size]
        self.population.generation += 1

    def run(self, generations: int, callback: Optional[Callable[[int, Population], None]] = None) -> Individual:
        """
        Run the genetic algorithm for specified generations
        Returns the best individual found
        """
        for gen in range(generations):
            self.evolve_generation()

            if callback:
                callback(gen, self.population)

        # Final evaluation
        self.population.evaluate_fitness()

        return self.population.best_individual

    def run_until_convergence(self, threshold: float, max_generations: int = 1000,
                             patience: int = 50) -> Individual:
        """
        Run until population converges or max generations reached
        Convergence: fitness improvement < threshold for 'patience' generations
        """
        best_fitness = float('-inf')
        generations_without_improvement = 0

        for gen in range(max_generations):
            self.evolve_generation()

            current_best = self.population.best_individual.fitness

            if current_best - best_fitness < threshold:
                generations_without_improvement += 1
            else:
                best_fitness = current_best
                generations_without_improvement = 0

            if generations_without_improvement >= patience:
                print(f"Converged at generation {gen}")
                break

        return self.population.best_individual

    def __repr__(self):
        return f"GeneticAlgorithm(pop={self.population.size}, mut={self.mutation_rate}, cross={self.crossover_rate})"
