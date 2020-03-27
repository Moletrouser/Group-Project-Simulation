from vpython import *
import numpy as np

# initialises the various arrays used
xPosData = np.array([])
yPosData = np.array([])
zPosData = np.array([])
timeData = np.array([])
velocityComponents = np.zeros(3)

# initialises the time counter and loop counters
i = 0
count = 0

# sets the canvas size
canvas(width=2400, height=1400)  # slightly bigger than default, adjust if you have small screen.

# sets the time step
dt = 10e-8

# creates the canvas
box = box(pos=vector(0,0,0),length=10e-8, height=10e-8, width=10e-8, opacity=0.1) ## sets the size of the box

## values for constants used in later equations
nanoM = 1e-18
gasM = 5.46e-26
alphaM = 6.644e-27
sf6M = 2.425e-25
c60M = 1.197e-24
T = 293
kB = 1.38e-23
P_gas = 500
nanoR = 199e-9
rho = 1850

## marks the centre where potential is zero, for reference
centrePos = vector(0,0,0)
Centre = sphere(pos=centrePos, radius= 10e-11, color=color.white)

# sets the nanoparticle's initial positon
nanoxPos = 2.65e-6
nanoyPos = 1.35e-6
nanozPos = 1.2e-6 #-51
initNanoPos = vector(nanoxPos, nanoyPos, nanozPos)

## sets the nanoparticle's intital velocity
nanoxVel = 0
nanoyVel = 0
nanozVel = 0
nanoVel = vector(nanoxVel, nanoyVel, nanozVel)

## creates the nano particle with values defined above
nanoParticle = sphere(pos=initNanoPos, radius=10e-10, color=color.blue, make_trail=True, retain = 50, interval=1)
nanoParticle.trail_color = color.white  # change the trail colour to white, or any colour you fancy
nanoVector = nanoParticle.pos
nanoVectorMag = mag(nanoVector)

## creates a set of orthogonal arrows and labels to mark the co-ordinate axes
xArrow = arrow(pos=vector(box.length/2+0.1*box.length,0,0), axis=vector(0.15*box.length,0,0), shaftwidth=10e-10, color=color.red)
xLabel= label(pos=vec(box.length/2+0.1*box.length + 1.1*xArrow.length,0,0), text='x', color=color.red)
yArrow = arrow(pos=vector(box.width/2+0.1*box.length,0,0), axis=vector(0,0.15*box.length,0), shaftwidth=10e-10, color=color.blue)
yLabel= label( pos=vec(box.width/2+0.1*box.length,1.1*yArrow.length,0), text='y', color=color.blue)
zArrow = arrow(pos=vector(box.height/2+0.1*box.length,0,0), axis=vector(0,0,0.15*box.length), shaftwidth=10e-10, color=color.green)
zLabel= label(pos=vec(box.height/2+0.1*box.length,0,1.1*zArrow.length), text='z', color=color.green)

# defines the paramaters for vpythons dynamical graphing
graphpos = graph(x=2000, y=2000, width=1000, height=500, title='Position Vs Time', xtitle='time /s', ytitle='Position /m',
                 foreground=color.black, background=color.white)
graphVel = graph(x=2000, y=2000, width=1000, height=500, title='Velocity Vs Time', xtitle='time /s', ytitle='Velocity /ms^-1',
                 foreground=color.black, background=color.black)
graphKE = graph(x=2000, y=2000, width=1000, height=500, title='KE Vs Time', xtitle='time /s', ytitle='KE',
                 foreground=color.black, background=color.black)
graphHist = graph(x=2000, y=2000, width=1000, height=500, title='Position Frequency', xtitle='Position', ytitle='Frequency',
                 foreground=color.black, background=color.black)

x_pos = gcurve(graph=graphpos, color=color.red, label='x position')
y_pos = gcurve(graph=graphpos, color=color.blue, label='y position')
z_pos = gcurve(graph=graphpos, color=color.green, label='z position')

x_vel = gcurve(graph=graphVel, color=color.red, label='x velocity')
y_vel = gcurve(graph=graphVel, color=color.blue, label='y velocity')
z_vel = gcurve(graph=graphVel, color=color.green, label='z velocity')

c = (8*kB*T/gasM/pi)**0.5 #Particle mean speed
b = ((1 + pi/8)*c*P_gas*gasM)/(kB*T*nanoR*rho) #gas damping term

gasMomentum = c*gasM

Sthermal = 4*kB*T*gasM*b # the thermal energy equation

thermalX = Sthermal
thermalY = Sthermal
thermalZ = Sthermal

def casimirForce(x):
    casimirForceNewtons = (-8e-13)*x**6 + (9e-11)*x**5 - (4e-9)*x**4 + (9e-8)*x**3 - (1e-6)*x**2 + (5e-6)*x - 4e-6
    if x < 6e-6 or 3e-6 < x:
        casimirForceNewtons = 0
    return casimirForceNewtons

