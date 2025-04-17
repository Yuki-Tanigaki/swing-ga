# from ga_engine import GAEngine
# from physics_engine import SwingSimulator

# ga = GAEngine(population_size=20, gene_length=600, mutation_rate=0.1, generations=10)
# best_gene, best_fitness = ga.run()

# # 可視化（再生）
# sim = SwingSimulator(visualize=True)
# sim.simulate(best_gene)

from ga_engine import GAEngine
from visualize import visualize_gene
import pickle

def main():
    # パラメータは必要に応じて変えてOK
    ga = GAEngine(
        population_size=20,
        gene_length=600,         # 約10秒間のモーション（60fps × 10）
        mutation_rate=0.1,
        generations=15
    )

    # 進化の実行
    best_gene, best_fitness = ga.run()

    # 保存（あとで再生したい用）
    with open("best_gene.pkl", "wb") as f:
        pickle.dump(best_gene, f)

    print("\n=== Visualizing Best Gene ===")
    visualize_gene(best_gene)

if __name__ == "__main__":
    main()
