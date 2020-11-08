
# Código con poda alfabeta con eleccion de minimax
# 3 en Raya de otra manera 
# Laboratorio #6
# inteligencia artificial
# Universitario: Juan Carlos Vasquez Macias 

import random
from pip._vendor.distlib.compat import raw_input #https://pypi.org/project/picage/
'''
picage proporciona una interfaz de estilo de objeto para manejar la estructura del archivo / módulo del paquete Python. Te da una API simple para acceder:

un nombre completo, nombre corto de un módulo de Python
padre, subpaquetes y submódulos
recorre recursivamente todos los subpaquetes y submódulos
Nota

Python es un lenguaje de programación tipo Dyanamic, todo en Python es un objeto, incluido el paquete y el módulo de Python.
'''


def Obtener_copia_Tablero(tablero):#Generara una copia del tablero para poder editar en el y no asi en el original
    tablero_Copiado = []

    for i in tablero:
        tablero_Copiado.append(i)
    return tablero_Copiado


def Mesa_Dibujo(tablero):
    copia_tablero = Obtener_copia_Tablero(tablero)

    for i in range(1, 10):
        if tablero[i] == '':
            copia_tablero[i] = str(i)
        else:
            copia_tablero[i] = tablero[i]

    print("\n")
    print(' ' + copia_tablero[7] + '  |  ' + copia_tablero[8] + '  |  ' + copia_tablero[9])
    print('---------------')
    print(' ' + copia_tablero[4] + '  |  ' + copia_tablero[5] + '  |  ' + copia_tablero[6])
    print('---------------')
    print(' ' + copia_tablero[1] + '  |  ' + copia_tablero[2] + '  |  ' + copia_tablero[3])
    print("\n")


def retornar_letra_jugador():
    letra = ''
    while letra != 'X' and letra != 'O':
        print(' \nAntes de nada, defina que ficha usara X o O?')
        letra = raw_input().upper()
        if letra != 'X' and letra != 'O':
            print("\nOpcion inválida! \n"
                  "Entre con la letra 'X' o 'X'\n "
                  "ou con la letra 'O' o 'o'!")

    if letra == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def juega_primero():
    if random.randint(0, 1) == 0:
        return 'computador'
    else:
        return 'jugador'


def realizar_movimiento(tablero, letra, movimiento):
    tablero[movimiento] = letra


def ganador(brd, let):
    return ((brd[7] == let and brd[8] == let and brd[9] == let) or
            (brd[4] == let and brd[5] == let and brd[6] == let) or
            (brd[1] == let and brd[2] == let and brd[3] == let) or
            (brd[7] == let and brd[4] == let and brd[1] == let) or
            (brd[8] == let and brd[5] == let and brd[2] == let) or
            (brd[9] == let and brd[6] == let and brd[3] == let) or
            (brd[7] == let and brd[5] == let and brd[3] == let) or
            (brd[9] == let and brd[5] == let and brd[1] == let))


def espacio_libre(tablero, movimiento):
    if tablero[movimiento] == '':
        return True
    else:
        return False


def obtener_movimiento_jugador(tablero):
    movimiento = ''
    while movimiento not in '1 2 3 4 5 6 7 8 9'.split() or not espacio_libre(tablero, int(movimiento)):
        print("\nCual sera su siguiente Movimineto? Escoja en los numeros\n "
              "del tablero de arriba (1 a 9).")
        movimiento = raw_input();
        if movimiento not in '1 2 3 4 5 6 7 8 9':
            print("\nOps, valor inválido!! Escoja uno de los movimientos validos de arriba\n "
                  "de 1 a 9.")

        if movimiento in '1 2 3 4 5 6 7 8 9':
            if not espacio_libre(tablero, int(movimiento)):
                print("\nEse espacio esta ocupado! \n"
                      "Escoja otro espacio entre 1 a 9,  nº\n"
                      " disponibles en el tablero.")

    return int(movimiento)


def escojer_movimiento_aleatorio(tablero, lista_movimientos):
    posibles_movimientos = []
    for i in lista_movimientos:
        if espacio_libre(tablero, i):
            posibles_movimientos.append(i)

    if len(posibles_movimientos) != 0:
        return random.choice(posibles_movimientos)
    else:
        return None


def tablero_lleno(tablero):
    for i in range(1, 10):
        if espacio_libre(tablero, i):
            return False
    return True


def posibles_opciones(tablero):
    opciones = []

    for i in range(1, 10):
        if espacio_libre(tablero, i):
            opciones.append(i)
    return opciones


def finalizar_juego(tablero, letra_computador):
    if letra_computador == 'X':
        letra_jugador = 'O'
    else:
        letra_jugador = 'X'

    if ganador(tablero, letra_computador):
        return 1

    elif ganador(tablero, letra_jugador):
        return -1

    elif tablero_lleno(tablero):
        return 0

    else:
        return None


