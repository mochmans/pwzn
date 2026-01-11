import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import numba

S0 = 999  # Initial susceptible population
I0 = 1     # Initial infected population
R0 = 0     # Initial recovered population
beta = 0.3  # Infection rate
gamma = 0.2  # Recovery rate
N = S0 + I0 + R0

@numba.njit
def sirModel(y, t, beta, gamma, N):
    S, I, R = y
    dSdT = -beta/N * I * S
    dIdT = (beta/N * I * S) - (gamma*I)
    dRdT = gamma*I
    return [dSdT, dIdT, dRdT]



t = np.linspace(0,200,100)

y0 = [S0, I0, R0]

solution = odeint(sirModel, y0, t, args=(beta, gamma, N))
S, I, R = solution.T

plt.figure(figsize=(7, 4), dpi=300)
plt.plot(t, S, lw=2, label='$S(t)$')
plt.plot(t, I, lw=2, label='$I(t)$')
plt.plot(t, R, lw=2, label='$R(t)$')
plt.savefig('logistic_growth_model.png')
plt.savefig('logistic_growth_model.pdf')