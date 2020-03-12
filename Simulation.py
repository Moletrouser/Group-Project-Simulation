from vpython import *
import numpy as np

xPosData = []
yPosData = []
zPosData = []
timeData = []
count = 0
canvas(width=2400, height=1400)  # slightly bigger than default, adjust if you have small screen.

dt = 10e-8 # timestep

box = box(pos=vector(0,0,0),length=5000, height=5000, width=5000, opacity=0.1) ## sets the size of the box

## values for the nano particle mass, M, the gas particle mass, and SF6/C60 masses in kg
nanoM = 1e-18
gasM = 5.46e-26
alphaM = 6.644e-27
sf6M =  2.425e-25
c60M = 1.197e-24

T = 293
kB = 1.38e-23
P_gas = 5e-3
nanoR = 199e-9
rho = 1850

## marks the centre where potential is zero for reference
centrePos = vector(0,0,0)
Centre = sphere(pos=centrePos, radius= 5, color=color.white)

## takes randoms values from a normal dist. for the nano particle starting position (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxPos = np.random.normal(500,50,1)
nanoyPos = np.random.normal(500,50,1)
nanozPos = np.random.normal(500,50,1)
initNanoPos = vector(nanoxPos, nanoyPos, nanozPos)

## takes randoms values from a normal dist. for the nano particle velocity (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
nanoxVel = np.random.normal(1,0.2,1)
nanoyVel = np.random.normal(1,0.2,1)
nanozVel = np.random.normal(1,0.2,1)
nanoVel = vector(nanoxVel, nanoyVel, nanozVel)

## creates the nano particle with values defined above
nanoParticle = sphere(pos=initNanoPos, radius=10, color=color.blue, make_trail=True, retain = 50, interval=1 )
nanoParticle.trail_color = color.white  # change the trail colour to white, or any colour you fancy
nanoVector = nanoParticle.pos
nanoVectorMag = mag(nanoVector)

## creates a set of orthogonal arrows and labels to mark the co-ordinate axis
xArrow = arrow(pos=vector(box.length/2+0.1*box.length,0,0), axis=vector(0.15*box.length,0,0), shaftwidth=10, color=color.red)
xLabel= label( pos=vec(box.length/2+0.1*box.length + 1.1*xArrow.length,0,0), text='x', color=color.red)
yArrow = arrow(pos=vector(box.width/2+0.1*box.length,0,0), axis=vector(0,0.15*box.length,0), shaftwidth=10, color=color.blue)
yLabel= label( pos=vec(box.width/2+0.1*box.length,1.1*yArrow.length,0), text='y', color=color.blue)
zArrow = arrow(pos=vector(box.height/2+0.1*box.length,0,0), axis=vector(0,0,0.15*box.length), shaftwidth=10, color=color.green)
zLabel= label( pos=vec(box.height/2+0.1*box.length,0,1.1*zArrow.length), text='z', color=color.green)

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

c = (8*kB*T/gasM/pi)**0.5 #Particle mean speed
b = ((1 + pi/8)*c*P_gas*gasM)/(kB*T*nanoR*rho) #gas damping term

b = ((1 + pi/8)*c*P_gas*gasM)/(kB*T*nanoR*rho) #gas damping term

gasMomentum = c*gasM

thermalX = 8*10e11
thermalY = 8*10e11
thermalZ = 8*10e11

## the entire simulation takes place within this while loop
while True:

    ## sets the magnitude of the restoration force on each axis
    restForceMagX = (1.42e-7)*abs(nanoVector.x)  #- 1*10e-20 #- b*abs(nanoVel.x) #- 1*10e-25
    dampingForceMagX = (9*10e-15) * abs(nanoVel.x)

    restForceMagY = (5.68e-7)*abs(nanoVector.y)  #- 1*10e-20 #- b*abs(nanoVel.y) #- 1*10e-25
    dampingForceMagY = (9*10e-15) * abs(nanoVel.y)

    restForceMagZ = (8.88e-7)*abs(nanoVector.z)  #- 1*10e-20 #- b*abs(nanoVel.z) #- 1*10e-25
    dampingForceMagZ = (9*10e-15) * abs(nanoVel.z)

    ## checks the position of the particle to decide in what direction the restoring force/ thermal energy input should act
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

    ## checks the velocity of the particle to decide in what direction the damping force should act
    if nanoVel.x > 0:
        nanoVel.x = nanoVel.x - dt * dampingForceMagX / nanoM + dt*thermalX
    else:
        nanoVel.x = nanoVel.x + dt * dampingForceMagX / nanoM - dt*thermalX

    if nanoVel.y > 0:
        nanoVel.y = nanoVel.y - dt * dampingForceMagY / nanoM + dt*thermalY
    else:
        nanoVel.y = nanoVel.y + dt * dampingForceMagY / nanoM - dt*thermalY

    if nanoVel.z > 0:
        nanoVel.z = nanoVel.z - dt * dampingForceMagZ / nanoM + dt*thermalZ
    else:
        nanoVel.z = nanoVel.z + dt * dampingForceMagZ / nanoM - dt*thermalZ


    ## simulates gas particle collisions, place holder
    if np.random.randint(0,1001)>990: ## rolls a random number to decide if collision has occured

         sign1 = (-1) ** np.random.randint(1, 3)  ## decides the sign of the momentum contribution on each axis
         sign2 = (-1) ** np.random.randint(1, 3)  ## decides the sign of the momentum contribution on each axis
         sign3 = (-1) ** np.random.randint(1, 3)  ## decides the sign of the momentum contribution on each axis

         rand1 = np.random.randint(0,100)
         rand2 = np.random.randint(0,100)
         rand3 = np.random.randint(0,100)

         xPortion = sign1 * gasMomentum * rand1/(rand1+rand2+rand3)
         yPortion = sign2 * gasMomentum * rand2/(rand1+rand2+rand3)
         zPortion = sign3 * gasMomentum * rand3/(rand1+rand2+rand3)

         nanoXMomentum = nanoVel.x * nanoM + xPortion
         nanoYMomentum = nanoVel.y * nanoM + yPortion
         nanoZMomentum = nanoVel.z * nanoM + zPortion

         nanoVel.x =+ nanoXMomentum/nanoM ## adds an impulse to the velocity on each axis
         nanoVel.y =+ nanoYMomentum/nanoM
         nanoVel.z =+ nanoZMomentum/nanoM


    ## simulates SF6/C60/alpha collisions. Delete as appropriate, needs refining
    if np.random.randint(0,1001)>998: ## rolls a random number to decide if collision has occured
        #Impulse = 0.1*(3e8)*alphaM      ## Alpha particle
        Impulse = 0.01 * (3e8) * c60M  ## C60 particle
        #Impulse = 0.0001 * (3e8) * sf6M  ## SF6 particle

        nanoMomentum = nanoVel.x * nanoM + Impulse
        nanoVel.x += nanoMomentum/nanoM
    #'''

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
            

    rate(100) ## sets the animation rate


