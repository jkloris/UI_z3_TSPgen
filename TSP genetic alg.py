import random
import math
import sys
from tkinter import *
MAP_SIZE = [200, 200]
CITIES = 20
EK_RATE = 1
BP_RATE = 1
NG_RATE = 1
# E3_RATE = 1

class Route:
    def __init__(self, vector):
        self.vector = vector
        self.fitness = None

    def calcFitness(self, map):
        fitness = 0
        for i in range(len(self.vector) - 1):
            if map.dist[self.vector[i]][self.vector[i + 1]] == None:
                map.dist[self.vector[i]][self.vector[i + 1]] = calcDistance(map.cities[self.vector[i]], map.cities[self.vector[i + 1]])
            fitness += map.dist[self.vector[i]][self.vector[i + 1]]
        if map.dist[self.vector[0]][self.vector[i + 1]] == None:
            map.dist[self.vector[0]][self.vector[i + 1]] = calcDistance(map.cities[self.vector[0]], map.cities[self.vector[i + 1]])
        fitness += map.dist[self.vector[0]][self.vector[i + 1]]

        self.fitness = fitness
        return fitness

    def mutate(self,map):
        r = random.randint(0,len(self.vector)-2)
        tmp = self.vector[r]
        self.vector[r] = self.vector[r+1]
        self.vector[r+1] = tmp
        self.calcFitness(map)




class Map:
    def __init__(self, sizeX, sizeY, citiesN):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.cities = []
        self.generateRandomCities(citiesN)

        self.dist = []
        for i in range(citiesN):
            self.dist.append(citiesN*[None])

    def generateRandomCities(self, num):
        for i in range(num):
            x = random.randint(0, self.sizeX)
            y = random.randint(0, self.sizeX)
            while self.cities.count([x,y]) > 0:
                x = random.randint(0, self.sizeX)
                y = random.randint(0, self.sizeY)

            self.cities.append([x,y])

    def createTestCities(self): #!20 miest!
        self.cities = [[79, 177], [12, 108], [95, 25],[28, 52], [153, 113],[30, 31], [44, 110], [186, 13], [47, 63], [182, 50], [72, 136],[53, 126], [43, 96], [123, 65],[117, 97],
                      [43, 107],[166, 1], [178, 69],[6, 41], [ 16, 173]]

def calcDistance(city1, city2):
    x = math.floor(math.sqrt((city1[0] - city2[0] )**2 + (city1[1] - city2[1])**2))
    return x



def generatePermutations(num, citiesN, map):
    routes = []
    s=list(range(citiesN))

    for i in range(num):
        random.shuffle(s)
        while routes.count(s) > 0:
            random.shuffle(s)
        r = Route(s[:])
        r.calcFitness(map)
        routes.append(r)

    return routes

#metoda vyberu generacii - kombinovana
def createNewGeneration(map, routes):
    routes.sort(key=lambda x: x.fitness)
    newGeneration = []
    elitekidsRate = EK_RATE / 10
    badParentsRate = BP_RATE / 10
    newGenesRate = NG_RATE

    for i in range(int(len(routes)/ elitekidsRate)):
        kid = breed2BKv2(routes[i],routes[i+1])
        kid.calcFitness(map)
        newGeneration.append(kid)
        kid = breed2BKv2(routes[i+1], routes[i])
        kid.calcFitness(map)
        newGeneration.append(kid)

    for i in range(len(routes), int(len(routes)/ badParentsRate), -1):
        routes[i-1].mutate(map)
        # routes[i-1].calcFitness(map)
        newGeneration.append(routes[i-1])

    newGeneration = newGeneration + generatePermutations(int(len(routes)/ newGenesRate), len(map.cities), map)
    newGeneration.sort(key=lambda x: x.fitness)
    return newGeneration[:len(routes)]

#metoda vyberu generacii len z elitnych
def createNewGeneration2(map, routes):
    routes.sort(key=lambda x: x.fitness)
    newGeneration = []
    for i in range(int(len(routes)/2)):
        kid = breed2BKv2(routes[i], routes[i + 1])
        kid.calcFitness(map)
        newGeneration.append(kid)
        kid = breed2BKv2(routes[i + 1], routes[i])
        kid.calcFitness(map)
        newGeneration.append(kid)

    return newGeneration

# metoda vyberu generacii - ruleta, kde elitni preziju vyradovanie
def createNewGeneration3(map, routes):

    routes.sort(key=lambda x: x.fitness)
    newGeneration = []
    size = len(routes)
    elite = routes[:int(len(routes)/E3_RATE)]
    routes = routes[int(len(routes)/E3_RATE):]

    S = 0
    for i in range(int(len(routes))):
        S+=routes[i].fitness

    for k in range(int(len(routes)/2-1)):
        r = random.randint(0, S)

        s = 0
        for i in range(int(len(routes))):
            s += routes[i].fitness
            if s >= r:
                S-=routes[i].fitness
                routes.pop(i)
                break
    routes = elite+routes
    for i in range(len(routes)-1):
        kid = breed2BKv2(routes[i], routes[i + 1])
        kid.calcFitness(map)
        newGeneration.append(kid)
        kid = breed2BKv2(routes[i + 1], routes[i])
        kid.calcFitness(map)
        newGeneration.append(kid)

    newGeneration.sort(key=lambda x: x.fitness)

    return newGeneration[:size]

