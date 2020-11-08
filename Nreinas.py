
#UNIVERSITARIO: JUAN CARLOS VASQUEZ MACIAS
#ASIGNATURA: INTELIGENCIA ARTIFICIAL

from time import time
from itertools import combinations
from collections import OrderedDict
from copy import deepcopy

from io import StringIO

try:
    from string import uppercase
except ImportError:
    from string import ascii_uppercase as uppercase

from PSR import ProblemaPSR, backtrack, convertir_a_binario

class Casilla_: #Cada casilla del tablero de ajedrez 
    afectado = False #Afectacion de la casilla por otra casillas
    reina = False #Si la casilla tiene reina o no
    def __init__(self,afectado = False,reina = False): 
        self.afectado = afectado 
        self.reina = reina

    def setAfectado(self,afectado): 
        self.afectado = afectado

    def getAfectado(self): 
        return self.afectado
    def setReina(self,reina):
        self.reina = reina
    def getReina(self): 
        return self.reina

tablero = [] #Creacion de la matriz
for i in range(0,8):
    tablero.append([None])
    for j in range(0,8):
        tablero[i].append(None)
print(tablero)



#Inicializacion de objetos casillas
def reinicializacionTablero():
    global tablero 
    for i in range(0,len(tablero)):
        for j in range(0,len(tablero)):
            tablero[i][j] = Casilla_(False,False) 
def casillasLibres():
	libres = 0
	for i in range(len(tablero)):
		for i in range(len(tablero)):
			#Casilla vacia
			if tablero[i][j].afectado == False and tablero[i][j].reina == False:
				libres += 1 #Significa que la casilla esta libre y se aumenta la variable que indica cuantas lo estan
	return libres #Retorna el numero de casillas libres	            
def primeraReina():
    pos = ""
    for i in range(8):
        for j in range(8):
            if(tablero[i][j].getReina()):
                pos = str(i) + str(j)
                return pos

def solucionado():
    num_reinas = 0
    for i in range(8):
        for j in range(8):
            if(tablero[i][j] != False):
                num_reinas +=1
    if(num_reinas == 8):
        return False
    else:
        return True             

reinas = 8
primerPos = ""

def afectarCasillas(row,column):
	b = False
	referenceRow = 0; referenceColumn = 0 #Variables locales de indice
	#up (afect)
	referenceRow = row; referenceColumn = column #Asignacion de los indices
	while(b == False):
		referenceRow -=1 #Se decrementa los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
			break
	b = False
	#down (afect)
	referenceRow = row; referenceColumn = column #Asignacion de los indices
	while(b == False):
		referenceRow -=1 #Se decrementa los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
			break
	b = False
	#left (afect)
	referenceRow = row; referenceColumn = column #Asignacion de los indices
	while(b == False):
		referenceColumn -= 1 #Se decrementa los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
			break
	b = False
	#rigth (afect)
	referenceRow = row;#Asignacion de los indices
	while(b == False):
		referenceColumn += 1 #Se decrementa las los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
	b = False
	#up-left (afect)
	referenceRow = row; referenceColumn = column #Asignacion de los indices
	while(b == False):
		referenceRow -=1; referenceColumn -= 1 #Se decrementa las los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
	b = False
	#up-rigth (afect)
	referenceRow = row; referenceColumn = column #Asignacion de los indices
	while(b == False):
		referenceRow +=1; referenceColumn += 1 #Se decrementa las los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
			break
	b = False
	#down-left (afect)
	referenceRow = row; referenceColumn = column #Asignacion de los indices
	while(b == False):
		referenceRow +=1; referenceColumn -= 1 #Se incrementan las los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
			break
	b = False
	#down-rigth (afect)
	referenceRow = row; referenceColumn = column #Asignacion de los indices
	while(b == False):
		referenceRow +=1; referenceColumn += 1 #Se decrementa las los indices
		try:
			tablero[referenceRow][referenceColumn].afectado = True
		except IndexError as e:
			b = True
			break



#Bucle principal
while(solucionado()):
	num_libres = casillasLibres() #Asigna a num_libres el numero de casillas vacias que hay en el tablero
	bel = 't'
	while(reinas > 0):
		for i in range(8):
			for j in range(8):
				#Caso de casilla libre
				if(tablero[i][j].getAfectado()==False and tablero[i][j].getReina()==False):
					tablero[i][j].setReina(True) #Se pone una reina en la casilla
					afectarCasillas(i,j) #Afecta todas las casillas relacionadas con la casilla actual
					reinas -= 1 #Disminuye el numero de reinas que faltan
				else:
					num_libres = casillasLibres() #Asigna el numero de casillas libres
					if(num_libres > reinas):
						bel = 'f'
						primerPos = primeraReina() #Asigna en un string los indices en el que se encuentra la primera reina
						break
			if(bel == 'f'):
				break
		if(bel == 'f'):
			break
	if(bel == 'f'):
		reinicializacionTablero()
		fil = int(primerPos[0])
		col = int(primerPos[1])
		tablero[fil][col].setAfectado(True);
		reinas = 8
	else:
		continue


def imprimiendoSolucion():
	print("SOLUCION: ")
	for i in range(0,8):
		for j in range(0,8):
			if(tablero[i][j].getReina()):
				print(" [R] ",end="")
			else:
				print(" [ ] ",end="")
		print(""); print("")

def mostrar_solucion(sol):
    for i in uppercase[:9]:
        print(" ".join([str(sol["%s%d" % (i, j)]) for j in range(1, 10)]))
if(main):	
	my_problem = ProblemaPSR(variables, dominios0, restricciones)
	sol = backtrack(my_problem)#Realiza la vuelta atras para optimizacion
	mostrar_solucion(sol)#Imprime toda la solcion de la matriz
	imprimiendoSolucion()#Muestra estado de la solucion 
