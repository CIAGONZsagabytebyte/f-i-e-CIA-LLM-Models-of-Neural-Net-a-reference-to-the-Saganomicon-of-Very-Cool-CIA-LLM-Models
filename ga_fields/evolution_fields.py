"""
Evolution Fields - Field-based evolutionary operators

Implements mutation, crossover, and selection as field transformations
in the saga evolutionary space.
"""

import random
import math
from typing import Any, List, Callable, Tuple


class EvolutionField:
    """Base class for evolutionary field operations"""

    def __init__(self, name: str = "evolution_field"):
        self.name = name
        self.applications = 0
        self.history = []

    def apply(self, genome: List[Any]) -> List[Any]:
        """Apply the evolutionary field to a genome"""
        self.applications += 1
        result = self._apply_field(genome)
        self.history.append({
            'input': genome[:3],
            'output': result[:3],
            'generation': self.applications
        })
        return result

    def _apply_field(self, genome: List[Any]) -> List[Any]:
        """Override this in subclasses"""
        return genome

    def __call__(self, genome: List[Any]) -> List[Any]:
        return self.apply(genome)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, applications={self.applications})"


class MutationField(EvolutionField):
    """Field that applies mutations to genomes"""

    def __init__(self, name: str = "mutation", mutation_rate: float = 0.01,
                 mutation_strength: float = 1.0):
        super().__init__(name)
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

    def _apply_field(self, genome: List[Any]) -> List[Any]:
        """Apply mutation field"""
        mutated = []
        for gene in genome:
            if random.random() < self.mutation_rate:
                mutated.append(self._mutate_gene(gene))
            else:
                mutated.append(gene)
        return mutated

    def _mutate_gene(self, gene: Any) -> Any:
        """Mutate a single gene"""
        if isinstance(gene, (int, float)):
            return gene + random.gauss(0, self.mutation_strength)
        elif isinstance(gene, bool):
            return not gene
        elif isinstance(gene, str):
            if len(gene) > 0:
                idx = random.randint(0, len(gene) - 1)
                chars = list(gene)
                chars[idx] = random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
                return ''.join(chars)
        elif isinstance(gene, list):
            if len(gene) > 0:
                idx = random.randint(0, len(gene) - 1)
                gene_copy = gene.copy()
                gene_copy[idx] = self._mutate_gene(gene[idx])
                return gene_copy
        return gene

    def set_cosmic_resonance(self) -> 'MutationField':
        """Set mutation to follow cosmic resonance patterns"""
        self.mutation_strength = 1.618033988749  # Golden ratio
        return self

    def set_adaptive_rate(self, fitness: float, target_fitness: float) -> 'MutationField':
        """Adapt mutation rate based on fitness"""
        if target_fitness > 0:
            fitness_ratio = fitness / target_fitness
            self.mutation_rate = 0.1 * (1 - fitness_ratio)
        return self


class CrossoverField(EvolutionField):
    """Field that performs genetic crossover"""

    def __init__(self, name: str = "crossover", crossover_type: str = "single_point"):
        super().__init__(name)
        self.crossover_type = crossover_type

    def apply_pair(self, genome1: List[Any], genome2: List[Any]) -> Tuple[List[Any], List[Any]]:
        """Apply crossover to a pair of genomes"""
        self.applications += 1

        if self.crossover_type == "single_point":
            return self._single_point_crossover(genome1, genome2)
        elif self.crossover_type == "two_point":
            return self._two_point_crossover(genome1, genome2)
        elif self.crossover_type == "uniform":
            return self._uniform_crossover(genome1, genome2)
        elif self.crossover_type == "saga":
            return self._saga_crossover(genome1, genome2)
        else:
            return genome1.copy(), genome2.copy()

    def _single_point_crossover(self, genome1: List[Any], genome2: List[Any]) -> Tuple[List[Any], List[Any]]:
        """Single-point crossover"""
        if len(genome1) != len(genome2) or len(genome1) < 2:
            return genome1.copy(), genome2.copy()

        point = random.randint(1, len(genome1) - 1)
        child1 = genome1[:point] + genome2[point:]
        child2 = genome2[:point] + genome1[point:]

        return child1, child2

    def _two_point_crossover(self, genome1: List[Any], genome2: List[Any]) -> Tuple[List[Any], List[Any]]:
        """Two-point crossover"""
        if len(genome1) != len(genome2) or len(genome1) < 3:
            return genome1.copy(), genome2.copy()

        points = sorted(random.sample(range(1, len(genome1)), 2))
        p1, p2 = points

        child1 = genome1[:p1] + genome2[p1:p2] + genome1[p2:]
        child2 = genome2[:p1] + genome1[p1:p2] + genome2[p2:]

        return child1, child2

    def _uniform_crossover(self, genome1: List[Any], genome2: List[Any]) -> Tuple[List[Any], List[Any]]:
        """Uniform crossover (each gene randomly chosen from parent)"""
        if len(genome1) != len(genome2):
            return genome1.copy(), genome2.copy()

        child1 = []
        child2 = []

        for g1, g2 in zip(genome1, genome2):
            if random.random() < 0.5:
                child1.append(g1)
                child2.append(g2)
            else:
                child1.append(g2)
                child2.append(g1)

        return child1, child2

    def _saga_crossover(self, genome1: List[Any], genome2: List[Any]) -> Tuple[List[Any], List[Any]]:
        """
        Saga crossover: blend genomes using golden ratio
        For numeric genes: child = parent1 * phi + parent2 * (1-phi)
        """
        if len(genome1) != len(genome2):
            return genome1.copy(), genome2.copy()

        phi = 0.618033988749  # Golden ratio conjugate
        child1 = []
        child2 = []

        for g1, g2 in zip(genome1, genome2):
            if isinstance(g1, (int, float)) and isinstance(g2, (int, float)):
                child1.append(g1 * phi + g2 * (1 - phi))
                child2.append(g2 * phi + g1 * (1 - phi))
            else:
                # Fall back to random selection for non-numeric
                if random.random() < phi:
                    child1.append(g1)
                    child2.append(g2)
                else:
                    child1.append(g2)
                    child2.append(g1)

        return child1, child2


