#Project 1 by Zoe Hackshaw

import numpy as np
from numpy import random
from numpy.random import randint #allows us to assign a random integer
from numpy import empty #allows us to an empty numpy array
import matplotlib.pyplot as plt

nfloors=100 #number of floors
npeople=10 #number of people

#now, starting with only accepting positive swaps
def mag(r):
    return np.sqrt(r[0]**2. + r[1]**2.)

def distance(N,r):
    s = 0. #distance traveled
    for i in range(N):
        s = s+mag(r[i+1] - r[i])
    return s

r = empty([npeople+1,2],float) #creating an empty array for the people 
for i in range(npeople): #this loop assigns random floors to random people
    r[i,0] = np.random.randint(nfloors) #the floor they start on
    r[i,1] = np.random.randint(nfloors) #the floor they are going to

dsaved=[]
D=distance(npeople,r) #calculating original distance

for m in range(10000): #this is going to repeat as many times as necessary for answer to converge
    i=np.random.randint(npeople)
    j=np.random.randint(npeople)
    while i==j: #incase the same floor is picked twice
        i=np.random.randint(npeople)
        j=np.random.randint(npeople)
    oldD=D
    r[i,0],r[j,0] = r[j,0],r[i,0] #these two lines are what is responsible for the swap
    r[i,1],r[j,1] = r[j,1],r[i,1]
    D=distance(npeople,r)#calculating change in distance
    delta=D-oldD#difference in floors, if a good swap, this should be negative
    if delta>0:#swapping it back if its a bad swap
        r[i,0],r[j,0] = r[j,0],r[i,0]
        r[i,1],r[j,1] = r[j,1],r[i,1]
        D=distance(npeople,r)
        dsaved.append(D)
    else:
        D=distance(npeople,r)
        dsaved.append(D)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.arange(len(dsaved)),dsaved)
ax.set_xscale('log')



#now, with annealing
Tmax = 10 #degrees
Tmin = 1e-3 #degrees
tau = 1.e4
T = Tmax
t = 0 #time

dsaved_anneal=[]
D = distance(npeople,r) #calculates the distance between people

while T >Tmin:

    t = t+1
    T = Tmax * np.exp(-t/tau) #this is to cool

    i = np.random.randint(npeople) #picking random people
    j = np.random.randint(npeople)
    while i == j: #to ensure the same floor is not picked twice
        i = np.random.randint(npeople)
        j = np.random.randint(npeople)
    oldD = D
    r[i,0],r[j,0] = r[j,0],r[i,0] #this swaps the floors
    r[i,1],r[j,1] = r[j,1],r[i,1]
    D = distance(npeople,r) #calculates new distance
    deltaD = D - oldD  #difference in distances, negative if good
    
    if deltaD > 0: #if positive it is a bad swap
        if np.random.random() > np.exp(-deltaD/T): #where the annealing takes place, sometimes accepting bad swaps
            r[i,0],r[j,0] = r[j,0],r[i,0]
            r[i,1],r[j,1] = r[j,1],r[i,1]
        D = distance(npeople,r)
        dsaved_anneal.append(D)
    else:
        D = distance(npeople,r)
        dsaved_anneal.append(D)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.arange(len(dsaved_anneal)),dsaved_anneal)
ax.set_xscale('log')