## the entire simulation takes place within this while loop
while True:

    ## sets the magnitude of the restoration force on each axisc
    restForceMagX = (1.42e-7)*abs(nanoVector.x)
    dampingForceMagX = b * abs(nanoVel.x)

    restForceMagY = (5.68e-7)*abs(nanoVector.y)
    dampingForceMagY = b * abs(nanoVel.y)

    restForceMagZ = (8.88e-7)*abs(nanoVector.z)
    dampingForceMagZ = b * abs(nanoVel.z)

    distanceToPlate = 1e-6 + nanoVector.z  ## calculates the distance to the , with the plate set at -1e-6 m on the z axis


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
        nanoVel.z = nanoVel.z - dt * (restForceMagZ - casimirForce(distanceToPlate))/ nanoM
    else:
        nanoVel.z = nanoVel.z + dt * (restForceMagZ + casimirForce(distanceToPlate))/ nanoM

    ## checks the velocity of the particle to decide in what direction the damping force should act
    if nanoVel.x > 0:
        nanoVel.x = nanoVel.x - dt * dampingForceMagX + dt*thermalX
    else:
        nanoVel.x = nanoVel.x + dt * dampingForceMagX - dt*thermalX

    if nanoVel.y > 0:
        nanoVel.y = nanoVel.y - dt * dampingForceMagY + dt*thermalY
    else:
        nanoVel.y = nanoVel.y + dt * dampingForceMagY - dt*thermalX

    if nanoVel.z > 0:
        nanoVel.z = nanoVel.z - dt * dampingForceMagZ + dt*thermalY
    else:
        nanoVel.z = nanoVel.z + dt * dampingForceMagZ - dt*thermalX

    ## simulates gas particle collisions
    if np.random.randint(0,1001)>999: ## rolls a random number to decide if collision has occurred
        i = 0
        while i < 3:
            velocityComponents[i] = np.sqrt(kB*T/gasM)*np.random.normal(0,1)
            i = i + 1

    # calculates the momentum associated with the gas particle velocity on each axis
    xPortion = velocityComponents[0]*gasM
    yPortion = velocityComponents[1]*gasM
    zPortion = velocityComponents[2]*gasM

    # updates the momenta of the nanoparticle
    nanoXMomentum = nanoVel.x * nanoM + xPortion*np.random.randint(0,101)/100
    nanoYMomentum = nanoVel.y * nanoM + yPortion*np.random.randint(0,101)/100
    nanoZMomentum = nanoVel.z * nanoM + zPortion*np.random.randint(0,101)/100

    nanoVel.x = + nanoXMomentum / nanoM  ## adds an impulse to the velocity on each axis
    nanoVel.y = + nanoYMomentum / nanoM
    nanoVel.z = + nanoZMomentum / nanoM
    
    ## simulates SF6/C60/alpha collisions. Delete as appropriate
    if np.random.randint(0,10001)>9999: ## rolls a random number to decide if collision has occured
        Impulse = 0.01*(3e8)*alphaM      ## Alpha particle
        #Impulse = 0.0001 * (3e8) * sf6M  ## SF6 particle

        nanoMomentum = nanoVel.x * nanoM + Impulse*np.random.randint(0,101)/100
        nanoVel.x += nanoMomentum/nanoM

    nanoVector.x = nanoVector.x + nanoVel.x * dt + dt * dt * restForceMagX/(2*nanoM)
    nanoVector.y = nanoVector.y + nanoVel.y * dt + dt * dt * restForceMagY/(2*nanoM)
    nanoVector.z = nanoVector.z + nanoVel.z * dt + dt * dt * restForceMagZ/(2*nanoM)
    
    nanoParticle.pos = nanoVector  # sets the new nanoParticle position to the updated position vector
    nanoVectorMag = mag(nanoVector)

    # advances the times counter
    count = count + dt

    #dynamically dispays the postion/velocity time graphs to the screen
    x_pos.plot(pos=(count, nanoVector.x))
    y_pos.plot(pos=(count, nanoVector.y))
    z_pos.plot(pos=(count, nanoVector.z))

    x_vel.plot(pos=(count, nanoVel.x))
    y_vel.plot(pos=(count, nanoVel.y))
    z_vel.plot(pos=(count, nanoVel.z))

    timeData = np.append(timeData, count)
    xPosData = np.append(xPosData, nanoVector.x)
    yPosData = np.append(yPosData, nanoVector.y)
    zPosData = np.append(zPosData, nanoVector.z)

    # provides a visual counter for the number of data points saved that is printed to the screen
    if i < 100:
        i = i + 1

    if i >= 100:
        print("The number of xPosData points is: ", xPosData.size)
        i=0

    # saves the position and time data as CSVs
    np.savetxt('timeData.csv', timeData)
    np.savetxt('xData.csv', xPosData)
    np.savetxt('yData.csv', yPosData)
    np.savetxt('zData.csv', zPosData)

    rate(200) ## sets the animation rate


