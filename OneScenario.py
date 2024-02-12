import gurobipy as gp
from gurobipy import GRB
#%%
# Input data
A = 500 # Land area
Crop = ['Wheat', 'Corn', 'Sugar beet'] # Crops
d = [200, 240] # Demand
r = [170, 150, 36, 10]  # Selling price
T = 6000 # Sugar beet production quota
c = [238, 210] # Purchase price
S = {1: 'optimistic', 2: 'expected', 3: 'pessimistic'} # Scenarios
q = {1: [3, 3.6, 24], 2: [2.5, 3, 20], 3: [2, 2.4, 16]} # Yield for each crop in each scenario
p = [150, 230, 260] # Planting cost
#%%
# Sets and indices
I = range(1, len(Crop)+1)
J = range(1, len(d)+1)
K = range(1, len(r)+1)
#%%
# Pick a scenario
s = 3
#%%
# Create a new model
model = gp.Model("OneScenario")
#%%
# Create variables
x = model.addVars(I, name="x")
y = model.addVars(J, name="y")
w = model.addVars(K, name="z")
#%%
# Set objective
model.setObjective(gp.quicksum(r[k-1] * w[k] for k in K) - gp.quicksum(p[i-1] * x[i] for i in I) - gp.quicksum(c[j-1] * y[j] for j in J), GRB.MAXIMIZE)
    
#%%
# Add constraints
model.addConstr((gp.quicksum(x[i] for i in I) <= A), name="Land")
model.addConstrs((q[s][j-1] * x[j] + y[j] - w[j] >= d[j-1] for j in J), name="demand")
model.addConstr((q[s][3-1] * x[3] - w[3] - w[4] >= 0), name="sugar beet")
model.addConstr((w[3] <= T), name="sugar beet quota")
#%%
# Optimize the model
model.optimize()
#%%
# Print the optimal solution
print('Scenario', S[s])
for v in model.getVars():
    print('%s %g' % (v.varName, v.x))
print('Obj: %g' % model.objVal)