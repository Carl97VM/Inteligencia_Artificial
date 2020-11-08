import random as rnd
import time as tm

class Cromosoma:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness

    def len(self):
        return len(self.genes)

    def __str__(self):
        s="%s %d" % (" ".join(map(str, self.genes)), self.fitness) # Agregar en el mapa las pocisiones
        s2=[] # Se crea una lista Vacia para asignarles valores
        n=len(self.genes) # Asignar el limite en esta variable depende del tamanio
        for i in range(n): # Recorrer
            s2.append(list("."*n)) # a S2 se le asigna la lista de puntos del tablero
            for k in range(n): # Recorrer
                if self.genes[k]==i: # Si genes en la pocision K es igual a I Proseguir
                    s2[i][k]="R" # Si No ubiera en choque en las rectas o ciagonales 
            s2[i]=" ".join(s2[i]) # Se le une a S2 los puntitos del tablero aparte de la pocision de la reyna

        return "\n".join(s2)+"\nfitness: " + str(self.fitness) # Devuelve S2 con la lista de pocion del tablero y reyna con lo del fitnes

class AGenetico:

    def __init__(self, casillas):
        self.casillas = casillas
        self.genes = range(casillas)
        #print("---------------")
        #print(self.genes)
        #print("---------------")

    def diagonales(self, gen, posicion):
        genesDiagonal1=[] # Vector o lista que abarce de isquierda a derecha
        genesDiagonal2=[] # Vector o lista que abarce de derecha a isquierda
        px=posicion+1 # Agarra la pocision aumentada
        py=gen+1 # Agarra los genes mas 1
        for x in range(self.casillas): # Recorre
            if x==posicion: # Si la pocision de x es igual a pocision actual
                genesDiagonal1.append(gen)  # Añadir a la diagonal el gen
                genesDiagonal2.append(gen)  # Añadir a la diagonal el gen
                continue
            y1 = (x-posicion)*((py-gen)/(px-posicion))+gen # Verificacion para saber si en la linea del gen si no hay choques o intersecciones para validar el movimineto
            y2 = (x-posicion)*((py-gen)/((posicion-1)-posicion))+gen # Verificacion para Constatar de que no hayan choques
            if y1>=0 and y1<self.casillas and y1!=gen: # Verificacion de que si no hay igualdad en las filas  desde la pocision 0 hasta el limite y si es difernete del limite
                genesDiagonal1.append(y1) # Añadir a la diagonal el valor de Y1
            else:
                genesDiagonal1.append(-1) # Añadir a la diagonal el valor de menos 1
            if y2>=0 and y2<self.casillas and y2!=gen: # Verificacion de que si en y2 desde 0 hasta el limite y que sea diferente del gen
                genesDiagonal2.append(y2) # Añadir a la diagonal 2 y2
            else:
                genesDiagonal2.append(-1) # Añadir a la diagonal el valor de menos 1
        return genesDiagonal1, genesDiagonal2 # Devolver las diagonales

    def fidoneidad(self, genes):# Funcion de Fitnes
        fitness=0
        i=0
        for k in range(len(genes)): # Recorrer en k los el tamaño de los genes
            diagonal1, diagonal2 = self.diagonales(genes[k], k) # Asignar  a las diagonales como valor privado los genes 
            for i in range(len(genes)): # Recorrer en i el tamaño de los genes
                if genes[k]==genes[i]:   # reina en horizontal verificacion de no coincidencias y de opctimizacion
                    continue
                elif (len(diagonal1)>i and genes[i]==diagonal1[i]) or (len(diagonal2)>i and genes[i]==diagonal2[i]): # reina en diagonal verificacion de no coincidencias y de opctimizacion
                    continue
                else:
                    fitness+=1 # Decir de que el fitnes esta bien en esta funcion para comparacion de caminos
        return fitness

    def nuevoPadre(self): # Funcion de Nuevos Padres
        genes = rnd.sample(self.genes, self.casillas) # A los genes se les asigna un randonico de los genes y de las casillas
        fitness=self.fidoneidad(genes) # Evaluacion de fitnes con los genes
        return Cromosoma(genes, fitness) # Devolver el cromosoma con los genes y viendo si cumple con el fitnes

    def reproducir(self, x, y): # Funcion de reporduccion
        c=rnd.randint(0, x.len()) # A c de le asigna un randonico entre 0 y el tamaño de x
        genes=x.genes[:c]+y.genes[c:] # A los genes  de le asigna la  asociacion de los genes de X hasta el final Mas los de y hasta el final
        fitness=self.fidoneidad(genes) # Evaluacion del fitnes con los genes
        return Cromosoma(genes, fitness) # Devuelve Cromosomas con comparacion de Fitnes

    def mutar(self, hijo): # Funcion de mutacion
        n=rnd.randint(0, hijo.len()-1) # Asignacion de un randonico en radianes desde 0 hasta el tamaño del hijo -1
        genes=hijo.genes # A genes se le asigna la extencion de genes con el hijo
        genes[n]=-1 # Genes un arreglo de tamaño n asignandole -1
        genX=genY=max(genes) # a gen x Y y se les asigna un maximo de genes
        while genX in genes and genY in genes: # Mientras los genes de x esten en y y los Genes de Y en los genes
            genX, genY = rnd.sample(self.genes, 2) # Se les asigna a los Genes de x Y y un randonico con maximo de dos decimales
        genes[n]= genX if genX in genes else genY # A los genes limitados por n se le asigna si El gen X esta dentro de los genes sino El Gen Y
        hijo.fitness=self.fidoneidad(genes) # Al hijo con la prueba de Fitnes en base de los genes para ver si cumple
        hijo.genes=genes # Asignacion de genes a Hijo de genes
        return hijo

    def seleccion(self, poblacion): #Funcion de seleccion
        if len(poblacion)>0: # Si el tamaño de la poblacion es mayor a 0, obiamente si
            return rnd.choice(poblacion) # Devuelve un randonico de la busqueda para la poblacion
        else:
            return self.nuevoPadre() # Sino fuera el caso Volvemos a Nuevos Padres


    def algoritmo(self, poblacion):

        while True:
            npobla=[]
            for i in range(len(poblacion)):
                x=self.seleccion(poblacion)
                y=self.seleccion(poblacion)
                hijo=self.reproducir(x, y)
                if rnd.randint(1, 20)<3:
                    hijo=self.mutar(hijo)
                npobla.append(hijo)
                if npobla[i].fitness>=(self.casillas*self.casillas-self.casillas):
                    return npobla[i]
            poblacion=npobla


    def run(self):
        poblacion=[]
        for i in range(350):
            poblacion.append(self.nuevoPadre())
        print(self.algoritmo(poblacion))

if __name__=="__main__":
    for n in [4, 5, 6, 7, 8, 9, 10]:
        t=tm.time()
        alg=AGenetico(n)
        alg.run()
        print(" %02.03f" % (tm.time()-t))
