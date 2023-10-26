# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 10:17:46 2021

@author: Victor Toro Lara 
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import scipy.io as sio
import csv as csv
from matplotlib import pyplot as plt  

# Crea dataframe con info importada desde google
df = pd.read_excel('linares-mulchen.xlsx')

import sys
#print(sys.getrecursionlimit())



#pasando dataframe a listas
lati=df['lat'].tolist()
longi=df['long'].tolist()
slope=df['slope(%)'].tolist()
slopecorre=df['slope(%)corre'].tolist()
sloperedon=df['slope(%)redon'].tolist()
distance_m=df['distance[m]'].tolist()
interval_m=df['interval[m]'].tolist()

viaje=[lati,longi,slope,slopecorre,sloperedon,distance_m,interval_m] 

#filtra intervalos con poca resolución            
viajelimpio=[[],[],[],[],[],[],[]]       
def limpieza150(viaje):
    newinter=0
    sumay=0
    for x in range(len(viaje[0])):

        if newinter<=150:
            newinter=newinter+viaje[6][x]
            sumay=sumay+viaje[6][x]*viaje[2][x]/100
            
        else:
            viajelimpio[0].append(viaje[0][x])
            viajelimpio[1].append(viaje[1][x])
            sloperad=np.arctan(sumay/newinter)
            slopegrad=sloperad*180/(np.pi)
            slopeporct=sumay/newinter*100
            viajelimpio[2].append(slopeporct)
            viajelimpio[3].append(0)
            viajelimpio[4].append(0)
            viajelimpio[5].append(0)
            viajelimpio[6].append(newinter)
            newinter=viaje[6][x]
            sumay=viaje[6][x]*viaje[2][x]/100
            
    for x in range(len(viajelimpio[0])):
        if x==0:
            viajelimpio[3][x]=viajelimpio[2][x]
        else:
            if abs(viajelimpio[2][x])>8:
                viajelimpio[3][x]=viajelimpio[3][x-1]
            else:
                viajelimpio[3][x]=viajelimpio[2][x]
       
    for x in range(len(viajelimpio[0])):
        viajelimpio[4][x]=round(viajelimpio[3][x])  
        
    for x in range(len(viajelimpio[0])):
        if x==0:
            viajelimpio[5][x]=viajelimpio[6][x]
        else:
            viajelimpio[5][x]=viajelimpio[6][x]+viajelimpio[5][x-1]    
                
                

        
limpieza150(viaje)       
        
# Info del chasis del camión.

pbv=45 #t
volumen= 70 #m3
g=9.8 #m/s2
rho= 1.225 #kg/m3
p1=14.94
p2=11.28
p3=9.04
p4=7.09
p5=5.54
p6=4.35
p7=3.44
p8=2.7
p9=2.08
p10=1.63
p11=1.27
p12=1
pd=2.64
alto=3.8
ancho=2.5
a= ancho*alto
nllantas=12
dneuma=41.8 #en pulgadas
velocidad=90/3.6 #m/s

tmax= 3300 #nm
c_tmax= 194 #gr/kwh

cero_noventa=180 #segundos

pm_cmin= 308 #kw

# #ref
# cr=0.0051 
# f=1
# cd= 0.58

#pesimista
cr=0.006
cd=0.91
f=1

# #optimista
# cr=0.0032
# cd=0.58
# f=1


#porcentaje a grados
def porctograd (alpha_porcentaje):
    if alpha_porcentaje <0:
        return (-1)*abs(np.arctan(alpha_porcentaje/100))*360/(2*np.pi)
    else:
        return np.arctan(alpha_porcentaje/100)*360/(2*np.pi)
        

#Acá defino las potencias. 
#area en metros y peso en toneladas
def pe(pb):
    return (12.03*a+2.033*pb)*1.34102
#peso en toneladas y velocidad en km/h
def pu(pb,v):
    return (cr*pb*g*(v/3.6))*1.34102
#velocidad en km/h
def paero(v):
    return 1.34102*rho*cd*a*((v/3.6)**3)/2000
