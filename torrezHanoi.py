import math
import time


#L�gica:
#Voy a asignar un valor num�rico a cada disco como 2 ^ n. El primer disco (el m�s peque�o) tendr� un valor de 2, un segundo valor de disco de 4, 
#un tercer valor de disco de 8, un cuarto valor de disco de 16, etc.
#Valor num�rico de cualquier disco = 2 ^ (n)
#El valor de cada clavija (polo) ser� la suma de todos los valores de disco en esa clavija en un momento dado. Por ejemplo, si la clavija tiene 
#actualmente el Disco 1 y 3, entonces el valor de esa clavija es 2 + 8 = 10
#El valor de todos los discos ser� 2 ^ 1 + 2 ^ 2 .... 2 ^ (n) = (2 ^ n) - 2. Por ejemplo, el valor total de 4 discos ser� 2 ^ 4 - 2 = 30   
#Estoy usando el operador "Bitwise And" para decidir si existe un disco dado en la clavija. Por ej.
#    -si el valor de la clavija es 20 (Disco 2 y 4), entonces 20 "Bitwise Y" 2 ser� igual a 0, lo que significa que la clavija no tiene el Disco 1
#    -si el valor de la clavija es 20 (Disco 2 y 4), entonces 20 "Bitwise Y" 4 ser� igual a 4, lo que significa que la clavija tiene el Disco 2
#Para verificar si no estoy colocando un disco m�s grande encima del disco m�s peque�o, utilic� el operador M�dulo (encontrar el resto). Por ej.
#    -si la clavija tiene un valor de 18 (Disco 1 y 4), entonces 18% 4 ser� 2, lo que significa que no puedo colocar el Disco 2 en esta clavija
#    -si la clavija tiene un valor de 24 (Disco 3 y 4), entonces 24% 4 ser� 0, lo que significa que puedo colocar el Disco 2 en esta clavija
#'' '

