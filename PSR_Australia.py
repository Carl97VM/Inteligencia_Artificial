from PSR import ProblemaPSR, backtrack, minimo_conflictos, VARIABLE_MAS_RESTRINGIDA, VARIABLE_GRADO_MAS_ALTO, VALOR_MENOS_RESTRINGIDO

variables = ('WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T')

dominios = dict((v, ['rojo', 'verde', 'azul']) for v in variables)

def const_different(variables, valores):
    return valores[0] != valores[1]  # esperar que el valor de los vecinos sea diferente

restricciones = [
    (('WA', 'NT'), const_different),
    (('WA', 'SA'), const_different),
    (('SA', 'NT'), const_different),
    (('SA', 'Q'), const_different),
    (('NT', 'Q'), const_different),
    (('SA', 'NSW'), const_different),
    (('Q', 'NSW'), const_different),
    (('SA', 'V'), const_different),
    (('NSW', 'V'), const_different),
]

mi_problema = ProblemaPSR(variables, dominios, restricciones)

#print(backtrack(mi_problema))
#print(backtrack(mi_problema, variable_heuristica=VARIABLE_MAS_RESTRINGIDA))
#print(backtrack(mi_problema, variable_heuristica=VARIABLE_GRADO_MAS_ALTO))
#print(backtrack(mi_problema, valor_heuristico=VALOR_MENOS_RESTRINGIDO))
#print(backtrack(mi_problema, variable_heuristica=VARIABLE_MAS_RESTRINGIDA, valor_heuristico=VALOR_MENOS_RESTRINGIDO))
#print(backtrack(mi_problema, variable_heuristica=VARIABLE_GRADO_MAS_ALTO, valor_heuristico=VALOR_MENOS_RESTRINGIDO))
print(minimo_conflictos(mi_problema))