#pb en toneladas
def pin(pb):
    return pb*(velocidad/cero_noventa)*velocidad*1.34102
#pb en toneladas, theta en porcentaje y velocidad en km/h
def ppe(pb,theta,v_ascen):
    return pb*g*(v_ascen/3.6)*np.sin(porctograd(theta)*2*np.pi/360)*1.34102
#n en rpm p es el paso de la marcha
def velo(n,p):
    return  n*2*np.pi*60*(dneuma*0.0245/2)/(1000*p*pd)


# Curvas ascenso velocidad descendente. Define la velocidad del camión en función de la ruta
    
def pend1(x):
    if x>2400:
        return 85.329
    else:    
        return 87.8 - 2.44E-3*x+5.53E-7*x**2+0.2

def pend2(x):
    if x>2300:
        return 73.25
    else:
        return 87.4-0.0126*x+2.69E-6*x**2 +0.6   

def pend3(x):
    if x>2000:
        return 60.44
    else:
        return 88.6-0.0379*x+1.73E-5*x**2-2.62E-9*x**3-0.6

def pend4(x):
    if x>2400:
        return 47.87
    else:
        return 87.8-0.0539*x+2.55E-5*x**2-4.17E-9*x**3+0.2

def pend5(x):
    if x>1200:
        return 42.15
    else:
        return 89.8-1.8 - 0.096*x+7.28E-5*x**2-2.4E-8*x**3+2.89E-12*x**4

def pend6(x):
    if x>834:
        return 37.11
    else:
        return 90.4-2.4-0.116*x+8.47E-5*x**2-2.43E-8*x**3+2.16E-12*x**4

def pend7(x):
    if x>750:
        return 32.044
    else:
        return 91.1-3.1-0.141*x+1.15E-4*x**2-3.87E-8*x**3+4.53E-12*x**4

def pend8(x):
    if x>750:
        return 27.12
    else:
        return 90.3-2.3-.163*x+1.47E-4*x**2-5.64E-8*x**3+7.83E-12*x**4

# Caso descenso velocidad ascendente. Define la velocidad del camión en función de la ruta
    
def pend0(x):
    if x>2250:
        return 88
    else:
        return (1- 1/(np.e**((0.00330941091482836*x)**0.374329530769291)))*100
    
def pendm1(x):
    if x>1650:
        return 88
    else:
        return (1- 1/(np.e**((0.00455755241896724*x)**0.372499460534917)))*100
    
def pendm2(x):
    if x<150:
        return x*31/75
    if x>=150 and x<750:
        return x*13/300 + 111/2
    else:
        return 88
def pendm3(x):
    if x<150:
        return x*32/75
    if x>=150 and x<620:
        return x*23/450 + 169/3
    else:
        return 88

def pendm4(x):
    if x<150:
        return x*34/75
    if x>=150 and x<520:
        return x*2/37 + 2216/37 
    else:
        return 88   
    
def pendm5(x):
    if 0<=x<150:
        return x*72/150
    if x>=150 and x<450:
        return x*4/75+64
    if x>=450:
        return 88    
    
def pendm6(x):
    if x<150:
        return x*74.5/150
    if x>=150 and x<450:
        return x*0.045 + 67.75
    else:
        return 88      

def pendm7(x):
    if x<150:
        return x*77.7/150
    if x>=150 and x<300:
        return x*0.06313 + 68.23
    else:
        return 88     
    
def pendm8(x):
    if x<150:
        return x*80.9/150
    if x>=150 and x<300:
        return x*0.04733 + 73.8
    else:
        return 88  
    
def penda1(x):
    if x==0:
        return 0
    if x>0:
        return -3.29+10.6*np.log(x)
    if x>3600:
        return 83.51
    
def penda2(x):
    if x==0:
        return 0
    if x>0:
        return 3.5+8.44*np.log(x)
    if x>2100:
        return 68.06 
    
def penda3(x):
    if x==0:
        return 0
    if x>0:
        return 6.39+6.91*np.log(x)
    if x>2026:
        return 59.001
    
