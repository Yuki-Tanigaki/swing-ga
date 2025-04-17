# ga_engine.py

import random
import math
from physics_engine import SwingSimulator

class GAEngine:
    def __init__(self, population_size=20, gene_length=600, mutation_rate=0.1, generations=20):
        self.population_size = population_size
        self.gene_length = gene_length
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []

    def _random_gene(self):
        # 各関節のモータースピードを [-3, 3] の範囲で初期化
        return [(random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(self.gene_length)]

    def _mutate_gene(self, gene):
        mutated = []
        for j1, j2 in gene:
            if random.random() < self.mutation_rate:
                j1 += random.uniform(-1, 1)
                j1 = max(min(j1, 5), -5)
            if random.random() < self.mutation_rate:
                j2 += random.uniform(-1, 1)
                j2 = max(min(j2, 5), -5)
            mutated.append((j1, j2))
        return mutated

    def _crossover(self, gene1, gene2):
        # 一点交叉
        point = random.randint(0, self.gene_length - 1)
        return gene1[:point] + gene2[point:]

    def run(self):
        # 初期集団生成
        self.population = [self._random_gene() for _ in range(self.population_size)]
        best_gene = None
        best_fitness = -float('inf')

        for gen in range(self.generations):
            print(f"\n=== Generation {gen+1} ===")
            fitness_scores = []
            for i, gene in enumerate(self.population):
                sim = SwingSimulator(visualize=False)
                fitness = sim.simulate(gene)
                fitness_scores.append((fitness, gene))
                print(f"Individual {i}: Fitness = {fitness:.3f}")

                # ベスト更新
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_gene = gene

            # ソート＆選択（上位50%残す）
            fitness_scores.sort(reverse=True, key=lambda x: x[0])
            survivors = [gene for (_, gene) in fitness_scores[:self.population_size // 2]]

            # 次世代生成
            next_gen = survivors.copy()
            while len(next_gen) < self.population_size:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)
                child = self._crossover(parent1, parent2)
                child = self._mutate_gene(child)
                next_gen.append(child)

            self.population = next_gen

        print(f"\n=== Evolution Complete ===")
        print(f"Best Fitness: {best_fitness:.3f}")
        return best_gene, best_fitness
