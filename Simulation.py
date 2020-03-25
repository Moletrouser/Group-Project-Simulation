from vpython import *
import numpy as np
import pickle as p

i=0
xPosData = np.array([])
yPosData = np.array([])
zPosData = np.array([])
timeData = np.array([])
velocityComponents = np.zeros(3)

count = 0
canvas(width=2400, height=1400)  # slightly bigger than default, adjust if you have small screen.

dt = 10e-8 # timestep

box = box(pos=vector(0,0,0),length=10e-8, height=10e-8, width=10e-8, opacity=0.1) ## sets the size of the box

## values for the nano particle mass, M, the gas particle mass, and SF6/C60 masses in kg
nanoM = 1e-18
gasM = 5.46e-26
alphaM = 6.644e-27
sf6M = 2.425e-25
c60M = 1.197e-24

T = 293
kB = 1.38e-23
P_gas = 5
nanoR = 199e-9
rho = 1850

## marks the centre where potential is zero for reference
centrePos = vector(0,0,0)
Centre = sphere(pos=centrePos, radius= 10e-11, color=color.white)

## takes randoms values from a normal dist. for the nano particle starting position (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
#nanoxPos = np.random.normal(5e-7,5e-8,1)
#nanoyPos = np.random.normal(5e-7,5e-8,1)
#nanozPos = np.random.normal(5e-7,5e-8,1)

nanoxPos = 2.65e-8
nanoyPos = 1.35e-8
nanozPos = 1.2e-8 #-51
initNanoPos = vector(nanoxPos, nanoyPos, nanozPos)

## takes randoms values from a normal dist. for the nano particle velocity (mean 5, standard dev. 0.5) PLACEHOLDER VALUES
#nanoxVel = np.random.normal(1e-6,1e-7,1)
#nanoyVel = np.random.normal(1e-6,1e-7,1)
#nanozVel = np.random.normal(1e-6,1e-7,1)

nanoxVel = 0
nanoyVel = 0
nanozVel = 0
nanoVel = vector(nanoxVel, nanoyVel, nanozVel)

## creates the nano particle with values defined above
nanoParticle = sphere(pos=initNanoPos, radius=10e-10, color=color.blue, make_trail=True, retain = 50, interval=1 )
nanoParticle.trail_color = color.white  # change the trail colour to white, or any colour you fancy
nanoVector = nanoParticle.pos
nanoVectorMag = mag(nanoVector)

## creates a set of orthogonal arrows and labels to mark the co-ordinate axis
xArrow = arrow(pos=vector(box.length/2+0.1*box.length,0,0), axis=vector(0.15*box.length,0,0), shaftwidth=10e-10, color=color.red)
xLabel= label( pos=vec(box.length/2+0.1*box.length + 1.1*xArrow.length,0,0), text='x', color=color.red)
yArrow = arrow(pos=vector(box.width/2+0.1*box.length,0,0), axis=vector(0,0.15*box.length,0), shaftwidth=10e-10, color=color.blue)
yLabel= label( pos=vec(box.width/2+0.1*box.length,1.1*yArrow.length,0), text='y', color=color.blue)
zArrow = arrow(pos=vector(box.height/2+0.1*box.length,0,0), axis=vector(0,0,0.15*box.length), shaftwidth=10e-10, color=color.green)
zLabel= label( pos=vec(box.height/2+0.1*box.length,0,1.1*zArrow.length), text='z', color=color.green)

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

x_Hist = gvbars(graph=graphHist, color=color.red, label='x')
c = (8*kB*T/gasM/pi)**0.5 #Particle mean speed
b = ((1 + pi/8)*c*P_gas*gasM)/(kB*T*nanoR*rho) #gas damping term

b = ((1 + pi/8)*c*P_gas*gasM)/(kB*T*nanoR*rho) #gas damping term

gasMomentum = c*gasM

Sthermal = 4*kB*T*gasM*b

thermalX = Sthermal
thermalY = Sthermal
thermalZ = Sthermal

print("The value of b is: ", b)
print("Sthermal is: ", Sthermal)