def penda4(x):
    if x==0:
        return 0
    if x>0:
        return 7.24+5.92*np.log(x)
    if x>980:
        return 48.0143 
    
def penda5(x):
    if x==0:
        return 0
    if x>0:
        return 11.4+4.49*np.log(x)   
    if x>920:
        return 42.041 
    
def penda6(x):
    if 0<=x<=75:
        return x/3
    if 75<x<=150:
        return 19+2*x/25
    if 150<x<=300:
        return 29+x/75
    if 300<x<=450:
        return 29+x/75
    if 450<x<=600:
        return 32+x/150
    if 600<x<=1050:
        return 104/3+x/450
    if x>1050:
        return 37
    
def penda7(x):
    if x==0:
        return 0
    if  0<x<=150:
        return -1.11+5.14*np.log(x)
    if 150<x<=300:
        return 0.02906*x+20.28
    if 300<x<=450:
        return 25+x/75
    if 450<x<=750:
        return 59/2+x/300
    if x>750:
        return 32
        
def penda8(x):
    if x==0:
        return 0
    if 0<x<=75:
        return -2.77+4.64*np.log(x)  
    if 75<x<=285:
        return x*0.03653+14.52  
    if 285<x<=450:
        return 23+x/150
    if 450<x<=750:
        return 49/2+x/300
    if x>750:
        return 27 
    
    