class SelectionField(EvolutionField):
    """Field that performs selection operations"""

    def __init__(self, name: str = "selection", method: str = "tournament"):
        super().__init__(name)
        self.method = method

    def select(self, population: List[Tuple[List[Any], float]], count: int = 1) -> List[List[Any]]:
        """
        Select individuals from population
        population: List of (genome, fitness) tuples
        """
        self.applications += 1

        if self.method == "tournament":
            return self._tournament_select(population, count)
        elif self.method == "roulette":
            return self._roulette_select(population, count)
        elif self.method == "rank":
            return self._rank_select(population, count)
        elif self.method == "cosmic":
            return self._cosmic_select(population, count)
        else:
            return [random.choice(population)[0] for _ in range(count)]

    def _tournament_select(self, population: List[Tuple[List[Any], float]],
                          count: int, tournament_size: int = 3) -> List[List[Any]]:
        """Tournament selection"""
        selected = []
        for _ in range(count):
            tournament = random.sample(population, min(tournament_size, len(population)))
            winner = max(tournament, key=lambda x: x[1])
            selected.append(winner[0])
        return selected

    def _roulette_select(self, population: List[Tuple[List[Any], float]],
                        count: int) -> List[List[Any]]:
        """Roulette wheel selection"""
        # Shift fitnesses to be positive
        min_fitness = min(f for _, f in population)
        adjusted_pop = [(g, f - min_fitness + 1) for g, f in population]

        total_fitness = sum(f for _, f in adjusted_pop)
        selected = []

        for _ in range(count):
            pick = random.uniform(0, total_fitness)
            current = 0
            for genome, fitness in adjusted_pop:
                current += fitness
                if current >= pick:
                    selected.append(genome)
                    break

        return selected

    def _rank_select(self, population: List[Tuple[List[Any], float]],
                    count: int) -> List[List[Any]]:
        """Rank-based selection"""
        sorted_pop = sorted(population, key=lambda x: x[1], reverse=True)
        ranks = list(range(len(sorted_pop), 0, -1))
        total_rank = sum(ranks)

        selected = []
        for _ in range(count):
            pick = random.uniform(0, total_rank)
            current = 0
            for (genome, _), rank in zip(sorted_pop, ranks):
                current += rank
                if current >= pick:
                    selected.append(genome)
                    break

        return selected

    def _cosmic_select(self, population: List[Tuple[List[Any], float]],
                      count: int) -> List[List[Any]]:
        """
        Cosmic selection: use harmonic series for selection probabilities
        Better individuals get selection probability proportional to 1/n
        where n is their rank (1st = 1/1, 2nd = 1/2, etc.)
        """
        sorted_pop = sorted(population, key=lambda x: x[1], reverse=True)

        # Harmonic series weights
        weights = [1.0 / (i + 1) for i in range(len(sorted_pop))]
        total_weight = sum(weights)

        selected = []
        for _ in range(count):
            pick = random.uniform(0, total_weight)
            current = 0
            for (genome, _), weight in zip(sorted_pop, weights):
                current += weight
                if current >= pick:
                    selected.append(genome)
                    break

        return selected


class AdaptiveEvolutionField(EvolutionField):
    """Evolution field that adapts its parameters based on population dynamics"""

    def __init__(self, name: str = "adaptive_evolution"):
        super().__init__(name)
        self.mutation_field = MutationField()
        self.crossover_field = CrossoverField()
        self.selection_field = SelectionField()

        self.diversity_threshold = 0.1
        self.convergence_threshold = 0.01

    def measure_diversity(self, population: List[List[Any]]) -> float:
        """Measure genetic diversity in population"""
        if not population or not population[0]:
            return 0.0

        # Calculate average pairwise distance
        total_distance = 0.0
        count = 0

        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                distance = self._genome_distance(population[i], population[j])
                total_distance += distance
                count += 1

        return total_distance / count if count > 0 else 0.0

    def _genome_distance(self, genome1: List[Any], genome2: List[Any]) -> float:
        """Calculate distance between two genomes"""
        if len(genome1) != len(genome2):
            return float('inf')

        distance = 0.0
        for g1, g2 in zip(genome1, genome2):
            if isinstance(g1, (int, float)) and isinstance(g2, (int, float)):
                distance += abs(g1 - g2)
            elif g1 != g2:
                distance += 1.0

        return distance / len(genome1)

    def adapt_parameters(self, diversity: float) -> None:
        """Adapt evolution parameters based on diversity"""
        if diversity < self.diversity_threshold:
            # Low diversity: increase mutation to explore
            self.mutation_field.mutation_rate = min(0.2, self.mutation_field.mutation_rate * 1.5)
            self.mutation_field.mutation_strength *= 1.5
        elif diversity > 0.5:
            # High diversity: decrease mutation to exploit
            self.mutation_field.mutation_rate = max(0.001, self.mutation_field.mutation_rate * 0.8)
            self.mutation_field.mutation_strength *= 0.8

    def __repr__(self):
        return f"AdaptiveEvolutionField(name={self.name}, mut_rate={self.mutation_field.mutation_rate:.4f})"
