import random as rm
import math as mt

#formulas fisicas
def polar (r,direction):
    y = r*mt.sin(mt.radians(direction))
    x = r*mt.cos(mt.radians(direction))
    return x, y    
def time(angle, speed):
    time =  ((2*speed)/9.81)*mt.sin(mt.radians(angle*2))
    return abs(time)
def distance(x1, y1, x2, y2):
    de = mt.sqrt((mt.pow((x2-x1), 2)) + (mt.pow((y2-y1), 2)))
    return de

#formulas de bits
def binario(binario):
    posicion = 0
    decimal = 0
    binario = binario[::-1]
    for digito in binario:
        multiplicador = 2**posicion
        decimal += int(digito) * multiplicador
        posicion += 1
    return decimal
def generar_cadena_binaria(longitud):
    cadena = []
    for _ in range(longitud):
        bit = rm.choice([0, 1])
        cadena.append(bit)
    return cadena

#objetos
class target:
     def __init__(this, positionx, positiony):
        this.positionx = positionx
        this.positiony = positiony
    
class tank:
    def __init__(this, positionx, positiony):
        this.chain = 0
        this.positionx = positionx
        this.positiony = positiony
        this.positionz = 0
        this.angle = 0
        this.aimx = 0
        this.aimy = 0
        this.time = 0
        this.direction = 0
        this.speed = 0
        
    def shoot(self, angle, speed, direction):
        speed = speed + 10
        xmax =  ((speed*speed)*mt.sin(mt.radians(angle*2)))/9.81
        x, y = polar(xmax, direction)
        x += self.positionx 
        y += self.positiony 
        self.time = time(angle, speed)
        self.aimx = x
        self.aimy = y
        self.direction = direction
        self.angle = angle
        self.speed = speed   
        

#generacion de individuos
def single():
    bc = generar_cadena_binaria(43)
    a = binario(bc[:9])
    b = binario(bc[10:19])
    c = binario(bc[20:28])
    d = binario(bc[29:37])
    e = binario(bc[38:])
    if(bc[19] == 0):
        c *= -1 
    if(bc[28] == 0):
        d *= -1
    guy = tank(c, d)
    guy.shoot(a, e, b)
    guy.chain = bc
    return guy 
def individual(bc):
    a = binario(bc[:9])
    b = binario(bc[10:19])
    c = binario(bc[20:28])
    d = binario(bc[29:37])
    e = binario(bc[38:])
    if(bc[19] == 0):
        c *= -1 
    if(bc[28] == 0):
        d *= -1
    guy = tank(c, d)
    guy.shoot(a, e, b)
    guy.chain = bc
    return guy 
def population(size):
    guy = []
    for i in range(size):
        guy.append(single())
    return guy
def targetmaker():
    targetA =  target(rm.randint(0,264),rm.randint(0,264))
    return targetA


#evaluacion
def assess(population, target):
    distances = []
    for i in range(len(population)):
        distances.append(distance(population[i].aimx, population[i].aimy, target.positionx,target.positiony))     
        distances[i] = 1/(distances[i]+1)
    return distances

def fit(assess):
    p =  []
    total = 0
    for i in range(len(assess)):
        total += assess[i]
    for i in range(len(assess)):
        p.append(assess[i]/total)
    return p

#seleccion de los mejores
def select(population, fit):
    sub2, sub = 0,0 
    total_fitness = sum(fit)
    probabilities = [f / total_fitness for f in fit]
    sub = rm.choices(population, probabilities)[0]
    while True:
        sub2 = rm.choices(population, probabilities)[0]
        if sub2 != sub:
            break
    return sub, sub2
    
#modificacion
def cross(ind, ind2):
    n = len(ind.chain)
    point = rm.randint(0,n)
    desc1 = individual(ind.chain[0:point] + ind2.chain[point:])
    desc2 = individual(ind2.chain[0:point] + ind.chain[point:])
    return desc1, desc2
def mutation(ind):
    point = rm.randint(0,len(ind.chain) - 1)
    des = ind.chain
    if(des[point] == 0):
        des[point] = 1
    else:
        des[point] = 0
    indn = individual(des)
    return indn

    
    
#1/value+1
print(fit(assess(population(5), targetmaker())))
a= population(10)
c = targetmaker()
b = fit(assess(a, c))
print(select(a, b))


def _AE(size, cicles):
    trgt = targetmaker()
    pption = population(size)
    check = False
    print("El objetivo está en x:", trgt.positionx, "y:", trgt.positiony)
    for i in range(cicles):
        ev = assess(pption, trgt)
        ft = fit(ev)
        npopulation = []
        for j in range(int(size/2)):
            ind, ind2 = select(pption, ft)
            ind, ind2 = cross(ind, ind2)
            ind2 = mutation(ind2)
            npopulation.append(ind)
            npopulation.append(ind2)
        pption = npopulation
        pption = npopulation  
    for i in range(size):
        if (ev[i] > .95 ):
                definitive = npopulation[i]
                check = True
                break
    if(check == True):
        print("El tanque de la posición x:", definitive.positionx, "y:", definitive.positiony, 
                "\nDispara en dirección", definitive.direction, "con un ángulo de", definitive.angle, 
                "a una velocidad de", definitive.speed, "\nAcertando en x:",  definitive.aimx, "y:", definitive.aimy
                )
        return definitive
    else:
        print("No se han encontrado un tanque, pruebe aumentar los ciclos o la poblacion")

        

    
_AE(100,1000)
          