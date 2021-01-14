import numpy
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib

G = 9.81

la = 1.0
lb = 1.0
ma = 1.0
mb = 1.0


# angle en degré & vitesse angulaire en degré par seconde
thetaA= 120.0
thetaB= 105.0
omegaA= 0.0
omegaB= 0.0

max_time= 30
dt= 0.02

# return an array from 0 to max_time w/ dt as step
t= numpy.arange(0, max_time, dt)



#convertir en radian & radian par secondes /deg2rad
# etat = [thA,wA,thB,WB]
etat = numpy.radians([thetaA,omegaA,thetaB,omegaB])


#fonction dérivée, prend en paramètres les états (position & vitesse) ainsi que le vecteur de temps
def func(etat, t):
    dydx = numpy.zeros_like(etat)
    dydx[0] = etat[1]

    delta = etat[2] - etat[0]
    den1 = (ma + mb) * la - mb * la * numpy.cos(delta) * numpy.cos(delta)
    dydx[1] = ((mb * la * etat[1] * etat[1] * numpy.sin(delta) * numpy.cos(delta)
                + mb * G * numpy.sin(etat[2]) * numpy.cos(delta)
                + mb * lb * etat[3] * etat[3] * numpy.sin(delta)
                - (ma + mb) * G * numpy.sin(etat[0]))
               / den1)

    dydx[2] = etat[3]

    den2 = (lb / la) * den1
    dydx[3] = ((- mb * lb * etat[3] * etat[3] * numpy.sin(delta) * numpy.cos(delta)
                + (ma + mb) * G * numpy.sin(etat[0]) * numpy.cos(delta)
                - (ma + mb) * la * etat[1] * etat[1] * numpy.sin(delta)
                - (ma + mb) * G * numpy.sin(etat[2]))
               / den2)
    return dydx

#intègre le système d'équations differentielles ordinaires
#Y tableau 2D des valeurs etats
Y= integrate.odeint(func,etat,t)

#on récupère toutes les lignes de la colonne 0 ce qui correspond à la position du point A
x1 = la * numpy.sin(Y[:,0])
y1= -la * numpy.cos(Y[:,0])

#ne pas oublier de décaler de |X1|
x2= lb * numpy.sin(Y[:,2])+x1
y2= -lb * numpy.cos(Y[:,2])+y1

#ici les vitesse angulaires du point A & B
wA=Y[:,1]
wB=Y[:,3]

#Ici on récupère les valeurs d'angles prise par A & B
AngleA= Y[:, 0]
AngleB= Y[:, 2]

#On crée une nouvelle figure
figure = plt.figure(figsize=(17, 8))

#faire dépendre la taille de la et lb, centré en 0
ax= figure.add_subplot(3,1,1, autoscale_on=False, xlim=(-la-lb, la+lb), ylim=(-la-lb, la+lb))
ax.set_aspect('equal')
#ax.grid()
line, = ax.plot([],[],'o-',color='b',lw=2)
path, = ax.plot([], [], color='r', alpha=0.25)

time_template = 'time = %.1fs'
time_text = ax.text(0.25, 0.90, '', transform=ax.transAxes)

#----------------------------------------------------------
#Compute the angular velocity of the two points
bx= figure.add_subplot(3,1,2, autoscale_on=False,xlim=(0,max_time),ylim=(min(min(wB),min(wA)),max(max(wB),max(wA))))
bx.grid()
curveWa,= bx.plot([],[],color='purple',lw=1,label='Vitesse Oméga_a')
curveWb,= bx.plot([], [],color='green',lw=1,label='Vitesse Oméga_b')

#----------------------------------------------------------
#Compute the angle of the point A & B
cx =figure.add_subplot(3,1,3, autoscale_on=False, xlim=(0, max_time), ylim=(min(min(AngleB),min(AngleA)),max(max(AngleB),max(AngleA))))
cx.grid()
CurveAngleA,= cx.plot([], [], color='purple', lw=1,label='angle_A(rad)')
CurveAngleB,= cx.plot([], [], color='green', lw=1,label='angle_B(rad)')

# Set les titres de chaques subplots
ax.title.set_text('Simulation de la trajectoire du double pendule')
bx.title.set_text('Vitesse angulaire W(t)')
cx.title.set_text('Angle théta(t)')


resume = False

def pauseIt(event):
    global resume
    if resume:
        anim.event_source.start()
        resume = False
        # print("start")
    else:
        anim.event_source.stop()
        resume = True
        # print("stop")


def initialisation():
    line.set_data([], [])
    path.set_data([], [])

    curveWa.set_data([], [])
    curveWb.set_data([], [])

    CurveAngleA.set_data([], [])
    CurveAngleB.set_data([], [])

    time_text.set_text('')
    return line ,  time_text

PATH_RANGE= None

def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    start_range= i - PATH_RANGE if PATH_RANGE!= None else 0
    start_range = numpy.clip(start_range, 0, None)
    thispath = [x2[start_range:i], y2[start_range:i]]

    path.set_data(thispath)
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i * dt))

    thisCruveA=  [t[start_range:i],wA[start_range:i]]
    thisCruveB = [t[start_range:i], wB[start_range:i]]
    curveWa.set_data(thisCruveA)
    curveWb.set_data(thisCruveB)

    thisAngleA = [t[start_range:i], AngleA[start_range:i]]
    thisAngleB = [t[start_range:i], AngleB[start_range:i]]
    CurveAngleA.set_data(thisAngleA)
    CurveAngleB.set_data(thisAngleB)


    return line, path , time_text , curveWa, curveWb, CurveAngleA, CurveAngleB,

figure.canvas.mpl_connect('button_press_event', pauseIt)


#FuncAnimation(fig, func, frames ,
# range(1,len(Y)= [1..Y-1]
#interval = Delay between frames in milliseconds (max_time/n) *(1000) avec n le nombre d'élément dans t, dt*1000
anim = matplotlib.animation.FuncAnimation(figure, animate, range(1, len(Y)),interval=(1 / (len(t) / max_time)) * 1000, blit=True, init_func=initialisation)
plt.show()




