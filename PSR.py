import random
from copy import deepcopy, copy
from itertools import product

from busquedas_02 import argmin, argmax

from operator import itemgetter


__all__ = ['todos_los_arcos', 'revisar', 'arco_consistencia_3']

fst = itemgetter(0)


def revisar(dominios, arco, restricciones):
    """
    Dado el arco X, Y (variables), elimina los valores del dominio de X 
    que no cumplen la restricción entre X e Y.

    Es decir, dado x1 en el dominio de X, x1 se eliminará del dominio, 
    si no hay ningún valor y en el dominio de Y que haga que la restricción (X, Y) sea verdadera, 
    para aquellas restricciones que afectan a X e Y.
    """
    x, y = arco
    restricciones_relacionadas = [(vecinos, restriccion)
                           for vecinos, restriccion in restricciones
                           if set(arco) == set(vecinos)]

    modificado = False

    for vecinos, restriccion in restricciones_relacionadas:
        for x_valor in dominios[x]:
            resultados_restriccion = (_llamar_restriccion({x: x_valor, y: y_valor},
                                                   vecinos, restriccion)
                                  for y_valor in dominios[y])

            if not any(resultados_restriccion):
                dominios[x].remove(x_valor)
                modificado = True

    return modificado


def todos_los_arcos(restricciones):
    """
    For each restriccion ((X, Y), const) adds:
        ((X, Y), const)
        ((Y, X), const)
    """
    arcos = set()

    for vecinos, restriccion in restricciones:
        if len(vecinos) == 2:
            x, y = vecinos
            list(map(arcos.add, ((x, y), (y, x))))

    return arcos

def arco_consistencia_3(dominios, restricciones):
    """
    Hace que un problema de PSR sea consistente en arco.
    Ignora cualquier restricción que no sea binaria.
    """
    arcos = list(todos_los_arcos(restricciones))
    arcos_pendientes = set(arcos)

    while arcos_pendientes:
        x, y = arcos_pendientes.pop()
        if revisar(dominios, (x, y), restricciones):
            if len(dominios[x]) == 0:
                return False
            arcos_pendientes = arcos_pendientes.union((x2, y2) for x2, y2 in arcos
                                              if y2 == x)
    return True


class ProblemaPSR(object):
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones

        # Diccionario de restricciones basadas en variables
        self.var_restricciones = dict([(v, [restriccion
                                         for restriccion in restricciones
                                         if v in restriccion[0]])
                                    for v in variables])

        # Calcular el grado de cada variable
        self.var_grados = dict([(v, len(self.var_restricciones[v]))
                                 for v in variables])


VARIABLE_MAS_RESTRINGIDA = 'mcv'
VARIABLE_GRADO_MAS_ALTO = 'degree'
VALOR_MENOS_RESTRINGIDO = 'lvc'


def backtrack(problema, variable_heuristica='', valor_heuristico='', inferencia=True):
    '''
    Busqueda backtracking (vuelta atrás).

    variable_heuristica es la heuristica elegida para una variable, puede ser
    VARIABLE_MAS_RESTRINGIDA, VARIABLE_GRADO_MAS_ALTO, or vacia para una simple eleccion ordenada.
    valor_heuristico es el valor heuristico elegido, pude ser
    VALOR_MENOS_RESTRINGIDO or vacio para una simple eleccion ordenada.
    '''
    asignacion = {}
    dominios = deepcopy(problema.dominios)

    if variable_heuristica == VARIABLE_MAS_RESTRINGIDA:
        selector_variable = _selector_variable_mas_restringida
    elif variable_heuristica == VARIABLE_GRADO_MAS_ALTO:
        selector_variable = _selector_variable_mayor_grado
    else:
        selector_variable = _selector_variable_basico

    if valor_heuristico == VALOR_MENOS_RESTRINGIDO:
        clasificador_valores = _clasificador_valores_menos_restrictivos
    else:
        clasificador_valores = _clasificador_valores_basico
    return _backtracking(problema,
                         asignacion,
                         dominios,
                         selector_variable,
                         clasificador_valores,
                         inferencia=inferencia)


def _selector_variable_basico(problema, variables, dominios):
    '''
    Selecciona la siguiente variable en orden.
    '''
    return variables[0]


def _selector_variable_mas_restringida(problema, variables, dominios):
    '''
    Elija la variable que tenga menos valores disponibles.
    '''
    # variable con menos valores disponibles
    return sorted(variables, key=lambda v: len(dominios[v]))[0]


def _selector_variable_mayor_grado(problema, variables, dominios):
    '''
    Elija la variable que está involucrada en más restricciones.
    '''
    # variable involucrada en más restricciones
    return sorted(variables, key=lambda v: problema.var_grados[v], reverse=True)[0]


def _contar_conflictos(problema, asignacion, variable=None, valor=None):
    '''
    Cuenta el número de restricciones no cumplidas en una asignación dada.
    '''
    return len(_encontrar_conflictos(problema, asignacion, variable, valor))


def _llamar_restriccion(asignacion, vecinos, restriccion):
    variables, valores = zip(*[(n, asignacion[n]) for n in vecinos])
    return restriccion(variables, valores)

