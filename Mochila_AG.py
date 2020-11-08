import random
"""
    MATERIA: Inteligencia Artificial
    Entrega de datos entre 0's y 1's 
    argumentando que los 0's son los objetos que no se llevaran en la mochila
    y que los 1"s si se llevaran en la mochila
"""
class Problema_Genetico(object):
    # Constructor
    def __init__(self, genes, fun_decodificar, fun_cruzar, fun_mutar, fun_fitness, longitud_individuos):
        self.genes = genes
        self.fun_decodificar = fun_decodificar
        self.fun_cruzar = fun_cruzar
        self.fun_mutar = fun_mutar
        self.fun_fitness = fun_fitness
        self.longitud_individuos = longitud_individuos
    
    def decodificar(self, genotipo):
        #Devuelve el fenotipo a partir del genotipo
        fenotipo = self.fun_decodificar(genotipo)
        return fenotipo
    
    def cruzar(self, cromosoma1, cromosoma2):         
        #Devuelve el cruce de un par de cromosomas
        cruce = self.fun_cruzar(cromosoma1, cromosoma2)
        return cruce 
    
    def mutar(self, cromosoma, prob):
        #Devuelve el cromosoma mutado
        mutante = self.fun_mutar(cromosoma, prob)
        return mutante

    def fitness(self, cromosoma):
        #Función de valoración
        valoracion = self.fun_fitness(cromosoma)
        return valoracion

"""
    Función interpreta lista de 0's y 1's como número natural:  
"""
def binario_a_decimal(x):
    return sum(b * (2 ** i) for (i, b) in enumerate(x)) 

def fun_cruzar(cromosoma1, cromosoma2):
    # Cruza los cromosomas por la mitad
    l1 = len(cromosoma1)
    l2 = len(cromosoma2)
    cruce1 = cromosoma1[0:int(l1 / 2)]+cromosoma2[int(l1 / 2):l2]
    cruce2 = cromosoma2[0:int(l2 / 2)]+cromosoma1[int(l2 / 2):l1]
    return [cruce1, cruce2]

def fun_mutar(cromosoma,prob):
    # Elige un elemento al azar del cromosoma y lo modifica con una probabilidad igual a prob
    l = len(cromosoma)
    p = random.randint(0, l - 1)
    if prob > random.uniform(0, 1):
        cromosoma[p] =  (cromosoma[p] + 1) % 2
        #cromosoma[p] = cromosoma[p]*-1
    return cromosoma

def fun_fitness_cuad(cromosoma):
    # Función de valoración que eleva al cuadrado el número recibido en binario
    n = binario_a_decimal(cromosoma)**2
    return n

def deco_x(x):
    return [binario_a_decimal(x[:4]), binario_a_decimal(x[4:])] 

def poblacion_inicial(problema_genetico, size):
    l = []
    for i in range(size):
        l.append([random.choice(problema_genetico.genes) for i in range(problema_genetico.longitud_individuos)])                
    return l

def cruza_padres(problema_genetico, padres):
    l = []
    l1 = len(padres)
    while padres != []:
        l.extend(problema_genetico.cruzar(padres[0], padres[1]))
        padres.pop(0)
        padres.pop(0)
    return l

def muta_individuos(problema_genetico, poblacion, prob):
    return [problema_genetico.mutar(x, prob) for x in poblacion]

def seleccion_por_torneo(problema_genetico, poblacion, n, k, opt):
    # Selección por torneo de n individuos de una población. Siendo k el nº de participantes
    # y opt la función max o min.
    seleccionados = []
    for i in range(n):
        participantes = random.sample(poblacion, k)
        seleccionado = opt(participantes, key = problema_genetico.fitness)
        #opt(poblacion, key = problema_genetico.fitness)
        seleccionados.append(seleccionado)
        # poblacion.remove(seleccionado)
    return seleccionados  

def nueva_generacion_t(problema_genetico, k, opt, poblacion, n_padres, n_directos, prob_mutar):
    padres2 = seleccion_por_torneo(problema_genetico, poblacion, n_directos, k, opt) 
    padres1 = seleccion_por_torneo(problema_genetico, poblacion, n_padres , k, opt)
    cruces =  cruza_padres(problema_genetico,padres1)
    generacion = padres2 + cruces
    resultado_mutaciones = muta_individuos(problema_genetico, generacion, prob_mutar)
    return resultado_mutaciones

