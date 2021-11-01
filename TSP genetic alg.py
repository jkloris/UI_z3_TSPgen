import random
import math
from tkinter import *
MAP_SIZE = [200, 200]
CITIES = 30

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

    def mutate(self):
        r = random.randint(0,len(self.vector)-2)
        tmp = self.vector[r]
        self.vector[r] = self.vector[r+1]
        self.vector[r+1] = tmp



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

def createNewGeneration(map, routes):
    routes.sort(key=lambda x: x.fitness)
    newGeneration = []
    for i in range(int(len(routes)/2)):
        kid = breed(routes[i],routes[i+1])
        if i == 3:
            kid.mutate()
        kid.calcFitness(map)
        newGeneration.append(kid)
        kid = breed(routes[i+1], routes[i])
        if i == 6:
            kid.mutate()
        kid.calcFitness(map)
        newGeneration.append(kid)

    return newGeneration

def createNewGeneration2(map, routes):
    routes.sort(key=lambda x: x.fitness)
    newGeneration = []
    for i in range(int(len(routes)/2)):
        kid = breed(routes[i],routes[i+1])
        kid.calcFitness(map)
        newGeneration.append(kid)
        kid = breed(routes[i], routes[len(routes) - i-1])
        kid.calcFitness(map)
        newGeneration.append(kid)

    return newGeneration

def breed(mum, dad):
    r1 = random.randint(0,len(mum.vector)-1)
    r2 = random.randint(0,len(mum.vector)-1)
    i1 = mum.vector.index(r1)
    i2 = mum.vector.index(r2)
    if i1 < i2:
        gene = mum.vector[i1:i2]
        pos = i2

    else:
        gene = mum.vector[i2:i1]
        pos = i1

    for d in range(len(dad.vector) - len(gene)):
        while dad.vector[pos] in gene:
            pos = pos + 1 if pos + 1 < len(dad.vector) else 0
        gene.append(dad.vector[pos])

    return Route(gene)

def drawMap(map, best,canvas):
    a=2
    b = 300
    for i in best.vector:
        canvas.create_oval(b+a*map.cities[i][0],b+a*map.cities[i][1],b+a*map.cities[i][0]+4,b+a*map.cities[i][1]+4,fill="red")
        if best.vector[i] != best.vector[-1]:
            canvas.create_line(b+a*map.cities[i][0],b+a*map.cities[i][1],b+a*map.cities[i+1][0],b+a*map.cities[i+1][1])
            canvas.create_text(b+a*map.cities[i][0],b+a*map.cities[i][1],text=best.vector[i])
        else:
            canvas.create_line(b+a*map.cities[i][0], b+a*map.cities[i][1], b+a*map.cities[0][0], b+a*map.cities[0][1])
def main():
    root = Tk()
    root.geometry("2000x800")
    canvas = Canvas(root, width = 1900, height = MAP_SIZE[1]*4)
    canvas.pack()
    y = 0
    map = Map(MAP_SIZE[0], MAP_SIZE[1], CITIES)

    routes = generatePermutations(80, CITIES, map)
    best = routes[0]
    for i in range(1900):
        x = min(routes, key=lambda a: a.fitness)
        canvas.create_oval(y,x.fitness/4,y+2,x.fitness/4+2)
        y+=1

        if best.fitness > x.fitness:
            best=x

        routes = createNewGeneration(map, routes)

    drawMap(map,best,canvas)

    root.mainloop()

if __name__ == '__main__':
    main()