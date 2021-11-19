import numpy as np
import mdptoolbox

P = [[[1,0,0],[.8,.2,0],[1,0,0]],[[.2,.8,0],[0,1,0],[0,0,1]],[[.5,.5,0],[0,0,1],[0,0,1]]]
R = [[[20,0,0],[40,30,0],[100,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[-10,-10,0],[0,0,-10],[0,0,0]]]
P = np.array(P)
R = np.array(R)
pi = mdptoolbox.mdp.PolicyIteration(P, R, 0.86)
pi.run()
print(pi.policy)
print(pi.iter)

