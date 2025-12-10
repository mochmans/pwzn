import numpy as np
import argparse
import os
from PIL import Image, ImageDraw
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import time

import numba

parser = argparse.ArgumentParser(description='Ising Model Simulation')
parser.add_argument('-L', '--latticeSize', help='Size of the lattice (LxL)', type=int, default=50)
parser.add_argument('-J', '--interactionStrength', help='Interaction strength (J)', type=float, default=1.0)
parser.add_argument('-Be', '--beta', help='Inverse temperature (beta)', type=float, default=0.5)
parser.add_argument('-N', '--numSteps', help='Number of Monte Carlo steps', type=int, default=100)
parser.add_argument('-D', '--spinDensity', help='Initial spin density', type=float, default=0.5)
parser.add_argument('-B', '--magneticField', help='Magnetic field (B)', type=float, default=0.0)

parser.add_argument('-I', '--outputImage', help='Output image file name', type=str)
parser.add_argument('-A', '--outputAnimation', help='Output animation file name', type=str, default='ising_simulation')
parser.add_argument('-F', '--outputFile', help='Output data file name', type=str)

simArgs = parser.parse_args()

latticeSize = simArgs.latticeSize
J = simArgs.interactionStrength
beta = simArgs.beta
B = simArgs.magneticField
numSteps = simArgs.numSteps
spinDensity = simArgs.spinDensity





@numba.njit
def calculateEnergy(lattice, latticeSize, i, j):
        energy = 0
        dE = lattice[(i+1)%latticeSize, j] + lattice[i, (j+1)%latticeSize] + lattice[(i-1)%latticeSize, j] + lattice[i, (j-1)%latticeSize]
        energy += -J  * dE * lattice[i,j] - B * lattice[i,j]
        return energy

@numba.njit
def spinFlip(lattice, L, beta, i, j, M):
        dE = -2 * calculateEnergy(lattice, L, i, j)

        if dE < 0 or np.random.rand() < np.exp(-dE * beta):   
            
            lattice[i, j] *= -1   

            M = lattice.sum()*1.0 / (L**2)


lattice = np.random.choice([-1, 1], size=(latticeSize, latticeSize), p=[1 - spinDensity, spinDensity])
M = lattice.sum()*1.0 / (latticeSize**2)


fig, ax = plt.subplots()
im = ax.imshow(lattice, animated=True, cmap='gray')
def update(frame):
    im.set_array(frame)
    return [im]

frames = []


outputAnimationCheck = False
outputImageCheck = False        
outputFileCheck = False

if simArgs.outputFile != None:
    outputFile = open(simArgs.outputFile+'.txt','w')
    outputFile.write(M.__str__() + '\n')
    outputFileCheck = True
if simArgs.outputAnimation != None:
    outputAnimationCheck = True
if simArgs.outputImage != None:
    outputImageCheck = True


def saveLattice(latticeSize, lattice, imgFile=None):
    image = Image.new('RGB', (1000, 1000), 'pink')
    draw = ImageDraw.Draw(image)
    draw.rectangle([200, 200, 400, 400], outline='blue', width=5)
    for i in range(latticeSize):
        for j in range(latticeSize):
            color = 'green' if lattice[i,j] == 1 else 'black'
            draw.rectangle([i*1000/latticeSize, j*1000/latticeSize, (i+1)*1000/latticeSize, (j+1)*1000/latticeSize], fill=color)
    if imgFile:
        image.save(imgFile)

def isingSimulation(lattice, numSteps,latticeSize, beta):
    start = time.perf_counter()
    for macrostep in range(numSteps):
        for microStep in range(latticeSize**2):
            i = np.random.randint(0, latticeSize)
            j = np.random.randint(0, latticeSize)
            spinFlip(lattice, latticeSize, beta, i, j, M) 
        frames.append(lattice.copy())  
        if outputFileCheck:
            outputFile.write(M.__str__() + '\n')
    
        if outputImageCheck: 
            if simArgs.outputImage[-3:] == 'png':
                filename = simArgs.outputImage[:-4] + '_step_' + (macrostep.__str__() + '.png')
            elif simArgs.outputImage[-3:] == 'jpg':
                filename = simArgs.outputImage[:-4] + '_step_' + (macrostep.__str__() + '.png')
            elif simArgs.outputImage[-4:] == 'jpeg':
                filename = simArgs.outputImage[:-5] + '_step_' + (macrostep.__str__() + '.png')
            else:
                filename = simArgs.outputImage + '_step_' + (macrostep.__str__() + '.png')
            saveLattice(latticeSize, lattice, imgFile=filename)

        if outputAnimationCheck:
            if simArgs.outputAnimation[:-3] != 'gif':
                animFile = simArgs.outputAnimation + 'numba.gif'
            else:
                animFile = simArgs.outputAnimation

    end = time.perf_counter()
    print(f"Simulation time: {end - start} seconds")
    ani = FuncAnimation(fig, update, frames=frames, interval=200, blit=True)
    ani.save(animFile)
    plt.show()

    
    
    



isingSimulation(lattice, numSteps, latticeSize, beta)




        


        