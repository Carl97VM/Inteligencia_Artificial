# Implementación del juego de dos jugadores Tic-Tac-Toe en Python.

#'''Haremos el tablero usando el diccionario 
#    en qué teclas estará la ubicación (es decir: arriba a la izquierda, centro a la derecha, etc.)
#    e inicialmente sus valores serán un espacio vacío y luego después de cada movimiento 
#    cambiaremos el valor según la elección de movimiento del jugador. '''#

#theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
#            '4': ' ' , '5': ' ' , '6': ' ' ,
#            '1': ' ' , '2': ' ' , '3': ' ' }

theBoard = {'21': ' ' , '22': ' ' , '23': ' ','24': ' ' , '25': ' ',
            '16': ' ' , '17': ' ' , '18': ' ','19': ' ' , '20': ' ',
            '11': ' ' , '12': ' ' , '13': ' ','14': ' ' , '15': ' ',
            '6': ' ' , '7': ' ' , '8': ' ','9': ' ' , '10': ' ',
            '1': ' ' , '2': ' ' , '3': ' ','4': ' ' , '5': ' '}

board_keys  = []

for key in theBoard:
    board_keys.append(key)


#'' 'Tendremos que imprimir el tablero actualizado después de cada movimiento en el juego y 
#    así haremos una función en la que definiremos la función printBoard
#    para que podamos imprimir fácilmente el tablero cada vez llamando a esta función. '' '

def printBoard(board):
    print(board['21'] + '|' + board['22'] + '|' + board['23'] + '|' + board['24'] + '|' + board['25'])
    print('-+-+-+-+-')
    print(board['16'] + '|' + board['17'] + '|' + board['18'] + '|' + board['19'] + '|' + board['20'])
    print('-+-+-+-+-')
    print(board['11'] + '|' + board['12'] + '|' + board['13'] + '|' + board['14'] + '|' + board['15'])
    print('-+-+-+-+-')
    print(board['6'] + '|' + board['7'] + '|' + board['8'] + '|' + board['9'] + '|' + board['10'])
    print('-+-+-+-+-')
    print(board['1'] + '|' + board['2'] + '|' + board['3'] + '|' + board['4'] + '|' + board['5'])
# Ahora escribiremos la función principal que tiene toda la funcionalidad del juego.
def game():

    turn  =  'X'
    count  =  0


    for i in range(10):
        printBoard(theBoard)
        print("es el turno," + turn + ".Donde quieres mover?")

        move  =  input ()        

        if theBoard[move] == ' ':
            theBoard[move] = turn
            count += 1
        else:
            print("El lugar esta lleno.\nMueve a otro lugar?")
            continue

        # Ahora comprobaremos si el jugador X u O ha ganado, por cada movimiento después de 5 movimientos. 
        if count >= 5:
            if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # a través de la cima
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")                
                break
            elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # a través del medio
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # en la parte inferior
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # por el lado izquierdo
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # a por el medio
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break 
            elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
                printBoard(theBoard)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break 

        # Si ni X ni O ganan y el tablero está lleno, declararemos el resultado como 'empate'.
        if count == 9:
            print("\nGame Over.\n")                
            print("It's a Tie!!")

        # Ahora tenemos que cambiar el jugador después de cada movimiento.
        if turn  == 'X' :
            turn  =  'O'
        else :
            turn  =  'X'        
    
    # Ahora preguntaremos si el jugador quiere reiniciar el juego o no.
    restart = input("Quieres jugar de nuevo?(y/n)")
    if restart == "y" or restart == "Y":  
        for key in board_keys:
            theBoard[key] = " "

        game()

if  __name__  ==  "__main__" :
    game ()