# -----------------------------------------------------------------------------------------------------------------------
# AQUI EMPIEZA EL ALGORITMO  PODA ALFA-BETA
def alphabeta(tablero, letra_computador, rodada, alpha, beta):
    if letra_computador == 'X':
        letra_jugador = 'O'
    else:
        letra_jugador = 'X'

    if rodada == letra_computador:
        proxima_rodada = letra_jugador
    else:
        proxima_rodada = letra_computador

    fim = finalizar_juego(tablero, letra_computador)

    if fim is not None:
        return fim

    movimientos_posibles = posibles_opciones(tablero)

    if rodada == letra_computador:
        for movimiento in movimientos_posibles:
            realizar_movimiento(tablero, rodada, movimiento)
            val = alphabeta(tablero, letra_computador, proxima_rodada, alpha, beta)
            realizar_movimiento(tablero, '', movimiento)
            if val > alpha:
                alpha = val

            if alpha >= beta:
                return alpha
        return alpha

    else:
        for movimiento in movimientos_posibles:
            realizar_movimiento(tablero, rodada, movimiento)
            val = alphabeta(tablero, letra_computador, proxima_rodada, alpha, beta)
            realizar_movimiento(tablero, '', movimiento)
            if val < beta:
                beta = val

            if alpha >= beta:
                return beta
        return beta


def obtener_movimiento_computador(tablero, letra_computador):
    a = -2
    opciones = []

    if letra_computador == 'X':
        letra_jogador = 'O'
    else:
        letra_jogador = 'X'

    # -----------------------------------------------------------------------------------------------------------------------
    # MINIMAX EMPEZARA AQUI
    # 1)La maquina puede ganar en el siguiente movimiento.

    for i in range(1, 10):
        copy = Obtener_copia_Tablero(tablero)
        if espacio_libre(copy, i):
            realizar_movimiento(copy, letra_computador, i)
            if ganador(copy, letra_computador):
                return i

    # 2) O jugador puede no ganar en el segundo movimiento.

    for i in range(1, 10):
        copy = Obtener_copia_Tablero(tablero)
        if espacio_libre(copy, i):
            realizar_movimiento(copy, letra_jogador, i)
            if ganador(copy, letra_jogador):
                return i

    posibles_opciones_on = posibles_opciones(tablero)

    for movimiento in posibles_opciones_on:

        realizar_movimiento(tablero, letra_computador, movimiento)
        val = alphabeta(tablero, letra_computador, letra_jugador, -2, 2)
        realizar_movimiento(tablero, '', movimiento)

        if val > a:
            a = val
            opciones = [movimiento]

        elif val == a:
            opciones.append(movimiento)

    return random.choice(opciones)


print('-------------------------------------------------------')
print(' 				 	TRES EN RAYA	     			  ')
print('-------------------------------------------------------')

print('                    X  |  O  |                        ')
print('                  -----------------                   ')
print('                       |  X  |                        ')
print('                  -----------------                   ')
print('                    O  |  O  |  X                     ')

print('-------------------------------------------------------')

print('EL JUEGO DE 3 EN RAYA TIENE EL PBJETIVO DE:\n'
      'FORMAR 3 SEGUIDOS PARA PODER GANAR EN TODO SENTIDO,\n'
      'GANA EL PRIMERO EN FORMAR 3 SEGUIDAS.')

print('\n                 COMENCEMOS!!                 ')

print('-------------------------------------------------------')

jugar = True
while jugar:

    tablero = [''] * 10
    letra_jugador, letra_computador = retornar_letra_jugador()
    rodada = juega_primero()
    print('O ' + rodada + ' Haz la primera Jugada.\n')
    juego_comienza = True

    while juego_comienza:
        if rodada == 'jugador':

            Mesa_Dibujo(tablero)
            movimiento = obtener_movimiento_jugador(tablero)
            realizar_movimiento(tablero, letra_jugador, movimiento)

            if ganador(tablero, letra_jugador):
                Mesa_Dibujo(tablero)
                print('\nUhuuuuuul! Tienes suerte, ganaste!')
                juego_comienza = False

            else:
                if tablero_lleno(tablero):
                    Mesa_Dibujo(tablero)
                    print('\nIzi, no pudiste ganar!!!\n'
                          ' a la computadora.')
                    break
                else:
                    rodada = 'computador'

        else:

            movimiento = obtener_movimiento_computador(tablero, letra_jugador)
            realizar_movimiento(tablero, letra_computador, movimiento)

            if ganador(tablero, letra_computador):
                Mesa_Dibujo(tablero)
                print("\nTe vencio la computadora\n"
                      "Quieres la revancha o no!!!")
                juego_comienza = False

            else:
                if tablero_lleno(tablero):
                    Mesa_Dibujo(tablero)
                    print('\nIzi, no pudiste ganar!!!\n'
                          ' a la computadora.')
                    break
                else:
                    rodada = 'jugador'

    opcion = ''
    while not (opcion == 'S' or opcion == 'N'):
        print("\nFin del Juego. \n\n"
              '-------------------------------------------------------\n'
              "Jugar nuevamente? \n"
              "Para si pulse 'S', para no digite 'N'.")

        opcion = raw_input().upper()
        if opcion != 'S' and opcion != 'N':
            print("\nOrpimio otra letra. \n"
                  "Para si pulse 'S', para no pulse 'N'!")

        if opcion == 'N':
            print("\nTe vere en la próxima!")
            jugar = False