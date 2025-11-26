import numpy as np
import argparse
import os
from PIL import Image, ImageDraw
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

from IPython.display import HTML

parser = argparse.ArgumentParser(description='Ising Model Simulation')
parser.add_argument('-L', '--latticeSize', help='Size of the lattice (LxL)', type=int, default=50)
parser.add_argument('-J', '--interactionStrength', help='Interaction strength (J)', type=float, default=1.0)
parser.add_argument('-Be', '--beta', help='Inverse temperature (beta)', type=float, default=0.5)
parser.add_argument('-N', '--numSteps', help='Number of Monte Carlo steps', type=int, default=100)
parser.add_argument('-D', '--spinDensity', help='Initial spin density', type=float, default=0.5)
parser.add_argument('-B', '--magneticField', help='Magnetic field (B)', type=float, default=0.0)

parser.add_argument('-I', '--outputImage', help='Output image file name', type=str)
parser.add_argument('-A', '--outputAnimation', help='Output animation file name', type=str)
parser.add_argument('-F', '--outputFile', help='Output data file name', type=str)

simArgs = parser.parse_args()

latticeSize = simArgs.latticeSize
J = simArgs.interactionStrength
beta = simArgs.beta
B = simArgs.magneticField
numSteps = simArgs.numSteps
spinDensity = simArgs.spinDensity


class IsingModel:
    def __init__(self, L, J, beta, B, spinDensity):
        self.L = L
        self.J = J
        self.beta = beta
        self.B = B
        self.spinDensity = spinDensity
        self.lattice = self.initializeLattice()
        self.M = self.lattice.sum()*1.0 / (self.L**2)

    
    def initializeLattice(self):
        lattice = np.random.choice([-1, 1], size=(self.L, self.L), p=[1 - self.spinDensity, self.spinDensity])
        return lattice
    
    def calculateEnergy(self, i, j):
        energy = 0
        dE = self.lattice[(i+1)%self.L, j] + self.lattice[i, (j+1)%self.L] + self.lattice[(i-1)%self.L, j] + self.lattice[i, (j-1)%self.L]
        energy += -self.J  * dE * self.lattice[i,j] - self.B * self.lattice[i,j]
        return energy
    
    def spinFlip(self, i, j):
        dE = -2 * self.calculateEnergy(i, j)

        if dE < 0 or np.random.rand() < np.exp(-dE * self.beta):   
            
            self.lattice[i, j] *= -1   

            self.M = self.lattice.sum()*1.0 / (self.L**2)

    def saveLattice(self,imgFile=None):
        image = Image.new('RGB', (1000, 1000), 'pink')
        draw = ImageDraw.Draw(image)
        draw.rectangle([200, 200, 400, 400], outline='blue', width=5)
        for i in range(self.L):
            for j in range(self.L):
                color = 'green' if self.lattice[i,j] == 1 else 'black'
                draw.rectangle([i*1000/self.L, j*1000/self.L, (i+1)*1000/self.L, (j+1)*1000/self.L], fill=color)
        if imgFile:
            image.save(imgFile)


isingSim = IsingModel(latticeSize, J, beta, B, spinDensity)

outputAnimationCheck = False
outputImageCheck = False        
outputFileCheck = False


fig, ax = plt.subplots()
im = ax.imshow(isingSim.lattice, animated=True, cmap='gray')
def update(frame):
    im.set_array(frame)
    return [im]

frames = []


if simArgs.outputFile != None:
    outputFile = open(simArgs.outputFile+'.txt','w')
    outputFile.write(isingSim.M.__str__() + '\n')
    outputFileCheck = True
if simArgs.outputAnimation != None:
    outputAnimationCheck = True
if simArgs.outputImage != None:
    outputImageCheck = True

for step in range(numSteps*(latticeSize**2)):
    i = np.random.randint(0, latticeSize)
    j = np.random.randint(0, latticeSize)
    isingSim.spinFlip(i, j)
    if outputFileCheck:
        outputFile.write(isingSim.M.__str__() + '\n')
    if outputImageCheck: 
        if step % (latticeSize**2) == 0:
            if simArgs.outputImage[-3:] == 'png':
                filename = simArgs.outputImage[:-4] + '_step_' + (step/latticeSize**2).__str__() + '.png'
            elif simArgs.outputImage[-3:] == 'jpg':
                filename = simArgs.outputImage[:-4] + '_step_' + (step/latticeSize**2).__str__() + '.png'
            elif simArgs.outputImage[-4:] == 'jpeg':
                filename = simArgs.outputImage[:-5] + '_step_' + (step/latticeSize**2).__str__() + '.png'
            else:
                filename = simArgs.outputImage + '_step_' + (step/latticeSize**2).__str__() + '.png'
            isingSim.saveLattice(imgFile=filename)
    if outputAnimationCheck:
        if step % (latticeSize**2) == 0:
            frames.append(isingSim.lattice.copy())  

if simArgs.outputAnimation != None:
    if simArgs.outputAnimation[:-3] != 'gif':
        animFile = simArgs.outputAnimation + '.gif'
    else:
        animFile = simArgs.outputAnimation

if outputAnimationCheck:
    ani = FuncAnimation(fig, update, frames=frames, interval=200, blit=True)
    ani.save(animFile)
    plt.show()
            

        


        