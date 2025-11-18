import numpy as np
import argparse
import os
parser = argparse.ArgumentParser(description='2D Ising Model Simulation')
parser.add_argument('-L', '--latticeSize', help='Size of the lattice (LxL)', type=int, default=10)
parser.add_argument('-J', '--interactionStrength', help='Interaction strength (J)', type=float, default=1.0)
parser.add_argument('-kT', '--temperature', help='Temperature (kT)', type=float, default=1.0)
parser.add_argument('-N', '--numSteps', help='Number of Monte Carlo steps', type=int, default=1000)
parser.add_argument('-D', '--spinDensity', help='Initial spin density', type=float, default=0.5)
parser.add_argument('-B', '--magneticField', help='Magnetic field (B)', type=float, default=0.0)

parser.add_argument('-oI', '--outputImage', help='Output image file name', type=str)
parser.add_argument('-oA', '--outputAnimation', help='Output animation file name', type=str)
parser.add_argument('-oF', '--outputFile', help='Output data file name', type=str)

simArgs = parser.parse_args()

latticeSize = simArgs.latticeSize
J = simArgs.interactionStrength
kT = simArgs.temperature
B = simArgs.magneticField
numSteps = simArgs.numSteps
spinDensity = simArgs.spinDensity


class IsingModel:
    def __init__(self, L, J, kT, B, spinDensity):
        self.L = L
        self.J = J
        self.kT = kT
        self.B = B
        self.spinDensity = spinDensity
        self.lattice = self.initializeLattice()
        self.M = self.lattice.sum()*1.0 / (self.L**2)

    
    def initializeLattice(self):
        lattice = np.random.choice([-1, 1], size=(self.L, self.L), p=[1 - self.spinDensity, self.spinDensity])
        return lattice
    
    def calculateEnergy(self):
        energy = 0
        for i in range(self.L):
            for j in range(self.L):
                dE = self.lattice[(i+1)%self.L, j] + self.lattice[i, (j+1)%self.L] + self.lattice[(i-1)%self.L, j] + self.lattice[i, (j-1)%self.L]
                energy += -self.J  * dE * self.lattice[i,j] - self.B * self.lattice[i,j]
        return energy / 2
    
    def spinFlip(self, i, j):
        dE = 2 * self.calculateEnergy()
        if dE < 0 or np.random.rand() < np.exp(-dE / self.kT):
            self.lattice[i, j] *= -1
            self.M = self.lattice.sum()*1.0 / (self.L**2)


isingSim = IsingModel(latticeSize, J, kT, B, spinDensity)

outputAnimationCheck = False
outputImageCheck = False        
outputFileCheck = False

if simArgs.outputImage != None:
    imgFile = open=(simArgs.outputImage,'w')
    outputImageCheck = True
if simArgs.outputAnimation != None:
    AnimFile = open=(simArgs.outputAnimation,'w')
    outputAnimationCheck = True
if simArgs.outputFile != None:
    outputFile = open(simArgs.outputFile,'w')
    outputFile.write(isingSim.M.__str__() + '\n')
    outputFileCheck = True

#Dodać zapisanie obrazów


for step in range(numSteps):
    i = np.random.randint(0, latticeSize)
    j = np.random.randint(0, latticeSize)
    isingSim.spinFlip(i, j)
    if outputFileCheck:
        outputFile.write(isingSim.M.__str__() + '\n')
    







testL = np.random.choice([-1, 1], size=(4, 4), p=[1 - spinDensity, spinDensity])
print(testL)
print(testL.sum())

# print(testL[0,0])
# print(testL[0,-1])
# print(testL[-1,-1])
# print(testL[-1,0])