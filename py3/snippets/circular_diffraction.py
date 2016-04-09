# Source: http://central.scipy.org/item/73/2/circular-diffraction

# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
import numpy as np
from scipy.special import j1
import matplotlib.pyplot as plt

wave = 500e-9
k = 2*np.pi/wave
side = 1e-6
points = 200
dim = np.linspace(-side/2,side/2,points)
ax,ay = np.meshgrid(dim,dim)
r = np.sqrt(ax**2 + ay**2)
area = (j1(k*r)/(k*r))**2
plt.imshow(area, cmap='viridis');
# hot()
plt.show();

