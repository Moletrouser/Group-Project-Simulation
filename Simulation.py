import vpython as vp
from vpython import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
#from pynput import keyboard


xPosData = []
yPosData = []
zPosData = []
timeData = []
count = 0
canvas(width=2400, height=1400)  # slightly bigger than default, adjust if you have small screen.

dt = 0.0002  # timestep
maxParticles = 20 ## not implemented yet, to be used in prospective loop to create N gas particles

box = box(pos=vector(0,0,0),length=100, height=100, width=100, opacity=0.2) ## sets the size of the box

## values for the nano particle mass, M, the gas particle mass, and SF6/C60 masses in kg
nanoM = 1e-18
gasM = 5.46e-26
alphaM = 6.644e-27
sf6M =  2.425e-25
c60M = 1.197e-24

T = 293
kB = 1.38e-23
P_gas = 1e-11
nanoR = 199e-9
rho = 1850

## marks the centre where potential is zero for reference
centrePos = vector(0,0,0)
Centre = sphere(pos=centrePos, radius= 0.1, color=color.white)

## takes randoms values from a normal dist. for the nano particle starting position (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxPos = np.random.normal(10,0.05,1)
nanoyPos = np.random.normal(10,0.05,1)
nanozPos = np.random.normal(10,0.05,1)
initNanoPos = vector(nanoxPos, nanoyPos, nanozPos)

## takes randoms values from a normal dist. for the nano particle velocity (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxVel = np.random.normal(0.01,0.002,1)
nanoyVel = np.random.normal(0.01,0.002,1)
nanozVel = np.random.normal(0.01,0.002,1)
nanoVel = vector(nanoxVel, nanoyVel, nanozVel)

## creates the nano particle with values defined above
nanoParticle = sphere(pos=initNanoPos, radius=1, color=color.blue, make_trail=True, retain = 100, interval=10 )
nanoParticle.trail_color = color.white  # change the trail colour to white, or any colour you fancy
nanoVector = nanoParticle.pos
nanoVectorMag = mag(nanoVector)

## creates a set of orthogonal arrows and labels to mark the co-ordinate axis
xArrow = arrow(pos=vector(box.length/2+10,0,0), axis=vector(15,0,0), shaftwidth=1, color=color.blue)
xLabel= label( pos=vec(box.length/2+20,0,0), text='x', color=color.blue)
yArrow = arrow(pos=vector(box.width/2+10,0,0), axis=vector(0,15,0), shaftwidth=1, color=color.green)
yLabel= label( pos=vec(box.width/2+20,20,0), text='y', color=color.green)
zArrow = arrow(pos=vector(box.height/2+10,0,0), axis=vector(0,0,15), shaftwidth=1, color=color.red)
zLabel= label( pos=vec(box.height/2+20,0,20), text='z', color=color.red)

graphpos = graph(x=2000, y=2000, width=1000, height=500, title='Position Vs Time', xtitle='time', ytitle='Position',
                 foreground=color.black, background=color.black)
graphVel = graph(x=2000, y=2000, width=1000, height=500, title='Velocity Vs Time', xtitle='time', ytitle='Velocity',
                 foreground=color.black, background=color.black)
graphKE = graph(x=2000, y=2000, width=1000, height=500, title='KE Vs Time', xtitle='time', ytitle='KE',
                 foreground=color.black, background=color.black)

x_pos = gcurve(graph=graphpos, color=color.red, label='x position')
y_pos = gcurve(graph=graphpos, color=color.blue, label='y position')
z_pos = gcurve(graph=graphpos, color=color.green, label='z position')

x_vel = gcurve(graph=graphVel, color=color.red, label='x velocity')
y_vel = gcurve(graph=graphVel, color=color.blue, label='y velocity')
z_vel = gcurve(graph=graphVel, color=color.green, label='z velocity')

c = (8*kB*T/gasM/pi)**0.5 #Partcle mean speed
b = ((1 + pi/8)*c*P_gas*gasM)/(kB*T*nanoR*rho) #gas damping term

b = 90# experimenting with larger b term