# Ecuacion para columna velocidad
def columnvelo(trip):
    viaje=trip
    viaje.append([0]*len(viaje[0])) #esto lo ocuparé cuando esté listo
    #viaje.append([0]*170)
    viaje.append([0]*len(viaje[0])) #columna para indicar si dato sirve o no.
    #viaje.append([0]*170)
    for i in range(len(viaje[0])): 
    #for i in range(170):
        if i==0:
            if viaje[4][0]==-8:
                viaje[7][0]=pendm8(viaje[6][0])
            if viaje[4][0]==-7:
                viaje[7][0]=pendm7(viaje[6][0])    
            if viaje[4][0]==-6:
                viaje[7][0]=pendm6(viaje[6][0])    
            if viaje[4][0]==-5:
                viaje[7][0]=pendm5(viaje[6][0])
            if viaje[4][0]==-4:
                viaje[7][0]=pendm4(viaje[6][0])
            if viaje[4][0]==-3:
                viaje[7][0]=pendm3(viaje[6][0])
            if viaje[4][0]==-2:
                viaje[7][0]=pendm2(viaje[6][0])
            if viaje[4][0]==-1:
                viaje[7][0]=pendm1(viaje[6][0])    
            if viaje[4][0]==0:
                viaje[7][0]=pend0(viaje[6][0])    
            if viaje[4][0]==1:
                viaje[7][0]=penda1(viaje[6][0])
            if viaje[4][0]==2:
                viaje[7][0]=penda2(viaje[6][0])
            if viaje[4][0]==3:
                viaje[7][0]=penda3(viaje[6][0])
            if viaje[4][0]==4:
                viaje[7][0]=penda4(viaje[6][0])
            if viaje[4][0]==5:
                viaje[7][0]=penda5(viaje[6][0])
            if viaje[4][0]==6:
                viaje[7][0]=penda6(viaje[6][0])
            if viaje[4][0]==7:
                viaje[7][0]=penda7(viaje[6][0])    
            if viaje[4][0]==8:
                viaje[7][0]=penda8(viaje[6][0])    
        

        else:
            
            if viaje[4][i]== -3 or -4 or -5 or -6 or -7 or -8:
                velo_actual=viaje[7][i-1]
                for l in range(36000):
                    if abs(pendm2(l/10)-velo_actual)<0.1:
                        inter=(l/10)+viaje[6][i]
                        viaje[8][i]=1
                        break
                    else:
                        inter=3600
                viaje[7][i]=pendm2(inter)  
                
            # if viaje[4][i]==-4:
            #     velo_actual=viaje[7][i-1]
            #     for l in range(36000):
            #         if abs(pendm4(l/10)-velo_actual)<0.1:
            #             inter=(l/10)+viaje[6][i]
            #             viaje[8][i]=1
            #             break
            #         else:
            #             inter=3600    
            #     viaje[7][i]=pendm4(inter)  
                
            # if viaje[4][i]==-3:
            #     velo_actual=viaje[7][i-1]
            #     for l in range(36000):
            #         if abs(pendm3(l/10)-velo_actual)<0.1:
            #             inter=(l/10)+viaje[6][i]
            #             viaje[8][i]=1
            #             break
            #         else:
            #             inter=3600    
            #     viaje[7][i]=pendm3(inter)   
                
            if viaje[4][i]==-2:
                velo_actual=viaje[7][i-1]
                for l in range(36000):
                    if abs(pendm2(l/10)-velo_actual)<0.1:
                        inter=(l/10)+viaje[6][i]
                        viaje[8][i]=1
                        break
                    else:
                        inter=3600    
                viaje[7][i]=pendm2(inter)  
                
            if viaje[4][i]==-1:
                velo_actual=viaje[7][i-1]
                for l in range(360000):
                    if abs(pendm1(l/100)-velo_actual)<0.1:
                        inter=(l/100)+viaje[6][i]
                        viaje[8][i]=1
                        break
                    else:
                        inter=3600    
                viaje[7][i]=pendm1(inter)  
                
            if viaje[4][i]==-0:
                velo_actual=viaje[7][i-1]
                for l in range(36000):
                    if abs(pend0(l/10)-velo_actual)<0.1:
                        inter=(l/10)+viaje[6][i]
                        viaje[8][i]=1
                        break
                    else:
                        inter=3600    
                viaje[7][i]=pend0(inter)  
                
            if viaje[4][i]==1:
                velo_actual=viaje[7][i-1]
                if 83.51<velo_actual<85.329:
                    velo_actual=83.51
                    for l in range(36000):
                        if abs(penda1(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda1(inter)        
                    
                if velo_actual>=85.329:
                    for l in range(36000):
                        if abs(pend1(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=2
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend1(inter)
                    
                if velo_actual<=83.51:
                    for l in range(36000):
                        if abs(penda1(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda1(inter)
           
            if viaje[4][i]==2:
                velo_actual=viaje[7][i-1]
                if 68.06<velo_actual<73.25:
                    velo_actual=68.06
                    for l in range(36000):
                        if abs(penda2(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda2(inter)
                    
                if velo_actual>=73.25:
                    for l in range(36000):
                        if abs(pend2(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend2(inter)
                    
                if velo_actual<=68.06:
                    for l in range(36000):
                        if abs(penda2(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda2(inter) 
                        
            if viaje[4][i]==3:
                velo_actual=viaje[7][i-1]
                if 59.001<velo_actual<60.44:
                    velo_actual=59.001
                    for l in range(36000):
                        if abs(penda3(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda3(inter)        
                    
                if velo_actual>=60.44:
                    for l in range(36000):
                        if abs(pend3(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend3(inter)
                    
                if velo_actual<=59.001:
                    for l in range(36000):
                        if abs(penda3(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda3(inter)  
                        
            if viaje[4][i]==4:
                velo_actual=viaje[7][i-1]
                if 48.01<velo_actual<47.87:
                    velo_actual=48.01
                    for l in range(36000):
                        if abs(penda4(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda4(inter)        
                    
                if velo_actual>=47.87:
                    for l in range(36000):
                        if abs(pend4(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend4(inter)
                    
                if velo_actual<=48.01:
                    for l in range(36000):
                        if abs(penda4(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda4(inter)
                    
            if viaje[4][i]==5:
                velo_actual=viaje[7][i-1]
                if 42.041<velo_actual<42.15:
                    velo_actual=42.041
                    for l in range(36000):
                        if abs(penda5(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda5(inter)        
                    
                if velo_actual>=42.15:
                    for l in range(36000):
                        if abs(pend5(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend5(inter)
                    
                if velo_actual<=42.041:
                    for l in range(36000):
                        if abs(penda5(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda5(inter)   
                    
            if viaje[4][i]==6:
                velo_actual=viaje[7][i-1]
                if 37<velo_actual<37.1:
                    velo_actual=37
                    for l in range(36000):
                        if abs(penda6(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda6(inter)        
                    
                if velo_actual>=37.1:
                    for l in range(36000):
                        if abs(pend6(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend6(inter)
                    
                if velo_actual<=37:
                    for l in range(36000):
                        if abs(penda6(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda6(inter)
                    
            if viaje[4][i]==7:
                velo_actual=viaje[7][i-1]
                if 32<velo_actual<32.044:
                    velo_actual=32
                    for l in range(36000):
                        if abs(penda7(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda7(inter)        
                    
                if velo_actual>=32.044:
                    for l in range(36000):
                        if abs(pend7(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend7(inter)
                    
                if velo_actual<=32:
                    for l in range(36000):
                        if abs(penda7(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda7(inter)  
                    
            if viaje[4][i]==8:
                velo_actual=viaje[7][i-1]
                if 27<velo_actual<27.12:
                    velo_actual=27
                    for l in range(36000):
                        if abs(penda8(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600 
                    viaje[7][i]=penda8(inter)        
                    
                if velo_actual>=27.12:
                    for l in range(36000):
                        if abs(pend8(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=1
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=pend8(inter)
                    
                if velo_actual<=27:
                    for l in range(36000):
                        if abs(penda8(l/10)-velo_actual)<0.1:
                            inter=(l/10)+viaje[6][i]
                            viaje[8][i]=0
                            break
                        else:
                            inter=3600    
                    viaje[7][i]=penda8(inter) 
                    
    for x in range(len(viaje[0])):
        viaje[7][x]=viaje[7][x]*f                  

#Agregando columna potencia requerida
def pestimada(peso,viaje):
    e_rodadura=list()
    e_rodadura.append([0]*len(viaje[0]))
    
    e_aero=list()
    e_aero.append([0]*len(viaje[0]))
    
    e_inercia=list()
    e_inercia.append([0]*len(viaje[0]))
    
    e_slope=list()
    e_slope.append([0]*len(viaje[0]))
    
    
    viaje.append([0]*len(viaje[0])) #esto lo ocuparé cuando esté listo
    #viaje.append([0]*170)
    viaje.append([0]*len(viaje[0])) #esto lo ocuparé cuando esté listo
    #viaje.append([0]*170)
    viaje.append([0]*len(viaje[0])) #esto lo ocuparé cuando esté listo
    #viaje.append([0]*170)
    viaje.append([0]*len(viaje[0])) #esto lo ocuparé cuando esté listo
    #viaje.append([0]*170)
    viaje.append([0]*len(viaje[0])) #esto lo ocuparé cuando esté listo
    #viaje.append([0]*170)
    for x in range(len(viaje[0])):
    #for x in range(170):
        if x==0:
            pot_rod=pu(peso,viaje[7][x])
            viaje[9][x]=pot_rod
            e_rodadura[0][x]=pot_rod*viaje[6][x]/1000/viaje[7][x]
            pot_aero=paero(viaje[7][x])
            e_aero[0][x]=pot_aero*viaje[6][x]/1000/viaje[7][x]
            viaje[10][x]=pot_aero
            if viaje[7][x]<15:
                pajus=peso*2.5
            if 15<=viaje[7][x]<24:
                pajus=peso*1.6
            if 24<=viaje[7][x]<29:
                pajus=peso*1.2    
            if 29<=viaje[7][x]:
                pajus=peso*1.09     
            pot_inercia= pajus*(((viaje[7][x]/3.6)**2-0)/(2*viaje[6][x]))*viaje[7][x]/(3.6*2)*1.34102
            #pb en toneladas, theta en porcentaje y velocidad en km/h
            viaje[11][x]=pot_inercia
            e_inercia[0][x]=pot_inercia*viaje[6][x]/1000/viaje[7][x]
            pot_p=ppe(peso,viaje[3][x],viaje[7][x]/2)
            viaje[12][x]=pot_p
            e_slope[0][x]=pot_p*viaje[6][x]/1000/viaje[7][x]
            total=pot_rod+pot_aero+pot_inercia+pot_p
            viaje[13][x]=total#FALTA SUMAR AIRE ACOND
        else:
            pot_rod=pu(peso,viaje[7][x])
            viaje[9][x]=pot_rod
            e_rodadura[0][x]=pot_rod*viaje[6][x]/1000/viaje[7][x]
            pot_aero=paero(viaje[7][x])
            viaje[10][x]=pot_aero
            e_aero[0][x]=pot_aero*viaje[6][x]/1000/viaje[7][x]
            if viaje[7][x]<15:
                pajus=peso*2.5
            if 15<=viaje[7][x]<24:
                pajus=peso*1.6
            if 24<=viaje[7][x]<29:
                pajus=peso*1.2    
            if 29<=viaje[7][x]:
                pajus=peso*1.09 
            pot_inercia= pajus*(((viaje[7][x]/3.6)**2-(viaje[7][x-1]/3.6)**2)/(2*viaje[6][x]))*(viaje[7][x]+viaje[7][x-1])/(2*3.6)*1.34102
            #pb en toneladas, theta en porcentaje y velocidad en km/h
            viaje[11][x]=pot_inercia
            e_inercia[0][x]=pot_inercia*viaje[6][x]/1000/viaje[7][x]
            pot_p=ppe(peso,viaje[3][x],(viaje[7][x]+viaje[7][x-1])/2)
            viaje[12][x]=pot_p
            e_slope[0][x]=pot_p*viaje[6][x]/1000/viaje[7][x]
            total=pot_rod+pot_aero+pot_inercia+pot_p
            viaje[13][x]=total#FALTA SUMAR AIRE ACOND
            
    sum1=0
    sum2=0
    sum3=0
    sum4=0 
    sumtime=0 #para saber el tiempo en que se cumplen las condiciones
              #es para conocer la potencia requerida por los aux. 
    
    for n in range(1,len(viaje[0])):
    
        if viaje[4][n]<=viaje[4][n-1] and viaje[4][n]>=0:#viaje[4][n]>=0: #and viaje[7][n]>viaje[7][n-1]:        
            sum1=sum1+e_rodadura[0][n]     
            sum2=sum2+e_aero[0][n] 
            sum3=sum3+e_inercia[0][n] 
            sum4=sum4+e_slope[0][n]
            sumtime=sumtime+viaje[6][x]/1000/viaje[7][x]
            
        else:
            sum1=sum1
            sum2=sum2
            sum3=sum3
            sum4=sum4
            sumtime=sumtime
    
        
    total=sum1+sum2+sum3+sum4  
    potencia_prom=total/sumtime
    pot_aux=potencia_prom*1.0752688-potencia_prom
    #sumtot_rodadura=sum(e_rodadura[0]) 
    #sumtot_aero=sum(e_aero[0]) 

    for x in range(len(viaje[0])):
        viaje[13][x]=viaje[13][x]+10#aquí ya agregué los auxiliares inspirado en la energía positiva consumida.
        

    
    print(f"Suma energía rodadura -> {sum1}[hp-h]")
    print(f"Suma energía aero -> {sum2}[hp-h]")
    print(f"Suma energía inercia -> {sum3}[hp-h]")
    print(f"Suma energía slope -> {sum4}[hp-h]")
    print(f"Suma energía total -> {total}[hp-h]") 
    print(f"Suma tiempo condicional -> {sumtime}[h]") 
    print(f"Potencia para auxiliares calculada -> {pot_aux}[hp]")
    print(f"Potencia para auxiliares fija -> {17.8}[hp]")
    #print(f"Suma total energía rodadura -> {sumtot_rodadura}[hp-h]")
    #print(f"Suma total energía aero -> {sumtot_aero}[hp-h]")
                                                                        
    
#Columna agrega tiempo
def agrega_time(viaje):
    viaje.append([0]*len(viaje[0]))
    #viaje.append([0]*170)
    for x in range(len(viaje[0])):
    #for x in range(170):    
        viaje[14][x]=viaje[6][x]/1000/viaje[7][x]
 
 
 
def consumomerce238(hp):
    if hp<=0:
        return 0
    if 0<hp<87.1:
        #return 0.291 + -1.53E-03*hp + 4.9E-06*hp**2
        return 0.305 + -1.79E-03*hp + 6.04E-06*hp**2
    if 87.1<=hp<120.6:
        return -0.00053*hp+0.24134
    if 120.6<=hp<144.72:
        return -0.00014*hp+0.193364
    if 144.72<=hp<167.5:
        return -0.00003*hp+0.17820
    if 167.5<=hp<194.3:
        return 0.00003*hp+0.165975
    if 194.3<=hp<238:
        return 0.00042*hp+0.09047
    
    if 238<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')  
        return 200   


#Ecuaciones de consumo       
def consumomerce306(hp):
    if hp<=0:
        return 0
    if 0<hp<103.18:
        return 0.259 + -7.89E-04*hp + 1.83E-06*hp**2
    if 103.18<=hp<150.08:
        return -0.00028*hp+0.226111
    if 150.08<=hp<234.5:
        return -0.0001*hp+0.19924
    if 234.5<=hp<270.68:
        return 0.00007*hp+0.15631
    if 270.68<=hp<306:
        return 0.0004*hp+0.06707
    if 306<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')  
        return 200
        
def consumomerce354(hp):
    if hp<=0:
        return 0
    if 0<hp<201:
        #return 0.292 + -9.41E-04*hp + 1.71E-06*hp**2
        #return 0.357 + -1.47E-03*hp + 2.78E-06*hp**2
        return 0.335 + -1.29E-03*hp + 2.43E-06*hp**2
    
    if 201<=hp<247.9:
        return -0.00017*hp+0.20721
    if 247.9<=hp<288.1:
        return -0.00002*hp+0.16964
    if 288.1<=hp<325.62:
        return 0.00014*hp+0.12246
    if 325.62<=hp<341.7:
        return 0.00055*hp-0.011325
    if 341.7<=hp<354:
        return 0.001*hp-0.16645
    
    if 354<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')    
        return 0
    
def consumocummins350(hp):
    if hp<=0:
        return 0
    if 0<hp<281.4:
        #return 0.292 + -7.64E-04*hp + 1.19E-06*hp**2
        return 0.372 + -1.29E-03*hp + 2.06E-06*hp**2
    if 281.4<=hp<309.54:
        return -0.00006*hp+0.18855
    if 309.54<=hp<335:
        return (-1*1.96386E-7*hp)+0.16897
    if 335<=hp<349.74:
        return 0.00036*hp+0.04709
    if 349.74<=hp<352.42:
        return 0.002*hp-0.526515
    
    if 352.42<=hp:
        print(hp,'¡EXCEDE POTENCIA MÁXIMA!')   
        return 0    
    
def consumocummins460(hp):
    if hp<=0:
        return 0
    if 0<hp<341.7:
        #return 0.305 + -7.4E-04*hp + 9.68E-07*hp**2
        return 0.39 + -1.18E-03*hp + 1.54E-06*hp**2
    if 341.7<=hp<381.9:
        return -0.00002*hp+0.17299
    if 381.9<=hp<458.28:
        return 0.00004*hp+0.14664
    if 458.28<=hp<460.96:
        return 0.00334*hp-1.363989

    
    
    if 460.96<=hp:
        print(hp ,'¡EXCEDE POTENCIA MÁXIMA!')  
        return 200 
    

    
#Columna agrega consumo de combustible  

def agregaconsumo(viaje,hp):
    viaje.append([0]*len(viaje[0]))
    #viaje.append([0]*170)
    
    if hp==306:
        for x in range(len(viaje[0])):
        #for x in range(170):
            viaje[15][x]=consumomerce306(viaje[13][x])*viaje[14][x]*viaje[13][x]        
    if hp==354:
        for x in range(len(viaje[0])):
        #for x in range(170):
            viaje[15][x]=consumomerce354(viaje[13][x])*viaje[14][x]*viaje[13][x] 
    if hp==238:
        for x in range(len(viaje[0])):
        #for x in range(170):
            viaje[15][x]=consumomerce238(viaje[13][x])*viaje[14][x]*viaje[13][x]  
            
    if hp==350:
        for x in range(len(viaje[0])):
        #for x in range(170):
            viaje[15][x]=consumocummins350(viaje[13][x])*viaje[14][x]*viaje[13][x] 
            
    if hp==460:
        for x in range(len(viaje[0])):
        #for x in range(170):
            viaje[15][x]=consumocummins460(viaje[13][x])*viaje[14][x]*viaje[13][x]           

def perfil_elev(viaje):
    viaje.append([0]*len(viaje[0]))
    viaje.append([0]*len(viaje[0]))
    for x in range(len(viaje[0])):
        viaje[16][x]=viaje[6][x]/1000
    for x in range(len(viaje[0])):
        viaje[17][x]=viaje[6][x]*np.tan((porctograd(viaje[3][x]))*np.pi/180)    
    for x in range(len(viaje[0])):
        if x>=1:
            viaje[16][x]=viaje[16][x]+viaje[16][x-1]
            viaje[17][x]=viaje[17][x]+viaje[17][x-1]
    
    #GRAFICANDO PERFIL DE ELEVACIÓN    
    plt.plot(viaje[16],viaje[17],'-',linewidth=2,color='b')   
    plt.grid()
    # plt.axis('equal')
    plt.xlabel('Distancia horizantal a 0 msnm [km]')
    plt.ylabel('Elevación [msnm]')
    plt.title('Perfil de elevación de la ruta')
    plt.show()
        
    


#Startability. Para hacerla variar hay que cambiar ficha camión. 
start=(tmax*pd*p1*1000/(2*np.pi*(dneuma*0.0245/2)))/(10.7*pbv*1000)

#print('startability del camión es' , start)
    
#       
columnvelo(viajelimpio)            
#
pestimada(40,viajelimpio) 
#
agrega_time(viajelimpio)
#

agregaconsumo(viajelimpio,354)   
#


sumaconsumo = sum(viajelimpio[15])

perfil_elev(viajelimpio)

print('El consumo de combustible es',sumaconsumo,'[lt]')

largoruta=viajelimpio[5][len(viajelimpio[0])-1]/1000 #En kilómetros
print('El largo de la ruta es', largoruta, '[km]')

print('El rendimiento obtenido es de', largoruta/sumaconsumo, '[km/lt]')

viajelimpio.append([0]*len(viajelimpio[0]))
viajelimpio[18][0]=(largoruta/sumaconsumo)

print('La máxima potencia necesaria es', max(viajelimpio[13]),'[hp]')
viajelimpio.append([0]*len(viajelimpio[0]))
viajelimpio[19][0]=max(viajelimpio[13])

print('El tiempo del viaje es', sum(viajelimpio[14]),'[hr]')
viajelimpio.append([0]*len(viajelimpio[0]))
viajelimpio[20][0]=sum(viajelimpio[14])

import pandas as pd

df2=pd.DataFrame(viajelimpio,index=['lat','long','slope(%)','slopecorre(%)','sloperedon(%)','dist[m]','interval[m]','velo[km/h]','encontrado','pot rodadura[hp]','pot aero[hp]','pot inercia[hp]','pot pendiente[hp]','potencia[hp]','tiempo[hr]','consumo[l]','dx[m]','elevación[m]','rendimiento[km/l]','potmax [hp]','tiempo [hr]'])  

df2_t=df2.transpose()   



df2_t.to_excel("354hp_25abril_linares-parral_40t_f12_crcdpes.xlsx")   
     


        
             
                