def _encontrar_conflictos(problema, asignacion, variable=None, valor=None):
    '''
    Encuentre restricciones no cumplidas en una asignación dada, con la posibilidad de especificar
    una nueva variable y valor para agregar a la asignación antes de verificar.
    '''
    if variable is not None and valor is not None:
        asignacion = deepcopy(asignacion)
        asignacion[variable] = valor

    conflictos = []
    for vecinos, restriccion in problema.restricciones:
        # Si todos los vecinos en la restricción tienen valores, verifica si es conflicto
        if all(n in asignacion for n in vecinos):
            if not _llamar_restriccion(asignacion, vecinos, restriccion):
                conflictos.append((vecinos, restriccion))

    return conflictos

def _clasificador_valores_basico(problema, asignacion, variable, dominios):
    '''
    Ordenar valores en el mismo orden original.
    '''
    return dominios[variable][:]


def _clasificador_valores_menos_restrictivos(problema, asignacion, variable, dominios):
    '''
    Ordena los valores en función de cuántos conflictos generan si se asignan.
    '''
    # valor que genera menos conflictos
    def actualizar_asignacion(valor):
        nueva_asignacion = deepcopy(asignacion)
        nueva_asignacion[variable] = valor
        return nueva_asignacion

    valores = sorted(dominios[variable][:],
                    key=lambda v: _contar_conflictos(problema, asignacion,
                                                   variable, v))
    return valores

def _backtracking(problema, asignacion, dominios, selector_variable, clasificador_valores, inferencia=True):
    '''
    Algoritmo de seguimiento recursivo interno.
    '''
    if len(asignacion) == len(problema.variables):
        return asignacion

    pendiente = [v for v in problema.variables if v not in asignacion]
    variable = selector_variable(problema, pendiente, dominios)
    valores = clasificador_valores(problema, asignacion, variable, dominios)

    for valor in valores:
        nueva_asignacion = deepcopy(asignacion)
        nueva_asignacion[variable] = valor

        if not _contar_conflictos(problema, nueva_asignacion): 
            nuevos_dominios = deepcopy(dominios)
            nuevos_dominios[variable] = [valor]

            if not inferencia or arco_consistencia_3(nuevos_dominios, problema.restricciones):
                resultado = _backtracking(problema,
                                       nueva_asignacion,
                                       nuevos_dominios,
                                       selector_variable,
                                       clasificador_valores,
                                       inferencia=inferencia)
                if resultado:
                    return resultado

    return None


def _valor_conflictos_minimos(problema, asignacion, variable):
    '''
    Devolver el valor que genera el menor número de conflictos..
    En caso de empate, se selecciona un valor aleatorio entre este subconjunto de valores.
    '''
    return argmin(problema.dominios[variable], lambda x: _contar_conflictos(problema, asignacion, variable, x))


def minimo_conflictos(problema, asignacion_inicial=None, limite_iteraciones=0):
    """
    Busca minimo de conflictos.

    asignacion_inicial, la asignación inicial, o None para generar una aleatoria.
    Si se especifica limite_iteraciones, el algoritmo finalizará después de ese número de iteraciones.
    De lo contrario, continuará hasta que encuentre una asignación que no genere conflictos (una solución).
    """
    asignacion = {}
    if asignacion_inicial:
        asignacion.update(asignacion_inicial)
    else:
        for variable in problema.variables:
            valor = _valor_conflictos_minimos(problema, asignacion, variable)
            asignacion[variable] = valor

    iteracion = 0
    ejecutar = True
    while ejecutar:
        conflictos = _encontrar_conflictos(problema, asignacion)

        variables_conflicto = [v for v in problema.variables
                              if any(v in conflicto[0] for conflicto in conflictos)]

        if variables_conflicto:
            variable = random.choice(variables_conflicto)
            valor = _valor_conflictos_minimos(problema, asignacion, variable)
            asignacion[variable] = valor

        iteracion += 1

        if limite_iteraciones and iteracion >= limite_iteraciones:
            ejecutar = False
        elif not _contar_conflictos(problema, asignacion):
            ejecutar = False

    return asignacion


def convertir_a_binario(variables, dominios, restricciones):
    """
    Devuelve una nueva lista de restricciones, todas binarias, usando variables ocultas.
    Puede usarlo como paso anterior al crear un problema.
    """

    def wdiff(vars_):
        def diff(variables, valores):
            ocultas, otra = variables
            if ocultas.startswith('ocultas'):
                idx = vars_.index(otra)
                return valores[1] == valores[0][idx]
            else:
                idx = vars_.index(ocultas)
                return valores[0] == valores[1][idx]
        diff.no_wrap = True  # para que no esté envuelto para intercambiar valores
        return diff

    nuevas_restricciones = []
    nuevos_dominios = copy(dominios)
    nuevas_variables = list(variables)
    ultimo = 0

    for vars_, const in restricciones:
        if len(vars_) == 2:
            nuevas_restricciones.append((vars_, const))
            continue

        ocultas = 'ocultas%d' % ultimo
        nuevas_variables.append(ocultas)
        ultimo += 1
        nuevos_dominios[ocultas] = [t for t in product(*map(dominios.get, vars_)) if const(vars_, t)]
        for var in vars_:
            nuevas_restricciones.append(((ocultas, var), wdiff(vars_)))
    return nuevas_variables, nuevos_dominios, nuevas_restricciones
