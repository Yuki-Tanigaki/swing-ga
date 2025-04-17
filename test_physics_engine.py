from physics_engine import SwingSimulator

sim = SwingSimulator(visualize=True)

# 例：単純なsin波モーション（約600フレーム）
control_sequence = [(math.sin(i * 0.1) * 2, math.cos(i * 0.1) * 2) for i in range(600)]

fitness = sim.simulate(control_sequence)
print("Fitness:", fitness)
