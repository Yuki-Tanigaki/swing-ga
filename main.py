from ga_engine import GAEngine
from physics_engine import SwingSimulator

ga = GAEngine(population_size=20, gene_length=600, mutation_rate=0.1, generations=10)
best_gene, best_fitness = ga.run()

# 可視化（再生）
sim = SwingSimulator(visualize=True)
sim.simulate(best_gene)
