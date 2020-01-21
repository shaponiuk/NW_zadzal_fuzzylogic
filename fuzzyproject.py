import numpy as np
import skfuzzy as fuzz
from skfuzzy import control

people = control.Antecedent(np.arange(0, 300, 1), 'people')
tech_supplies = control.Antecedent(np.arange(0, 500, 1), 'tech_supplies')
skill = control.Antecedent(np.arange(0, 100, 1), 'skill')
productivity = control.Consequent(np.arange(0, 100, 1), 'productivity')
cost = control.Consequent(np.arange(0, 100, 1), 'cost')
tech_supplies_demand = control.Consequent(np.arange(0, 100, 1), 'tech_supplies_demand')

tech_supplies.automf(3)
skill.automf(3)
productivity.automf(3)
cost.automf(5)
people.automf(3)
tech_supplies_demand.automf(3)

tech_supplies_demand_rule_1 = control.Rule(tech_supplies['poor'] & people['average'],
                                           tech_supplies_demand['average'])
tech_supplies_demand_rule_2 = control.Rule(tech_supplies['average'] & people['good'],
                                           tech_supplies_demand['average'])
tech_supplies_demand_rule_3 = control.Rule(tech_supplies['poor'] & people['good'],
                                           tech_supplies_demand['good'])
tech_supplies_demand_rule_4 = control.Rule(tech_supplies['good'],
                                           tech_supplies_demand['poor'])
tech_supplies_demand_rule_5 = control.Rule(tech_supplies['average'] & people['average'],
                                           tech_supplies_demand['poor'])
tech_supplies_demand_rule_6 = control.Rule(people['poor'],
                                           tech_supplies_demand['poor'])

cost_rule_1 = control.Rule(tech_supplies_demand['good'] & (people['good'] | skill['good']),
                           cost['good'])
cost_rule_2 = control.Rule((people['average'] & skill['good'])
                           | (people['good'] & skill['average']),
                           cost['decent'])
cost_rule_3 = control.Rule((people['good'] & skill['poor'])
                           | (people['poor'] & skill['good'])
                           | people['average'] & skill['average'],
                           cost['average'])
cost_rule_4 = control.Rule((people['poor'] & skill['average'])
                           | (people['average'] & skill['poor']),
                           cost['mediocre'])
cost_rule_5 = control.Rule(people['poor'] & skill['poor'],
                           cost['poor'])

productivity_rule_1 = control.Rule(skill['good'], productivity['good'])
productivity_rule_2 = control.Rule(skill['average']
                                   | (skill['poor'] & people['good']),
                                   productivity['average'])
productivity_rule_3 = control.Rule(skill['poor'] & (people['poor'] | people['average']),
                                   productivity['poor'])

def test_case(inputs):
    ctrl = control.ControlSystem([tech_supplies_demand_rule_1,
                                  tech_supplies_demand_rule_2,
                                  tech_supplies_demand_rule_3,
                                  tech_supplies_demand_rule_4,
                                  tech_supplies_demand_rule_5,
                                  tech_supplies_demand_rule_6,
                                  cost_rule_1,
                                  cost_rule_2,
                                  cost_rule_3,
                                  cost_rule_4,
                                  cost_rule_5,
                                  productivity_rule_1,
                                  productivity_rule_2,
                                  productivity_rule_3])

    ctrl_sim = control.ControlSystemSimulation(ctrl)

    ctrl_sim.input['tech_supplies'] = inputs[0]
    ctrl_sim.input['people'] = inputs[1]
    ctrl_sim.input['skill'] = inputs[2]

    ctrl_sim.compute()

    tech_supplies_demand.view(sim=ctrl_sim)
    cost.view(sim=ctrl_sim)
    productivity.view(sim=ctrl_sim)

test_case([100, 150, 80])
test_case([0, 0, 0])
test_case([3, 30, 100])
test_case([0, 300, 0])