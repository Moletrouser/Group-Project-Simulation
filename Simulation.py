import vpython as vp
from vpython import sphere, vector, color, rate, mag, canvas, box
import numpy as np
from sympy import *

canvas(width=2400, height=1400)  # slightly bigger than default, adjust if you have small screen.

dt = 0.01  # timestep
step = 1  # loop counter
maxStep = 20000*100000  # maximum number of steps
maxParticles = 20

box = box(pos=vector(0,0,0),length=60, height=60, width=60, opacity=0.2)


#  Define the star, planets and constants
M = 1000  # mass of star (in units where G = 1)
gasM = 1
initPos = vector(10, 0, 0)  # initial position vectors of Planets
centrePos = vector(0,0,0)
nanoParticle = sphere(pos=initPos, radius=1, color=color.blue, make_trail=True )  # defines the appearance of the planets
Centre = sphere(pos=centrePos, radius= 0.1, color=color.white)
nanoParticle.trail_color = color.white  # change the trail colour to white, or any colour you fancy

nanoVel = vector(-0.5, 0.1, -0.2)  # defines the starting velocity vectors of the planets
nanoVector = nanoParticle.pos
nanoVectorMag = mag(nanoVector)  # finds the magnitude of the respective position vectors

restForceDirection = (-1)*nanoVector/nanoVectorMag
restForceMag = mag(nanoVector)**2

i = 0

### Gas particle Generator ###
##while i <= maxParticles:


xPos = np.random.normal(10,3,1)
yPos = np.random.normal(10,3,1)
zPos = np.random.normal(10,3,1)
initGasPos = vector(xPos, yPos, zPos)


xVel = np.random.normal(5,0.5,1)
yVel = np.random.normal(5,0.5,1)
zVel = np.random.normal(5,0.5,1)
gasVel = vector(xVel, yVel, zVel)

gasParticle = sphere(pos=initGasPos, radius=0.5, color=color.yellow)
#gasParticle.trail_color = color.green

gasVector = gasParticle.pos
gasXPos = vp.dot(gasParticle.pos, vector(1,0,0))
gasYPos = vp.dot(gasParticle.pos, vector(0,1,0))
gasZPos = vp.dot(gasParticle.pos, vector(0,0,1))

nanoToGasVector = gasParticle.pos-nanoParticle.pos
nanoToGasDistance = mag(nanoToGasVector)

while step <= maxStep:

    nanoToGasVector = gasParticle.pos - nanoParticle.pos
    nanoToGasDistance = mag(nanoToGasVector)

    gasXPos = vp.dot(gasParticle.pos, vector(1, 0, 0))
    gasYPos = vp.dot(gasParticle.pos, vector(0, 1, 0))
    gasZPos = vp.dot(gasParticle.pos, vector(0, 0, 1))

    nanoMomentum = mag(nanoVel)*M
    gasMomentum = mag(gasVel)*gasM

    restForceDirection = (-1) * nanoVector / nanoVectorMag
    restForceMag = mag(nanoVector) ** 2

    nanoVel = nanoVel + dt*restForceMag*restForceDirection/M
    nanoVector = nanoVector + nanoVel * dt  # defines the new postion vectors of each planet after the velocity change
    nanoParticle.pos = nanoVector  # tells python to set the sphere locations to the new position vectors
    nanoVectorMag = mag(nanoVector)
    restForceDirection = (-1) * nanoVector / nanoVectorMag

    gasVector = gasVector + gasVel * dt
    gasParticle.pos = gasVector

    if abs(gasVector.x) >= 30:
        gasVel.x = -gasVel.x
    if abs(gasVector.y) >= 30:
        gasVel.y = -gasVel.y
    if abs(gasVector.z) >= 30:
        gasVel.z = -gasVel.z

    #if nanoToGasDistance<(nanoParticle.radius + gasParticle.radius): #### re do collision code

    step = step + 1
    rate(1200)