## the entire simulation takes place within this while loop
while True:

    ## sets the magnitude of the restoration force on each axis
    restForceMagX = 377*abs(nanoVector.x)*nanoM + b*abs(nanoVel.x)*nanoM
    restForceMagY = 753*abs(nanoVector.y)*nanoM + b*abs(nanoVel.y)*nanoM
    restForceMagZ = 942*abs(nanoVector.z)*nanoM + b*abs(nanoVel.z)*nanoM
    
    
    ## checks the position of the particle to decide in what direction the restoring force should act
    if nanoVector.x > 0:
        nanoVel.x = nanoVel.x - dt * restForceMagX / nanoM
    else:
        nanoVel.x = nanoVel.x + dt * restForceMagX / nanoM

    if nanoVector.y > 0:
        nanoVel.y = nanoVel.y - dt * restForceMagY / nanoM
    else:
        nanoVel.y = nanoVel.y + dt * restForceMagY / nanoM

    if nanoVector.z > 0:
        nanoVel.z = nanoVel.z - dt * restForceMagZ / nanoM
    else:
        nanoVel.z = nanoVel.z + dt * restForceMagZ / nanoM


    ## checks if the nano particle has collided with the walls of the container, reverses the velocity if so
    if nanoVector.x - nanoParticle.radius >= box.length / 2:
        if nanoVel.x > 0:
            nanoVel.x = -nanoVel.x
    if nanoVector.x + nanoParticle.radius <= -box.length / 2:
        if nanoVel.x < 0:
            nanoVel.x = -nanoVel.x

    if nanoVector.y - nanoParticle.radius >= box.width / 2:
        if nanoVel.y > 0:
            nanoVel.y = -nanoVel.y
    if nanoVector.y + nanoParticle.radius <= -box.length / 2:
        if nanoVel.y < 0:
            nanoVel.y = -nanoVel.y

    if nanoVector.z - nanoParticle.radius >= box.height / 2:
        if nanoVel.z > 0:
            nanoVel.z = -nanoVel.z
    if nanoVector.z + nanoParticle.radius <= -box.length / 2:
        if gasVel.z < 0:
            nanoVel.z = -nanoVel.z


    ## simulates gas particle collisions, place holder
    if np.random.randint(0,6001)>5999: ## rolls a random number to decide if collision has occured

         sign1 = (-1) ** np.random.randint(1, 3) ## decides the sign of the momentum contribution on each axis
         sign2 = (-1) ** np.random.randint(1, 3)
         sign3 = (-1) ** np.random.randint(1, 3)

         impulseX = sign1 * np.random.normal(5e-5, 2e-6, 1)
         impulseY = sign2 * np.random.normal(5e-5, 2e-6, 1)
         impulseZ = sign3 * np.random.normal(5e-5, 2e-6, 1)

         nanoVel.x =+ impulseX ## adds an impulse to the velocity on each axis
         nanoVel.y =+ impulseY
         nanoVel.z =+ impulseZ 


    ## simulates SF6/C60/alpha collisions. Delete as appropriate, needs refining
    if np.random.randint(0,9001)>8999: ## rolls a random number to decide if collision has occured
        #Impulse = 0.1*(3e8)*alphaM      ## Alpha particle
        Impulse = 0.1 * (3e8) * c60M  ## C60 particle
        #Impulse = 0.001 * (3e8) * sf6M  ## SF6 particle

        nanoMomentum = nanoVel.x*nanoM + Impulse
        nanoVel.x += nanoMomentum/nanoM

    nanoVector.x = nanoVector.x + nanoVel.x * dt + dt * dt * restForceMagX/(2*nanoM)
    nanoVector.y = nanoVector.y + nanoVel.y * dt + dt * dt * restForceMagY/(2*nanoM)
    nanoVector.z = nanoVector.z + nanoVel.z * dt + dt * dt * restForceMagZ/(2*nanoM)
    
    nanoParticle.pos = nanoVector  # sets the new nanoParticle position to the updated postion vecotr
    nanoVectorMag = mag(nanoVector)

    count = count + dt
    timeData.append(count)

    x_pos.plot(pos=(count, nanoVector.x))
    y_pos.plot(pos=(count, nanoVector.y))
    z_pos.plot(pos=(count, nanoVector.z))

    x_vel.plot(pos=(count, nanoVel.x))
    y_vel.plot(pos=(count, nanoVel.y))
    z_vel.plot(pos=(count, nanoVel.z))
            

    rate(800) ## sets the animation rate