def algoritmo_genetico_t(problema_genetico, k, opt, ngen, size, prop_cruces, prob_mutar):
    poblacion = poblacion_inicial(problema_genetico, size)
    print("Poblacion Inicial")
    print(poblacion)
    n_padres = round(size * prop_cruces)
    n_padres = int (n_padres if n_padres % 2 == 0 else n_padres - 1)
    n_directos = size - n_padres
    for _ in range(ngen):
        poblacion = nueva_generacion_t(problema_genetico, k, opt, poblacion, n_padres, n_directos, prob_mutar)
        print("Nueva población")
        print(poblacion)
    mejor_cr = opt(poblacion, key = problema_genetico.fitness)
    mejor = problema_genetico.decodificar(mejor_cr)
    return (mejor, problema_genetico.fitness(mejor_cr)) 

def decodifica_mochila(cromosoma, n_objetos, pesos, capacidad):
    peso_en_mochila = 0
    l = []
    for i in range(n_objetos):
        if cromosoma[i] == 1 and peso_en_mochila + pesos[i] <= capacidad:
            l.append(1)
            peso_en_mochila += pesos[i]
        elif cromosoma[i] == 0 or peso_en_mochila + pesos[i] > capacidad:
            l.append(0)
    return l 

def fitness_mochila(cromosoma, n_objetos, pesos, capacidad, valores):
    objetos_en_mochila = decodifica_mochila(cromosoma, n_objetos, pesos, capacidad)
    valor = 0
    for i in range(n_objetos):
        if objetos_en_mochila[i] == 1:
            valor += valores[i]
    return valor
            
#EJEMPLOS DE ALGORITMOS GENETICOS DE LAS MOCHILAS CON 3 INTERPRETACIONES
"""
    M1
"""
pesos1 = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
valores1 = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

"""
    M2
"""
pesos2 = [70,73,77,80,82,87,90,94,98,106,110,113,115,118,120]
valores2 = [135,139,149,150,156,163,173,184,192,201,210,214,221,229,240]

"""
    M3
"""
pesos3 = [382745,799601,909247,729069,467902, 44328,
       34610,698150,823460,903959,853665,551830,610856,
       670702,488960,951111,323046,446298,931161, 31385,496951,264724,224916,169684]
valores3 = [825594,1677009,1676628,1523970, 943972,  97426,
       69666,1296457,1679693,1902996,
       1844992,1049289,1252836,1319836, 953277,2067538, 675367,
       853655,1826027, 65731, 901489, 577243, 466257, 369261]

"""
    Para La mochila 1
"""
def fitness_mochila_1(cromosoma):
    v = fitness_mochila(cromosoma, 10, pesos1, 165, valores1)
    return v

def decodifica_mochila_1(cromosoma):
    v = decodifica_mochila(cromosoma, 10, pesos1, 165)
    return v

m1g = Problema_Genetico([0,1], decodifica_mochila_1, fun_cruzar, fun_mutar, fitness_mochila_1, 10)


"""
    Para La mochila 2
"""

def fitness_mochila_2(cromosoma):
    v = fitness_mochila(cromosoma, 15, pesos2, 750, valores2)
    return v

def decodifica_mochila_2(cromosoma):
    v = decodifica_mochila(cromosoma, 14, pesos2, 750)
    return v

m2g = Problema_Genetico([0,1], decodifica_mochila_2, fun_cruzar, fun_mutar, fitness_mochila_2, 15)


"""
    Para La mochila 3
"""

def fitness_mochila_3(cromosoma):
    v = fitness_mochila(cromosoma, 24, pesos3, 6404180 , valores3)
    return v

def decodifica_mochila_3(cromosoma):
    v = decodifica_mochila(cromosoma, 24, pesos3, 6404180)
    return v
m3g = Problema_Genetico([0,1], decodifica_mochila_3, fun_cruzar,  fun_mutar, fitness_mochila_3,24)


#print(algoritmo_genetico_t(m1g, 3, max, 100, 50, 0.8, 0.05))   #Mochila 1 Resultados
print(algoritmo_genetico_t(m2g,3, max, 200, 100, 0.8, 0.05))    #Mochila 2 Resultados
#print(algoritmo_genetico_t(m3g, 5, max, 400, 200, 0.75, 0.1))   #Mochila 3 Resultados 