'''
def casimirForce(x):
    casimirForceMicroN = 0.0408*x**4 - 0.5945*x**3 + 1.9414*x**2 + 1.8969*x - 3.067
    casimirForce = casimirForceMicroN*10**-6
    if abs(x) > 70:
        casimirForce = 0
    return x
'''
def casimirForce(x):
    return 0


distanceToPlate = 7 + nanoVector.z  ## calculates the distance to the plate

## the entire simulation takes place within this while loop
while True:

    ## sets the magnitude of the restoration force on each axisc
    restForceMagX = (1.42e-7)*abs(nanoVector.x)
    dampingForceMagX = b * abs(nanoVel.x)

    restForceMagY = (5.68e-7)*abs(nanoVector.y)
    dampingForceMagY = b * abs(nanoVel.y)

    restForceMagZ = (8.88e-7)*abs(nanoVector.z)
    dampingForceMagZ = b * abs(nanoVel.z)

    distanceToPlate = 100 + nanoVector.z  ## calculates the distance to the plate


    ## checks the position of the particle to decide in what direction the restoring force/ thermal energy input should act (WITH CASIMIR)

    if nanoVector.x > 0:
        nanoVel.x = nanoVel.x - dt * restForceMagX / nanoM
    else:
        nanoVel.x = nanoVel.x + dt * restForceMagX / nanoM

    if nanoVector.y > 0:
        nanoVel.y = nanoVel.y - dt * restForceMagY / nanoM
    else:
        nanoVel.y = nanoVel.y + dt * restForceMagY / nanoM

    if nanoVector.z > 0:
        nanoVel.z = nanoVel.z - dt * (restForceMagZ - casimirForce(distanceToPlate/10e6))/ nanoM
    else:
        nanoVel.z = nanoVel.z + dt * (restForceMagZ + casimirForce(distanceToPlate/10e6))/ nanoM

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


    ## simulates gas particle collisionsr
    if np.random.randint(0,1001)>999: ## rolls a random number to decide if collision has occurred
        i = 0
        while i < 3:
            velocityComponents[i] = np.sqrt(kB*T/gasM)*np.random.normal(0,1)
            i = i + 1

    xPortion = velocityComponents[0]*gasM
    yPortion = velocityComponents[1]*gasM
    zPortion = velocityComponents[2]*gasM

    nanoXMomentum = nanoVel.x * nanoM + xPortion*np.random.randint(0,101)/100
    nanoYMomentum = nanoVel.y * nanoM + yPortion*np.random.randint(0,101)/100
    nanoZMomentum = nanoVel.z * nanoM + zPortion*np.random.randint(0,101)/100

    nanoVel.x = + nanoXMomentum / nanoM  ## adds an impulse to the velocity on each axis
    nanoVel.y = + nanoYMomentum / nanoM
    nanoVel.z = + nanoZMomentum / nanoM

    '''
    ## simulates SF6/C60/alpha collisions. Delete as appropriate, needs refining
    if np.random.randint(0,25001)>24999: ## rolls a random number to decide if collision has occured
        Impulse = 0.01*(3e8)*alphaM      ## Alpha particle
        #Impulse = 0.0001 * (3e8) * sf6M  ## SF6 particle

        nanoMomentum = nanoVel.x * nanoM + Impulse*np.random.randint(0,101)/100
        nanoVel.x += nanoMomentum/nanoM
    '''

    nanoVector.x = nanoVector.x + nanoVel.x * dt + dt * dt * restForceMagX/(2*nanoM)
    nanoVector.y = nanoVector.y + nanoVel.y * dt + dt * dt * restForceMagY/(2*nanoM)
    nanoVector.z = nanoVector.z + nanoVel.z * dt + dt * dt * restForceMagZ/(2*nanoM)
    
    nanoParticle.pos = nanoVector  # sets the new nanoParticle position to the updated postion vector
    nanoVectorMag = mag(nanoVector)

    count = count + dt

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

    if i < 100:
        i = i + 1

    if i >= 100:
        print("The number of xPosData points is: ", xPosData.size)
        i=0

    #p.dump(combinedData, open("combinedData.pkl", "wb"))

    np.savetxt('timeData.csv', timeData)
    np.savetxt('xData.csv', xPosData)
    np.savetxt('yData.csv', yPosData)
    np.savetxt('zData.csv', zPosData)

    rate(400) ## sets the animation rate


