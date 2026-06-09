import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

x = ctrl.Antecedent(np.arange(0, 10, 1), 'x')
y = ctrl.Consequent(np.arange(0, 10, 1), 'y')

x['low'] = fuzz.trimf(x.universe, [0, 0, 5])
y['low'] = fuzz.trimf(y.universe, [0, 0, 5])

rule = ctrl.Rule(x['low'], y['low'])
ctrl_sys = ctrl.ControlSystem([rule])
sim = ctrl.ControlSystemSimulation(ctrl_sys)

sim.input['x'] = 2
sim.compute()
print("Before update:", sim.output['y'])

# Update MF
x['low'] = fuzz.trimf(x.universe, [0, 5, 10])

# Need to check if re-computing uses the new MF
sim.input['x'] = 2
sim.compute()
print("After update (same sim):", sim.output['y'])

# Check if rebuilding is necessary
rule2 = ctrl.Rule(x['low'], y['low'])
ctrl_sys2 = ctrl.ControlSystem([rule2])
sim2 = ctrl.ControlSystemSimulation(ctrl_sys2)
sim2.input['x'] = 2
sim2.compute()
print("After update (new sim):", sim2.output['y'])
