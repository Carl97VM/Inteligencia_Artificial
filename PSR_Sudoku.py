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

variables = ["%s%d" % (i, j) for i in uppercase[:9] for j in range(1, 10)]

dominios = OrderedDict((v, list(range(1, 10))) for v in variables)


def const_different(variables, values):
    return values[0] != values[1]  # Se espera que el valor de los vecinos sea diferente

sudoku = \
"""
  3 2 6
9  3 5  1
  18 64
  81 29
7       8
  67 82
  26 95
8  2 3  9
  5 1 3
"""


def analizar_rompecabeza(puzzle):
    sudoku_lineas = list(map(lambda s: s.rstrip("\n"), StringIO(puzzle).readlines()[1:]))
    dominios = {}

    for k, i in enumerate(uppercase[:9]):
        for j in range(1, 10):
            linea = sudoku_lineas[k]
            if len(linea) <= (j - 1):
                continue
            val = linea[j - 1]
            if val != ' ':
                var = "%s%d" % (i, j)
                dominios[var] = [int(val)]

    return dominios


def hacer_restricciones():
    """
    Hace una lista de restricciones para el problema de restricción binaria.
    """
    restricciones = []

    for j in range(1, 10):
        vars = ["%s%d" % (i, j) for i in uppercase[:9]]
        restricciones.extend((c, const_different) for c in combinations(vars, 2))

    for i in uppercase[:9]:
        vars = ["%s%d" % (i, j) for j in range(1, 10)]
        restricciones.extend((c, const_different) for c in combinations(vars, 2))

    for b0 in ['ABC', 'DEF', 'GHI']:
        for b1 in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
            vars = ["%s%d" % (i, j) for i in b0 for j in b1]
            l = list((c, const_different) for c in combinations(vars, 2))
            restricciones.extend(l)

    return restricciones


def hacer_k_restricciones():

    def alldiff(variables, values):
        return len(values) == len(set(values))  # Elimina valores repetidos y conteo

    restricciones = []

    for j in range(1, 10):
        vars_ = ["%s%d" % (i, j) for i in uppercase[:9]]
        restricciones.append((vars_, alldiff))

    for i in uppercase[:9]:
        vars_ = ["%s%d" % (i, j) for j in range(1, 10)]
        restricciones.append((vars_, alldiff))

    for b0 in ['ABC', 'DEF', 'GHI']:
        for b1 in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
            vars_ = ["%s%d" % (i, j) for i in b0 for j in b1]
            restricciones.append((vars_, alldiff))

    return restricciones


def mostrar_solucion(sol):
    for i in uppercase[:9]:
        print(" ".join([str(sol["%s%d" % (i, j)]) for j in range(1, 10)]))


dominios.update(analizar_rompecabeza(sudoku))

# -- Restricciones binarias hechas a mano.--
restricciones = hacer_restricciones()
inicio = time()
dominios0 = deepcopy(dominios)
my_problem = ProblemaPSR(variables, dominios0, restricciones)
sol = backtrack(my_problem)
transcurrido = time() - inicio
mostrar_solucion(sol)
print("tomo %d segundos completar utilizando restriccinoes binarias" % transcurrido) # por que AC3 es rapido

# -- Restricciones N-arias hechas binarias utilizando variables ocultas --
dominios1 = deepcopy(dominios)
inicio = time()
variables1, dominios1, restricciones = convertir_a_binario(variables, dominios1, hacer_k_restricciones())
my_problem = ProblemaPSR(variables1, dominios1, restricciones)
sol = backtrack(my_problem)
transcurrido = time() - inicio
mostrar_solucion(sol)
print("tomo %d segundos completar utilizando restricciones binarias (variables ocultas)" % transcurrido)

# -- Restriciones N-arias --
restricciones = hacer_k_restricciones()
dominios3 = deepcopy(dominios)
inicio = time()
my_problem = ProblemaPSR(variables, dominios3, restricciones)
sol = backtrack(my_problem)
transcurrido = time() - inicio
mostrar_solucion(sol)
print("Tomo %d segundos completar utilizando restricciones n-arias" % transcurrido)

