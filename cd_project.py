# -*- coding: utf-8 -*-
"""CD_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15YQjc1SYaKcIsSKGx69MQFxWwhTCppLm
"""

#Logistic
import numpy as np
import matplotlib.pyplot as plt
kr=100
ks=100

rr=0.5 # effective replication rate resistant cells
rs=0.5 # (effective) replication rate sensitive cells
Wrs=0.1 # switching rate resistant --> sensitive
Wsr=0.1 # switching rate sensitive --> resistant
d=0 # death rate sensitive cells 
# d=0 for normal cancer progression
# d>rs for chemotherapy so that effective replication rate < 0
h=1 # step / increment

# Commented out IPython magic to ensure Python compatibility.
# Time dynamics and phase space
import matplotlib.pyplot as plt
# show plots in notebook
# % matplotlib inline

# define system in terms of separated differential equations
def f(Cr,Cs):
    return rr*Cr*(1-(Cr+Cs)/kr)-Wrs*Cr+Wsr*Cs
def g(Cr,Cs):
    return rs*Cs*(1-(Cs+Cr)/ks)-Wsr*Cs+Wrs*Cr-d*Cs

# initialize lists containing values
x = []
y = []

#iv1, iv2 = initial values, dt = timestep, time = range
def sys(iv1, iv2, dt, time):
    # initial values:
    x.append(iv1)
    y.append(iv2)
    # compute and fill lists
    for i in range(time):
        x.append(x[i] + (f(x[i],y[i])) * dt)
        y.append(y[i] + (g(x[i],y[i])) * dt)
    return x, y

sys(10, 10, 0.1, 500)

#plot
fig = plt.figure(figsize=(15,5))
fig.subplots_adjust(wspace = 0.5, hspace = 0.3)
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.plot(x, 'r-', label='Cr')
ax1.plot(y, 'b-', label='Cs')
#ax1.plot(z, 'g-', label='prey')
#ax1.set_title("Dynamics in time")
ax1.set_xlabel("time")
ax1.grid()
ax1.legend(loc='best')

ax2.plot(x, y, color="blue")
ax2.set_xlabel("Cr")
ax2.set_ylabel("Cs")  
#ax2.set_title("Phase space")
ax2.grid()

# Fix points
fp = []

def find_fixed_points(r):
    for x in range(r):
        for y in range(r):
            if ((f(x,y) == 0) and (g(x,y) == 0)):
                fp.append((x,y))
    return fp

fp=find_fixed_points(100)

#Nullclines
fig2 = plt.figure(figsize=(8,6))
ax4 = fig2.add_subplot(1,1,1)
h=0.5
Cr=np.arange(-100,100,h)

Cs1=Cr*(Wrs+rr*Cr/kr-rr)/(Wsr-rr*Cr/kr) # Cr

A=-rs/ks
B=rs-rs*Cr/ks-Wsr-d
C=Wrs*Cr
Cs2plus= (-B+np.sqrt(B**2-4*A*C))/(2*A) #Cs
Cs2minus= (-B-np.sqrt(B**2-4*A*C))/(2*A)

# plot nullclines
ax4.plot(Cr,Cs1, 'r-', lw=2, label='Cr-nullcline')
ax4.plot(Cr,Cs2plus, 'b-', lw=2,label='Cs plus-nullcline')
ax4.plot(Cr,Cs2minus, 'g-', lw=2, label='Cs minus-nullcline')
ax4.set_xlim(-20,100)
ax4.set_ylim(-20,100)

# plot fixed points
for point in fp:
    ax4.plot(point[0],point[1],"red", marker = "o", markersize = 10.0)
#ax4.set_title("Quiverplot with nullclines")
ax4.set_xlabel("Cr")
ax4.set_ylabel("Cs")  
ax4.legend(loc='best')

# quiverplot
# define a grid and compute direction at each point
xm = np.linspace(-100, 100, 20)
ym = np.linspace(-100, 200, 20)

X1 , Y1  = np.meshgrid(xm, ym)                    # create a grid

DX1=f(X1,Y1)
DY1=g(X1,Y1)
M = (np.hypot(DX1, DY1))                        # norm growth rate 
M[ M == 0] = 1.                                 # avoid zero division errors 
DX1 /= M                                        # normalize each arrows
DY1 /= M                                       # normalize each arrows


ax4.quiver(X1, Y1, DX1, DY1, M, pivot='mid')
#ax4.plot(x, y, '--',lw=2,color="orange",label='Trajectory IC=(10,10)')
ax4.legend()
ax4.grid()

