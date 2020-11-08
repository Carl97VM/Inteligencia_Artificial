from PSR import backtrack, ProblemaPSR, convertir_a_binario

variables = ('A', 'B', 'C')

dominios = {
    'A': [1, 2, 3],
    'B': [1, 3, 4],
    'C': [1, 2],
}


def const_different(variables, valores):
    return len(valores) == len(set(valores))  # elimina valores repetidos y conteo


# una restricción que espera que una variable sea más grande que otra
def const_one_bigger_other(variables, valores):
    return valores[0] > valores[1]


# una restricción que espera que dos variables sean una impar y la otra par,
# no importa cuál es de qué tipo
def const_one_odd_one_even(variables, valores):
    if valores[0] % 2 == 0:
        return valores[1] % 2 == 1  # first even, expect second to be odd
    else:
        return valores[1] % 2 == 0  # first odd, expect second to be even


# Una restricción que requiere que una variable sea diferente de 1
def const_not_1(variables, valores):
    return valores[0] != 1

restricciones = [
    (('A', 'B', 'C'), const_different),
    (('A', 'C'), const_one_bigger_other),
    (('A', 'C'), const_one_odd_one_even),
    (('A',), const_not_1)
]

variables, dominios, restricciones = convertir_a_binario(variables, dominios, restricciones)
problema = ProblemaPSR(variables, dominios, restricciones)
resultado = backtrack(problema)
print(resultado)
# resultado, {'A':2, 'B': 3, 'C': 1})

