#ex1
import random
def ex1():
    r=3
    b=4
    bl=2
    z=random.randint(1,6)
    if z==2 or z==3 or z==5:
        bl=bl+1
    elif z==6:
        r=r+1
    else:
        b=b+1

    total=["red"]*r+["blue"]*b+["black"]*bl
    return random.choice(total)

#a
x=ex1()
print(x)

#b

suma=0
for i in range(12000):
    if ex1()=="red":
        suma=suma+1

print(suma/12000)

#ex2
import numpy as np
import matplotlib.pyplot as plt
l=[1,2,5,10]

#2.1

x1=np.random.poisson(lam=1,size=1000)
x2=np.random.poisson(lam=2,size=1000)
x3=np.random.poisson(lam=5,size=1000)
x4=np.random.poisson(lam=10,size=1000)

#print(x1,x2,x3,x4)

#2.2

ales=np.random.choice(l,size=1000,)
xr=np.array([np.random.poisson(lam=l) for l in ales])

#a
#descrescatoare
#plt.hist(xr,bins=None,range=None,density=False,histtype='bar',color="purple",label=None)
#towers/linii care sunt mari la val mici
#plt.hist(x1,bins=None,range=None,density=False,histtype='bar',color="green",label=None)
#towers mai unite putin
#plt.hist(x2,bins=None,range=None,density=False,histtype='bar',color="pink",label=None)
#towers unite ca un clopot dar nu chiar
#plt.hist(x3,bins=None,range=None,density=False,histtype='bar',color="blue",label=None)
#full on clopot
#plt.hist(x4,bins=None,range=None,density=False,histtype='bar',color="red",label=None)

#b

#distributia aleatorie este complet descrescatoare(nu urca inapoi) si contine toate valorile
#numarul de apeluri poate fi influentat de la o zi la alta din cauza incertitudinii de la lambda
plt.show()