# Best First Search utilizar� la l�gica �ltima entrada, primera salida. De esa forma, vamos a seguir profundizando (verticalmente) antes de buscar estados horizontales.
def Solve_By_BestFS(n):
    # Declarar variables
    # Valores de cada clavija o pivote
    peg1_value = peg2_value = peg3_value = 0

    # Lista para almacenar los estados adyacentes
    state_COLLECTION = []

    # lista utilizada para guardar las acciones que hemos realizado hasta para cada elemento en la lista anterior, para que podamos rastrear. El tama�o de esta lista siempre ser� el mismo que el de otra lista de COLECCI�N
    steps_till_now_COLLECTION = []

    # Esta lista es para almacenar los estados que ya hemos encontrado, para que no entremos en un ciclo infinito
    past_states = []

    # variables temporales para almacenar los pasos para el estado de trabajo actual y el siguiente estado adyacente
    steps_till_current_state = steps_till_next_state = []

    # Variable temporal para almacenar el valor del disco que se mueve
    Value_of_Disk = 0

    # Variable temporal para almacenar el estado actual y el siguiente estado adyacente
    current_state = new_state = []

    # Variable temporal para almacenar el disco que se mueve
    disk_on_top = 0

    # Variables Booleanas
    state_found_before = solution_found = False

    # Encuentra el valor total de todos los discos en funci�n de n n�mero de discos
    Value_of_All_Disks = int(math.pow(2, n + 1)) - 2

    # Estado inicial donde todos los discos est�n en Peg1. Debido a que las listas est�n indexadas comenzando por 0, simplemente ignoraremos el �ndice 0.
    current_state = [0, Value_of_All_Disks, 0, 0]

    # Inserte el estado inicial en la lista COLECCI�N
    state_COLLECTION.append(current_state)
    steps_till_now_COLLECTION.append(steps_till_current_state)
    past_states.append(current_state)

    # Bucle hasta encontrar la soluci�n
    while solution_found == False and len(state_COLLECTION) > 0:
        # Obtenga el MEJOR estado en la pila
        best_item = - 1
        for item in range(0,len(state_COLLECTION)):
            state = state_COLLECTION[item]
            for d in range(n-1, 0, -1):
                partial_solution_val = math.pow(2, d+1)-2
                if ((n+d)%2 == 0):
                    partial_solution_peg = 3
                else:
                    partial_solution_peg = 2
                if (state[partial_solution_peg] == partial_solution_val):
                    best_item = item
                    break
            if (best_item > -1):
                break
        if best_item == -1:
            best_item = 0

        current_state = state_COLLECTION.pop(best_item)
        # Obtenga los pasos correspondientes en la l�gica de COLECCI�N
        steps_till_current_state = steps_till_now_COLLECTION.pop(best_item)
        # Bucle todas las clavijas para la fuente para el movimiento del disco
        for source_peg in range(3, 0, -1):
            # si la clavija no tiene disco a partir de ahora, pase a la siguiente clavija
            if (current_state[source_peg] == 0):
                continue
            # Bucle todas las clavijas para el destino para el movimiento del disco
            for dest_peg in range(3, 0, -1):
                # Source Peg y Dest Peg no pueden ser iguales
                if (solution_found == True or source_peg == dest_peg):
                    continue
                # Bucle para cada tama�o de disco de peque�o a grande
                for disk_size in range(1, n + 1):
                    Value_of_Disk = int(math.pow(2, disk_size))
                    # Utilizando el operador Y Bitwise, encuentre el disco en la parte superior de esta clavija de origen
                    if ((current_state[source_peg] & Value_of_Disk) == Value_of_Disk):
                        disk_on_top = disk_size
                        break
                # La clavija de destino debe estar vac�a o el disco superior debe ser m�s grande que el disco que se est� moviendo
                if (current_state[dest_peg] == 0 or current_state[dest_peg] % Value_of_Disk == 0):
                    # Los siguientes pasos mueven el disco de origen a destino y crean un nuevo estado fuera del estado actual
                    new_state = list(current_state)
                    new_state[source_peg] = new_state[source_peg] - Value_of_Disk
                    new_state[dest_peg] = new_state[dest_peg] + Value_of_Disk
                    next_step = [disk_on_top, source_peg, dest_peg]
                    steps_till_next_state = list(steps_till_current_state)
                    steps_till_next_state.append(next_step)
                    # Compruebe si el nuevo estado es la soluci�n final que estamos buscando (todos los discos en la clavija 3)
                    if (new_state[3] == Value_of_All_Disks):
                        steps = 1
                        output = ""
                        for aseq in steps_till_next_state:
                            output = output + str(steps) + ": Move Disk " + str(aseq[0]) + " From " + str(
                                aseq[1]) + " To " + str(aseq[2]) + "\n"
                            steps = steps + 1
                        print(output)
                        solution_found = True
                        return
                    # else - todav�a no encontramos la soluci�n
                    else:
                        # aseg�rese de que el nuevo estado no se haya descubierto antes
                        state_found_before = False
                        for past_state in past_states:
                            if (past_state[1] == new_state[1] and past_state[2] == new_state[2] and past_state[3] ==
                                new_state[3]):
                                state_found_before = True
                                break
                        # si este es el nuevo estado que descubrimos antes, luego agr�guelo a las listas de COLECCI�N
                        if state_found_before == False:
                            state_COLLECTION.append(new_state)
                            steps_till_now_COLLECTION.append(steps_till_next_state)
                            past_states.append(new_state)
                            
if __name__ == "__main__":
    n = int(input("Ingrese el numero de discos"))
    start_time=time.time()
    print ("Resolver por el mejor metodo de primera busqueda:")
    Solve_By_BestFS(n)
    tiempo_ejecucion=time.time()-start_time
    print("\nEl tiempo de ejecucion del laberinto es", round(tiempo_ejecucion,6)," segundos")

#AYUDA = () len(INICIO+1)

#def hanoi(n, pivote_inicial, pivote_final, pivote_auxiliar):
#    if(n == 1):
#        print(pivote_inicial+"->"+pivote_final)
#    else:
#        hanoi(n-1, pivote_inicial, pivote_auxiliar, pivote_final)
#        print(pivote_inicial+"->"+pivote_final)
#        hanoi(n-1, pivote_auxiliar, pivote_final, pivote_inicial)

#def main():
    
#    n = int(input("Presione un cantidad de discos: "))
#    pivoteIni = input("Estado del pivote Inicial: ")
#    pivoteAux = input("Estado del pivote Auxiliar: ")
#    pivoteFin = input("Estado del pivote Final: ")
#    hanoi(n, pivoteIni, pivoteAux, pivoteFin)

#if __name__ == '__main__':
#    main()
# coding=utf-8

#import time


