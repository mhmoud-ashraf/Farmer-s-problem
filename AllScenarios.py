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
S = [1, 2, 3] # Scenarios 1: optimistic, 2: expected, 3: pessimistic
q = {1: [3, 3.6, 24], 2: [2.5, 3, 20], 3: [2, 2.4, 16]} # Yield for each crop in each scenario
p = [150, 230, 260] # Planting cost
#%%
# Sets and indices
I = range(1, len(Crop)+1)
J = range(1, len(d)+1)
K = range(1, len(r)+1)
#%%
# Create a new model
model = gp.Model("AllScenarios")
#%%
# Create variables
x = model.addVars(I, name="x")
y = model.addVars(S, J, name="y")
w = model.addVars(S, K, name="w")
#%%
# Set objective
model.setObjective((1/3)*gp.quicksum(r[k-1] * w[s,k] for k in K for s in S) - gp.quicksum(p[i-1] * x[i] for i in I) - (1/3)*gp.quicksum(c[j-1] * y[s,j] for j in J for s in S), GRB.MAXIMIZE)
    
#%%
# Add constraints
model.addConstr((gp.quicksum(x[i] for i in I) <= A), name="Land")
model.addConstrs((q[s][j-1] * x[j] + y[s,j] - w[s,j] >= d[j-1] for j in J for s in S), name="demand")
model.addConstrs((q[s][3-1] * x[3] - w[s,3] - w[s,4] >= 0 for s in S), name="sugar beet")
model.addConstrs((w[s,3] <= T for s in S), name="sugar beet quota")
#%%
# Optimize the model
model.optimize()
#%%
# Print the optimal solution
for v in model.getVars():
    print('%s %g' % (v.varName, v.x))
print('Obj: %g' % model.objVal)