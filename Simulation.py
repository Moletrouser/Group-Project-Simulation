import vpython as vp
from vpython import *
import numpy as np
from sympy import *

canvas(width=2400, height=1400)  # slightly bigger than default, adjust if you have small screen.

dt = 0.0001  # timestep
maxParticles = 20 ## not implemented yet, to be used in prospective loop to create N gas particles

box = box(pos=vector(0,0,0),length=60, height=60, width=60, opacity=0.2) ## sets the size of the box

## values for the nano particle mass, M, and the gas mass, gasM. Not to scale, PLACEHOLDER VALUES
M = 1
gasM = 0.001

## marks the centre where potential is zero for reference
centrePos = vector(0,0,0)
Centre = sphere(pos=centrePos, radius= 0.1, color=color.white)

## takes randoms values from a normal dist. for the nano particle starting position (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxPos = np.random.normal(10,5,1)
nanoyPos = np.random.normal(10,5,1)
nanozPos = np.random.normal(10,5,1)
initNanoPos = vector(nanoxPos, nanoyPos, nanozPos)

## takes randoms values from a normal dist. for the nano particle velocity (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxVel = np.random.normal(3,1,1)
nanoyVel = np.random.normal(3,1,1)
nanozVel = np.random.normal(3,1,1)
nanoVel = vector(nanoxVel, nanoyVel, nanozVel)

## creates the nano particle with values defined above
nanoParticle = sphere(pos=initNanoPos, radius=1, color=color.blue, make_trail=True, retain = 50 )
nanoParticle.trail_color = color.white  # change the trail colour to white, or any colour you fancy
nanoVector = nanoParticle.pos
nanoVectorMag = mag(nanoVector)

## picks a random integer value for each co-ordinate of the gas particles starting location within the box
gasxPos = np.random.randint(-box.length/2, box.length/2)
gasyPos = np.random.normal(-box.width/2, box.width/2)
gaszPos = np.random.normal(-box.height/2,box.height/2)
initGasPos = vector(gasxPos, gasyPos, gaszPos)

## takes randoms values from a normal dist. for the gas velocity (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
gasxVel = np.random.normal(250,25,1)
gasyVel = np.random.normal(250,25,1)
gaszVel = np.random.normal(250,25,1)
gasVel = vector(gasxVel, gasyVel, gaszVel)

## creates the gas particle with values defined above
gasParticle = sphere(pos=initGasPos, radius=0.5, color=color.yellow)

## creates a set of orthogonal arrows and labels to mark the co-ordinate axis
xArrow = arrow(pos=vector(40,0,0), axis=vector(15,0,0), shaftwidth=1, color=color.blue)
xLabel= label( pos=vec(60,0,0), text='x', color=color.blue)
yArrow = arrow(pos=vector(40,0,0), axis=vector(0,15,0), shaftwidth=1, color=color.green)
yLabel= label( pos=vec(40,20,0), text='y', color=color.green)
zArrow = arrow(pos=vector(40,0,0), axis=vector(0,0,15), shaftwidth=1, color=color.red)
zLabel= label( pos=vec(40,0,20), text='z', color=color.red)

## the entire simulation takes place within this while loop
while True:

    ## calculates the distance between the centres of the gas and nano particles
    nanoToGasVector = gasParticle.pos - nanoParticle.pos
    nanoToGasDistance = mag(nanoToGasVector)

    ## this is an unneccesary way of calcuating the postion vector of the gas particle
    ## can just be replaced with gasVector.x, gasVector.y etc
    gasXPos = vp.dot(gasParticle.pos, vector(1, 0, 0))
    gasYPos = vp.dot(gasParticle.pos, vector(0, 1, 0))
    gasZPos = vp.dot(gasParticle.pos, vector(0, 0, 1))
    gasVector = gasParticle.pos

    ## calculates the momentum of the gas and nano particle for use in collision calculations
    ## not currently used
    nanoMomentum = mag(nanoVel)*M
    gasMomentum = mag(gasVel)*gasM

    ## sets the magnitude of the restoration force on each axis
    restForceMagX = 377*abs(nanoVector.x)*M
    restForceMagY = 753*abs(nanoVector.y)*M
    restForceMagZ = 942*abs(nanoVector.z)*M

    ## checks the position of the particle to decide in what direction the restoring force should act
    if nanoVector.x > 0:
        nanoVel.x = nanoVel.x - dt * restForceMagX / M
    else:
        nanoVel.x = nanoVel.x + dt * restForceMagX / M

    if nanoVector.y > 0:
        nanoVel.y = nanoVel.y - dt * restForceMagY / M
    else:
        nanoVel.y = nanoVel.y + dt * restForceMagY / M

    if nanoVector.z > 0:
        nanoVel.z = nanoVel.z - dt * restForceMagZ / M
    else:
        nanoVel.z = nanoVel.z + dt * restForceMagZ / M

    nanoVector = nanoVector + nanoVel * dt  # defines the new position vector of the nano particle
    nanoParticle.pos = nanoVector  # sets the new nanoParticle position to the updated postion vecotr
    nanoVectorMag = mag(nanoVector)

    gasVector = gasVector + gasVel * dt  # defines the new position vector of the gas particle
    gasParticle.pos = gasVector # sets the new gas Particle position to the updated position vector

    ## checks if the gas particle has collided with the walls of the container, reverses the velocity if so
    if abs(gasVector.x) + gasParticle.radius >= box.length/2:
        gasVel.x = -gasVel.x
    if abs(gasVector.y) + gasParticle.radius >= box.width/2:
        gasVel.y = -gasVel.y
    if abs(gasVector.z) + gasParticle.radius >= box.height/2:
        gasVel.z = -gasVel.z

    ## box.size/2
    ## +(gasParticle.size/2)

    ## condition to be met if collision has occurred
    ## needs to be finished
    #if nanoToGasDistance<(nanoParticle.radius + gasParticle.radius):

    rate(1200) ## sets the animation rate

