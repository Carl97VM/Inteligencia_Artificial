from time import time
from copy import deepcopy

from PSR import (
    backtrack, VARIABLE_MAS_RESTRINGIDA, VALOR_MENOS_RESTRINGIDO,
    convertir_a_binario, ProblemaPSR)

variables = ('F', 'T', 'U', 'W', 'R', 'O', 'C_10', 'C_100', 'C_1000')

dominios = dict((v, list(range(1, 10))) for v in variables)


def const_different(variables, values):
    return len(values) == len(set(values))  # elimina valores repetidos y cuenta

restricciones = [
    (('F', 'T', 'U', 'W', 'R', 'O'), const_different),
    (('O', 'R', 'C_10'), lambda vars_, values: values[0] + values[0] == values[1] + 10 * values[2]),
    (('C_10', 'W', 'U', 'C_100'), lambda vars_, values: values[0] + values[1] + values[1] == values[2] + 10 * values[3]),
    (('C_100', 'T', 'O', 'C_1000'), lambda vars_, values: values[0] + values[1] + values[1] == values[2] + 10 * values[3]),
    (('C_1000', 'F'), lambda vars_, values: values[0] == values[1])
]

restricciones_originales = deepcopy(restricciones)
dominios_originales = deepcopy(dominios)

inicio = time()
problema = ProblemaPSR(variables, dominios_originales, restricciones_originales)
resultado = backtrack(problema, variable_heuristica=VARIABLE_MAS_RESTRINGIDA, valor_heuristico=VALOR_MENOS_RESTRINGIDO)
transcurrido = time() - inicio
print(resultado)
print("Tomo %d segundos terminar utilizando restricciones n-arias" % transcurrido)


inicio = time()
variables, dominios, restricciones = convertir_a_binario(variables, dominios, restricciones)
problema = ProblemaPSR(variables, dominios, restricciones)
resultado = backtrack(problema, valor_heuristico=VALOR_MENOS_RESTRINGIDO)
transcurrido = time() - inicio
print(resultado)
print("Tomo %d segundos terminar utilizando restricciones binarias" % transcurrido)
