import vpython as vp
from vpython import *
import numpy as np
import random
from sympy import *

canvas(width=2400, height=1400)  # slightly bigger than default, adjust if you have small screen.

dt = 0.0001  # timestep
maxParticles = 20 ## not implemented yet, to be used in prospective loop to create N gas particles

box = box(pos=vector(0,0,0),length=120, height=120, width=120, opacity=0.2) ## sets the size of the box

## values for the nano particle mass, M, and the gas mass, gasM. Not to scale, PLACEHOLDER VALUES
M = 1e-18
gasM = 5.46e-26

## marks the centre where potential is zero for reference
centrePos = vector(0,0,0)
Centre = sphere(pos=centrePos, radius= 0.1, color=color.white)

## takes randoms values from a normal dist. for the nano particle starting position (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxPos = np.random.normal(10,5,1)
nanoyPos = np.random.normal(10,5,1)
nanozPos = np.random.normal(10,5,1)
initNanoPos = vector(nanoxPos, nanoyPos, nanozPos)

## takes randoms values from a normal dist. for the nano particle velocity (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxVel = np.random.normal(1,0.2,1)
nanoyVel = np.random.normal(1,0.2,1)
nanozVel = np.random.normal(1,0.2,1)
nanoVel = vector(nanoxVel, nanoyVel, nanozVel)

## creates the nano particle with values defined above
nanoParticle = sphere(pos=initNanoPos, radius=1, color=color.blue, make_trail=True, retain = 50 )
nanoParticle.trail_color = color.white  # change the trail colour to white, or any colour you fancy
nanoVector = nanoParticle.pos
nanoVectorMag = mag(nanoVector)

## picks a random value for each co-ordinate of the gas particles starting location within the box
gasxPos = (-box.length/2)+np.random.random()*box.length
gasyPos = (-box.width/2)+np.random.random()*box.width
gaszPos = (-box.height/2)+np.random.random()*box.height
initGasPos = vector(gasxPos, gasyPos, gaszPos)

## takes randoms values from a normal dist. for the gas velocity (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
gasxVel = np.random.normal(1000,25,1)
gasyVel = np.random.normal(1000,25,1)
gaszVel = np.random.normal(1000,25,1)
gasVel = vector(gasxVel, gasyVel, gaszVel)

## creates the gas particle with values defined above
gasParticle = sphere(pos=initGasPos, radius=0.5, color=color.yellow)

## creates a set of orthogonal arrows and labels to mark the co-ordinate axis
xArrow = arrow(pos=vector(box.length/2+10,0,0), axis=vector(15,0,0), shaftwidth=1, color=color.blue)
xLabel= label( pos=vec(box.length/2+20,0,0), text='x', color=color.blue)
yArrow = arrow(pos=vector(box.width/2+10,0,0), axis=vector(0,15,0), shaftwidth=1, color=color.green)
yLabel= label( pos=vec(box.width/2+20,20,0), text='y', color=color.green)
zArrow = arrow(pos=vector(box.height/2+10,0,0), axis=vector(0,0,15), shaftwidth=1, color=color.red)
zLabel= label( pos=vec(box.height/2+20,0,20), text='z', color=color.red)

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
    if gasVector.x - gasParticle.radius >= box.length/2:
        if gasVel.x > 0:
            gasVel.x = -gasVel.x
    if gasVector.x + gasParticle.radius <= -box.length/2:
        if gasVel.x < 0:
            gasVel.x = -gasVel.x

    if gasVector.y - gasParticle.radius >= box.width/2:
        if gasVel.y > 0:
            gasVel.y = -gasVel.y
    if gasVector.y + gasParticle.radius <= -box.length / 2:
        if gasVel.y < 0:
            gasVel.y = -gasVel.y

    if gasVector.z - gasParticle.radius >= box.height/2:
        if gasVel.z > 0:
            gasVel.z = -gasVel.z
    if gasVector.z + gasParticle.radius <= -box.length / 2:
        if gasVel.z < 0:
            gasVel.z = -gasVel.z

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



    ## condition to be met if collision has occurred

    ## if nanoToGasDistance <= (nanoParticle.radius + gasParticle.radius):
    if nanoToGasDistance <= 7:

        vecX = nanoParticle.pos - gasParticle.pos
        norm(vecX)

        vecV1 = nanoVel
        x1 = vecX.dot(vecV1)
        vecV1x = vecX * x1
        vecV1y = vecV1 - vecV1x
        m1 = M

        vecX = vecX*(-1)
        vecV2 = gasVel
        x2 = vecX.dot(vecV2)
        vecV2x = vecX * x2
        vecV2y = vecV2 - vecV2x
        m2 = gasM

        nanoVel = vecV1x * (m1 - m2)/(m1 + m2) + vecV2x * (2 * m2)/(m1 + m2) + vecV1y
        gasVel = vecV1x * (2 * m1) / (m1 + m2) + vecV2x * (m2 - m1) / (m1 + m2) + vecV2y



    rate(1200) ## sets the animation rate

