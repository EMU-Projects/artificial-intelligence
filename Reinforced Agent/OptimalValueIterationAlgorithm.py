# -*- coding: utf-8 -*-
"""
Created on Fri May 21 09:35:40 2021

@author: ACAN
"""
# Value Iteration Algorithm
import numpy as np

# Algorithm Parameters
Conv_Diff = 1.0e-6 # If sum of absolute differences between
                  # V(s) values of two successive iterations 
                  # is less than this STOP.
GAMMA = 0.5       # Disocunt factor

# Let's consider the a grid of NxM dimensions
# Each cell corresponds to a state, Let's initialize teh states
N=10
M=10

#Define and initialize all states
States=[]
for i in range(N):
    for j in range(M):
            States.append((i,j))  
            
ObstacleStates=[(6,2),(7,2),(6,4),(6,5),(3,6)]   
TerminalStates=[(3,3),(9,0),(5,8)] 
        
#Define Actions
Actions={}
for s in States:
    if s not in ObstacleStates and s not in TerminalStates:
        Actions[s]=[]
        if s==(0,0):
            if (0,1) not in ObstacleStates:
                Actions[s].append('R')
            if (1,0) not in ObstacleStates:
                Actions[s].append('D')
        elif s==(0,M-1):
            if (0,M-2) not in ObstacleStates:
                Actions[s].append('L')
            if (1,M-1) not in ObstacleStates:
                Actions[s].append('D')
        elif s==(N-1,0):
            if (N-2,0) not in ObstacleStates:
                Actions[s].append('U')
            if (N-1,1) not in ObstacleStates:
                Actions[s].append('R')                
        elif s==(N-1,M-1):
            if (N-2,M-1) not in ObstacleStates:
                Actions[s].append('U')
            if (N-1,M-2) not in ObstacleStates:
                Actions[s].append('L')                
        elif s[0]==0:
            if (0,s[1]+1) not in ObstacleStates:
                Actions[s].append('R')
            if (0,s[1]-1) not in ObstacleStates:
                Actions[s].append('L')
            if (1,s[1]) not in ObstacleStates:
                Actions[s].append('D')
        elif s[0]==N-1:
            if (0,s[1]+1) not in ObstacleStates:
                Actions[s].append('R')
            if (0,s[1]-1) not in ObstacleStates:
                Actions[s].append('L')
            if (N-2,s[1]) not in ObstacleStates:
                Actions[s].append('U')
        elif s[1]==0:
            if (s[0],1) not in ObstacleStates:
                Actions[s].append('R')
            if (s[0]-1,0) not in ObstacleStates:
                Actions[s].append('U')
            if (s[0]+1,0) not in ObstacleStates:
                Actions[s].append('D')
        elif s[1]==M-1:
            if (s[0],M-2) not in ObstacleStates:
                Actions[s].append('L')
            if (s[0]-1,M-1) not in ObstacleStates:
                Actions[s].append('U')
            if (s[0]+1,M-2) not in ObstacleStates:
                Actions[s].append('D')
        else:
            if (s[0],s[1]-1) not in ObstacleStates:
                Actions[s].append('L')
            if (s[0],s[1]+1) not in ObstacleStates:
                Actions[s].append('R')
            if (s[0]-1,s[1]) not in ObstacleStates:
                Actions[s].append('U')
            if (s[0]+1,s[1]) not in ObstacleStates:
                Actions[s].append('D')

# Define Rewards for States
Rewards={}
for s in Actions.keys():
    ActionsList=Actions[s]
    for a in ActionsList:
        Rewards[(s,a)] = +1
Rewards[(2,3),'D'] = +10
Rewards[(3,2),'R'] = +10
Rewards[(4,3),'U'] = +10
Rewards[(3,4),'L'] = +10
Rewards[(4,8),'D'] = +10
Rewards[(5,7),'R'] = +10
Rewards[(6,8),'U'] = +10
Rewards[(5,9),'L'] = +10
Rewards[(8,9),'D'] = +10
Rewards[(9,1),'L'] = +10

Rewards[(2,2),'D'] = +5
Rewards[(1,3),'D'] = +5
Rewards[(2,4),'D'] = +5
Rewards[(4,7),'D'] = +5
Rewards[(4,8),'D'] = +5
Rewards[(4,9),'D'] = +5
Rewards[(7,0),'D'] = +5
Rewards[(8,1),'D'] = +5

Rewards[(4,2),'U'] = +5
Rewards[(5,3),'U'] = +5
Rewards[(4,4),'U'] = +5
Rewards[(6,7),'U'] = +5
Rewards[(7,8),'U'] = +5
Rewards[(6,9),'U'] = +5

Rewards[(2,4),'L'] = +5
Rewards[(3,5),'L'] = +5
Rewards[(4,4),'L'] = +5
Rewards[(4,9),'L'] = +5
Rewards[(6,9),'L'] = +5
Rewards[(8,1),'L'] = +5
Rewards[(9,2),'L'] = +5

