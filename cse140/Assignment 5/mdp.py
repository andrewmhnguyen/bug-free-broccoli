import numpy as np
import mdptoolbox


P = [[[1,0,0],[.8,.2,0],[1,0,0]],[[.2,.8,0],[0,1,0],[0,0,1]],[[.5,.5,0],[0,0,1],[0,0,1]]]
R = [[[20,0,0],[40,30,0],[100,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[-10,-10,0],[0,0,-10],[0,0,0]]]
pi = mdptoolbox.mdp.PolicyIteration(P, R, 0.86)
pi2 = mdptoolbox.mdp.ValueIteration(P, R, 0.86)
pi.run()
pi2.run()
print(pi.policy)
print(pi.iter)
print(pi2.policy)
print(pi2.iter)