# metoda vyberu generacii - ruleta, kde elitni idu do dalsej generacie
def createNewGeneration4(map, routes, E3_RATE):

    routes.sort(key=lambda x: x.fitness)
    newGeneration = []
    size = len(routes)
    elite = routes[:int(len(routes)/E3_RATE)]
    routes = routes[int(len(routes)/E3_RATE):]

    S = 0
    for i in range(int(len(routes))):
        S+=routes[i].fitness

    for k in range(int(len(routes)/2-1)):
        r = random.randint(0, S)

        s = 0
        for i in range(int(len(routes))):
            s += routes[i].fitness
            if s >= r:
                S-=routes[i].fitness
                routes.pop(i)
                break
    routes = elite+routes
    for i in range(len(routes)-1):
        kid = breed2BK(routes[i], routes[i + 1])
        kid.calcFitness(map)
        newGeneration.append(kid)
        kid = breed2BK(routes[i + 1], routes[i])
        if i % (size-2*E3_RATE if size > 2*E3_RATE else 1) == 0:
            kid.mutate(map)
        kid.calcFitness(map)
        newGeneration.append(kid)

    newGeneration += elite
    newGeneration.sort(key=lambda x: x.fitness)

    return newGeneration[:size]

def breed2BK(mum, dad):
    r1 = random.randint(0,len(mum.vector)-1)
    r2 = random.randint(0,len(mum.vector)-1)
    i1 = mum.vector.index(r1)
    i2 = mum.vector.index(r2)
    if i1 < i2:
        kid = mum.vector[i1:i2]
        pos = i2

    else:
        kid = mum.vector[i2:i1]
        pos = i1

    for d in range(len(dad.vector) - len(kid)):
        while dad.vector[pos] in kid:
            pos = pos + 1 if pos + 1 < len(dad.vector) else 0
        kid.append(dad.vector[pos])

    return Route(kid)

def breed2BKv2(mum, dad):
    r1 = random.randint(0, len(mum.vector) - 1)
    r2 = random.randint(0, len(mum.vector) - 1)
    i1 = mum.vector.index(r1)
    i2 = mum.vector.index(r2)
    if i1 < i2:
        kid = mum.vector[i1:i2]
    else:
        kid = mum.vector[i2:i1]
        
    pos = 0
    for d in range(len(dad.vector) - len(kid)):
        while dad.vector[pos] in kid:
            pos = pos + 1 if pos + 1 < len(dad.vector) else 0
        kid.append(dad.vector[pos])

    return Route(kid)


def drawMap(map, best,canvas):
    a=2
    b = 300
    for i in best.vector:
        canvas.create_oval(b+a*map.cities[i][0],b+a*map.cities[i][1],b+a*map.cities[i][0]+4,b+a*map.cities[i][1]+4,fill="red")
        if best.vector.index(i) < len(best.vector)-1:
            next = best.vector[best.vector.index(i)+1]
            canvas.create_line(b+a*map.cities[i][0],b+a*map.cities[i][1],b+a*map.cities[next][0],b+a*map.cities[next][1])
            canvas.create_text(b+a*map.cities[i][0],b+a*map.cities[i][1], font=("Purisa", 12), text=best.vector[i])
        else:
            canvas.create_line(b+a*map.cities[i][0], b+a*map.cities[i][1], b+a*map.cities[best.vector[0]][0], b+a*map.cities[best.vector[0]][1])


def main(E3_RATE):
    root = Tk()
    root.geometry("1500x700")
    canvas = Canvas(root, width = 1900, height = MAP_SIZE[1]*4)
    canvas.pack()
    y = 0
    map = Map(MAP_SIZE[0], MAP_SIZE[1], CITIES)
    map.createTestCities()

    routes = generatePermutations(50, CITIES, map)

    best = routes[0]

    remainCounter = 400
    generationCounter = 0
    while remainCounter > 0:
        generationCounter+=1
        x = min(routes, key=lambda a: a.fitness)
        # for a in routes:
        #     x+=a.fitness
        # x = int(x/len(routes))
        canvas.create_oval(y,x.fitness/4,y+2,x.fitness/4+2)
        y+=1

        if generationCounter % 100 == 0:
            E3_RATE+=1

        remainCounter-=1
        if best.fitness > x.fitness:
            best=x
            remainCounter = 500

        routes = createNewGeneration4(map, routes, E3_RATE)
        # routes = createNewGeneration(map, routes)

    drawMap(map,best,canvas)
    print(best.fitness, best.vector)
    print(E3_RATE)
    root.mainloop()


if __name__ == '__main__':
    # EK_RATE = int(sys.argv[1])
    # BP_RATE = int(sys.argv[2])
    # NG_RATE = int(sys.argv[3])
    EK_RATE = 2
    BP_RATE = 2.3
    NG_RATE = 7
    E3_RATE = 7
    main(E3_RATE)