Rewards[(2,2),'R'] = +5
Rewards[(3,1),'R'] = +5
Rewards[(4,2),'R'] = +5
Rewards[(4,7),'R'] = +5
Rewards[(5,6),'R'] = +5
Rewards[(6,7),'R'] = +5

         
# Define state transition probabilities uniformly
StateTransitionProbs={}
for s in Actions.keys(): # Transitions are not defined for all states
    ActionsList=Actions[s]
    for a in ActionsList:
        if a == 'U':
            NextState = (s[0]-1, s[1])
            StateTransitionProbs[(s,a)]={NextState:1.0} 
            # probability of moving into the
            # next state after taking action a
        if a == 'D':
            NextState = (s[0]+1, s[1])
            StateTransitionProbs[(s,a)]={NextState:1.0} 
            # probability of moving into the
            # next state after taking action a
        if a == 'L':
            NextState = (s[0], s[1]-1)
            StateTransitionProbs[(s,a)]={NextState:1.0} 
            # probability of moving into the
            # next state after taking action a
        if a == 'R':
            NextState = (s[0], s[1]+1)
            StateTransitionProbs[(s,a)]={NextState:1.0} 
            # probability of moving into the
            # next state after taking action a
        
# Define an initial uniformly random policy
Policy={}
for s in Actions.keys(): # Actions are not defined for all states
    Policy[s] = np.random.choice(Actions[s])

for s in Policy:
    print(s,":",Policy[s])    
print()

# Define and initialize the State-Value Matrix
V={}
for i in States:
    V[i]=0


# VALUE ITERATION
Iteration = 0
Termination_Cond=False
while not Termination_Cond:
    Max_Change = 0
    Old_V=dict(V)
    for s in States:            
        if s in Policy:            
            New_V=-np.inf            
            for a in Actions[s]:                
                for NextState in StateTransitionProbs[(s,a)]:
                    NextStateTransProb=StateTransitionProbs[(s,a)][NextState]                                
                    Temp = NextStateTransProb*(Rewards[s,a]+GAMMA*V[NextState])
                    if Temp > New_V:
                        New_V=Temp
                        Policy[s]=a
            V[s]=New_V
    
    Iteration += 1
    print("ITERATION :",Iteration)
    for s in Policy:
        print(s,":",Policy[s])    
    print()

    
    for s in V.keys():
        Max_Change=max(Max_Change,abs(Old_V[s]-V[s]))
    
    if Max_Change <= Conv_Diff:
        Termination_Cond=True

# Print V Values of the grid world
V_Grid=np.zeros((N,M))

for s in States:
    RowIndex=s[0]
    ColIndex=s[1]
    V_Grid[RowIndex,ColIndex]=V[s]

for i in range(N):
    for j in range(M):
        if V_Grid[i,j] >=0:
            print("{0}{1:.2f}{2}".format('|+',V_Grid[i,j],'|'),end='')
        else:
            print("{0}{1:.2f}{2}".format('|',V_Grid[i,j],'|'),end='')
    print()
    
# COMPUTING Q(s,a) Values
# Remember that Q_pi(s,a)=SumOverNextStates(TransProb(s,s',a)*(Rewards(s,s',a)+Gamma*V_Pi(S')))    

# Iniatilize Q(S,a) dictionary
# Define and initialize the State-Action Value Matrix
Q={}
for s in Actions.keys():
    ActionsList=Actions[s]
    for a in ActionsList:
        Q[(s,a)]=0

for s in States:            
    if s not in ObstacleStates and s not in TerminalStates:            
        ActionsList=Actions[s]
        for a in ActionsList:
            SumOverNextStates=0
            for NextState in StateTransitionProbs[(s,a)]:
                NextStateTransProb=StateTransitionProbs[(s,a)][NextState]
                SumOverNextStates += NextStateTransProb*(Rewards[s,a]+GAMMA*V[NextState])
            Q[s,a]=SumOverNextStates

# Print Q(s,a) Values of the grid world
Q_Matrix={} # There are 4 actions {L,R,U,D}
for State_Action in Q:
    if State_Action[0] not  in Q_Matrix:
        Q_Matrix[State_Action[0]]={State_Action[1]:Q[State_Action]}
    else:
        Q_Matrix[State_Action[0]].update({State_Action[1]:Q[State_Action]})

for s in Q_Matrix.keys():
    print(s,":",end='')
    for a in Q_Matrix[s]:        
        if Q_Matrix[s][a] >=0:            
            print("{0}{1}{2:.2f}{3}".format(a,":+",Q_Matrix[s][a],'|'),end='')
        else:
            print("{0}{1}{2:.2f}{3}".format(a,":",Q_Matrix[s][a],'|'),end='')
    print()