## Dibuja las torres.
#def dibujarTorres():
#    for fila in torres:
#        for col in fila:
#            if col == 0:
#                print("            |            ", end="")
#            elif col == 1:
#                print("          [///]          ", end="")
#            elif col == 2:
#                print("         [/////]         ", end="")
#            elif col == 3:
#                print("        [///////]        ", end="")
#            elif col == 4:
#                print("       [/////////]       ", end="")
#            elif col == 5:
#                print("      [///////////]      ", end="")
#            elif col == 6:
#                print("     [/////////////]     ", end="")
#            elif col == 7:
#                print("    [///////////////]    ", end="")
#        print()
#    print("="*77)
#    print("            1                        2                        3            ")
#    time.sleep(1)

## Nos devuelve el disco de arriba de la columna col, sino devuelve 0.
#def buscarDiscoArriba(col):
#	fila = 0
#	while fila <= discos and torres[fila][col] == 0:
#		fila += 1
#	if fila <= discos:
#		return torres[fila][col]
#	else:
#		return 0

## Nos devuelve el espacio vacio de arriba de la columna col.
#def buscarEspacioArriba(col):
#	fila = 0
#	while fila <= discos and torres[fila][col] == 0:
#		fila += 1
#	return fila - 1

## Elimina el disco de arriba de la columna col.
#def eliminarDiscoArriba(col):
#    fila = 0
#    while fila <= discos and torres[fila][col] == 0:
#        fila += 1
#    torres[fila][col] = 0

## Representaci�n gr�fica.
#def hanoiGrafico(n, origen=1, auxiliar=2, destino=3):

#    if n > 0:
#        hanoiGrafico(n-1, origen, destino, auxiliar) # n-1 discos de la torre origen a la torre auxiliar.
#        disco = buscarDiscoArriba(origen-1)
#        eliminarDiscoArriba(origen-1)
#        torres[buscarEspacioArriba(destino-1)][destino-1] = disco
#        print("\n"*40)
#        dibujarTorres()
#        hanoiGrafico(n-1, auxiliar, origen, destino) # n-1 discos de la torre auxiliar a la torre final.

## Representaci�n en modo texto.
#def hanoiTexto(n, origen=1, auxiliar=2, destino=3):

#    if n > 0:
#        hanoiTexto(n-1, origen, destino, auxiliar) # n-1 discos de la torre origen a la torre auxiliar.
#        print("Se mueve el disco %d de torre %d a la torre %d" % (n, origen, destino)) # disco n a la torre destino.
#        hanoiTexto(n-1, auxiliar, origen, destino) # n-1 discos de la torre auxiliar a la torre final.

#print("\n"*40)
#print("     TORRES DE HANOI     ")
#print("*"*25)
#modo = int(input("Ingrese la opcion deseada:\n\n1) Modo grafico\n2) Modo texto\n\n"))

#if modo == 1:
#    discos = int(input("\nIngrese entre 1 y 7 discos: "))

#    # Defino la matriz para el gr�fico
#    if discos > 0 and discos < 8:
#        if discos == 1:
#            torres = [[0,0,0],[1,0,0]]
#        elif discos == 2:
#            torres = [[0,0,0],[1,0,0],[2,0,0]]
#        elif discos == 3:
#            torres = [[0,0,0],[1,0,0],[2,0,0],[3,0,0]]
#        elif discos == 4:
#            torres = [[0,0,0],[1,0,0],[2,0,0],[3,0,0],[4,0,0]]
#        elif discos == 5:
#            torres = [[0,0,0],[1,0,0],[2,0,0],[3,0,0],[4,0,0],[5,0,0]]
#        elif discos == 6:
#            torres = [[0,0,0],[1,0,0],[2,0,0],[3,0,0],[4,0,0],[5,0,0],[6,0,0]]
#        elif discos == 7:
#            torres = [[0,0,0],[1,0,0],[2,0,0],[3,0,0],[4,0,0],[5,0,0],[6,0,0],[7,0,0]]

#        print("\n"*40)
#        dibujarTorres()
#        hanoiGrafico(discos)
#    else:
#        print("\nERROR! Solo se permiten de 1 a 7 discos para el modo grafico.")
#elif modo == 2:
#    discos = int(input("\nIngrese numero de discos: "))

#    if discos > 0:
#        print()
#        hanoiTexto(discos)
#    else:
#        print("\nERROR! Ingrese un numero mayor a 0.")
#else:
#    print("\nERROR! La opcion ingresada es incorrecta.")
