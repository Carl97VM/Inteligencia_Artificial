import numpy as np
import os
import random
from random import randint
import sys
import csv


def loadCSV(pathRequeriments, pathStock):
	requeriments = np.loadtxt(pathRequeriments,delimiter = ',')

	materials = []

	fichero = open(pathStock,'rb')
	for line in fichero:
		local = []
		line = line.split(',')
		for item in line:
			if len(item)!=0 and item!='\n':
				local.append(float(item))
		materials.append(local)
	fichero.close()
	return requeriments,materials

'''
def initialPopulation(requeriments, materials, popSize):
	materialsList = []
	cont = 1
	for i in range(len(materials)):
		for j in range(2,len(materials[i])):
			materialsList.append([cont,materials[i][0],materials[i][j]])
			cont +=1
	requerimentsList = []
	for i in range(len(requeriments)):
		for j in range(int(requeriments[i][0])):
			requerimentsList.append([requeriments[i][2],requeriments[i][1]])
	candidatesList = np.empty([len(requerimentsList),len(materialsList)])
	for i in range(len(requerimentsList)):
		for j in range(len(materialsList)):
			if materialsList[j][1] == requerimentsList[i][0]:
				candidatesList[i][j] = materialsList[j][0]
			else:
				candidatesList[i][j] = 0
	population = []
	wasteFinal = []
	for pop in range(popSize):
		solutions = []
		for i in range(len(requerimentsList)):
			selections = np.where(candidatesList[i] != 0)[0]
			selection = candidatesList[i][random.choice(selections)]
			if materialsList[int(selection-1)][2] >= requerimentsList[i][1]:
				solutions.append([requerimentsList[i][0],requerimentsList[i][1],selection])
			else:
				flag = 1
				while flag == 1:
					selection = candidatesList[i][random.choice(selections)]
					if materialsList[int(selection-1)][2] >= requerimentsList[i][1]:
						solutions.append([requerimentsList[i][0],requerimentsList[i][1],selection])
						flag = -1
		typesMaterialsCut = range(1,len(candidatesList[0])+1)
		solutions = np.array(solutions)
		orderingList = []
		for i in range(len(typesMaterialsCut)):
			orderingList.append(solutions[np.where(solutions[:,-1] == typesMaterialsCut[i])[0]])
		for i in range(len(orderingList)):
			orderingList[i] = orderingList[i][orderingList[i][:,1].argsort()]
		total = 0
		for p in orderingList:
			total+=len(p)
		globalResult = []
		wasteTotal = 0
		total = 0
		for i in range(len(orderingList)):
			waste = 0
			result = []
			if len(orderingList[i]) != 0:
				#print orderingList[i]
				line = []
				if len(orderingList[i]) > 1:
					total += len(orderingList[i])
					for j in range(len(orderingList[i])):
						
						if j>0:
							if orderingList[i][j][1] <= waste:
								line.append(orderingList[i][j][1])	
								waste-= orderingList[i][j][1]
							else:
								result.append([materialsList[i][2], materialsList[i][1], line])
								waste = materialsList[i][2] - orderingList[i][j][1]
								line = []
								line.append(orderingList[i][j][1])
								if j == len(orderingList[i])-1:
									result.append([materialsList[i][2], materialsList[i][1], line])
						else:
							line.append(orderingList[i][j][1])
							waste = materialsList[i][2]-orderingList[i][j][1]
				else:
					total += len(orderingList[i])
					result.append([materialsList[i][2], materialsList[i][1], [orderingList[i][0][1]]])
				cuts = [len(result),materialsList[i][2], materialsList[i][1]]
				costGlobal = []
				#print cuts
				cost = 0
				for fil in range(len(result)):
					for column in range(len(result[fil][2])):
						cuts.append(result[fil][2][column])
						cost+=result[fil][2][column]
				cuts.append(len(result)*materialsList[i][2]-cost)
				wasteTotal+=len(result)*materialsList[i][2]-cost
				globalResult.append(cuts)
		wasteFinal.append(wasteTotal)
		population.append(globalResult)
		print total
	return population,wasteFinal, requerimentsList, materialsList, candidatesList
'''

def initialPopulation(requeriments, materials, popSize):

	materialsList = []
	cont = 1
	for i in range(len(materials)):
		for j in range(2,len(materials[i])):
			materialsList.append([cont,materials[i][0],materials[i][j]])
			cont +=1
	requerimentsList = []

	for i in range(len(requeriments)):
		for j in range(int(requeriments[i][0])):
			requerimentsList.append([requeriments[i][2],requeriments[i][1]])

	candidatesList = np.empty([len(requerimentsList),len(materialsList)])

	for i in range(len(requerimentsList)):
		for j in range(len(materialsList)):
			if materialsList[j][1] == requerimentsList[i][0]:
				candidatesList[i][j] = materialsList[j][0]
			else:
				candidatesList[i][j] = 0

	population = []
	wasteFinal = []
	for pop in range(popSize):
		solutions = []
		for i in range(len(requerimentsList)):
			selections = np.where(candidatesList[i] != 0)[0]
			selection = candidatesList[i][random.choice(selections)]
			if materialsList[int(selection-1)][2] >= requerimentsList[i][1]:
				solutions.append([requerimentsList[i][0],requerimentsList[i][1],selection])
			else:
				flag = 1
				while flag == 1:
					selection = candidatesList[i][random.choice(selections)]
					if materialsList[int(selection-1)][2] >= requerimentsList[i][1]:
						solutions.append([requerimentsList[i][0],requerimentsList[i][1],selection])
						flag = -1

		typesMaterialsCut = range(1,len(candidatesList[0])+1)

		solutions = np.array(solutions)

		orderingList = []
		for i in range(len(typesMaterialsCut)):
			orderingList.append(solutions[np.where(solutions[:,-1] == typesMaterialsCut[i])[0]])

		for i in range(len(orderingList)):
			orderingList[i] = orderingList[i][orderingList[i][:,1].argsort()]


		globalResult = []
		wasteTotal = 0

		for i in range(len(orderingList)):
			waste = 0
			result = []
			if len(orderingList[i]) != 0:
				#print orderingList[i]
				line = []
				if len(orderingList[i]) > 1:
					for j in range(len(orderingList[i])):
						
						if j>0:
							#print len(line)
							if orderingList[i][j][1] <= waste:
								line.append(orderingList[i][j][1])	
								waste-= orderingList[i][j][1]
								if j == len(orderingList[i])-1:
									result.append([materialsList[i][2], materialsList[i][1], line])
							else:
								result.append([materialsList[i][2], materialsList[i][1], line])
								waste = materialsList[i][2] - orderingList[i][j][1]
								line = []
								line.append(orderingList[i][j][1])
								if j == len(orderingList[i])-1:
									result.append([materialsList[i][2], materialsList[i][1], line])
						else:
					#		print len(line)
							line.append(orderingList[i][j][1])
							waste = materialsList[i][2]-orderingList[i][j][1]
					#raw_input()
				else:
					result.append([materialsList[i][2], materialsList[i][1], [orderingList[i][0][1]]])


				cuts = [len(result),materialsList[i][2], materialsList[i][1]]


				costGlobal = []
				#print cuts
				cost = 0
				for fil in range(len(result)):
					for column in range(len(result[fil][2])):
						cuts.append(result[fil][2][column])
						cost+=result[fil][2][column]
				cuts.append(len(result)*materialsList[i][2]-cost)
				wasteTotal+=len(result)*materialsList[i][2]-cost
				globalResult.append(cuts)


		wasteFinal.append(wasteTotal)
		population.append(globalResult)
	return population,wasteFinal, requerimentsList, materialsList, candidatesList

def breed(parent1, parent2, sizeMaterials):
	typesMaterials = range(1,sizeMaterials+1)
	child = []

	solutionsForMaterialParent1 = []
	for i in range(len(typesMaterials)):
		select = typesMaterials[i]
		local = []
		for j in range(len(parent1)):
			if parent1[j][2] == select:
				local.append(parent1[j])
		solutionsForMaterialParent1.append(local)


	solutionsForMaterialParent2 = []
	for i in range(len(typesMaterials)):
		select = typesMaterials[i]
		local = []
		for j in range(len(parent2)):
			if parent2[j][2] == select:
				local.append(parent2[j])
		solutionsForMaterialParent2.append(local)


	for i in range(len(typesMaterials)):
		if typesMaterials[i]%2 == 0:
			child.extend(solutionsForMaterialParent2[i])
		else:
			child.extend(solutionsForMaterialParent1[i])
	return child


def breedPopulation(matingpool, popSize, sizeMaterials):
	index = range(len(matingpool))
	numberChildrens = popSize-len(matingpool)
	childrens = []
	for i in range(numberChildrens):
		indexParent1 = random.choice(index)
		indexParent2 = random.choice(index)
		childrens.append(breed(matingpool[indexParent1], matingpool[indexParent2], sizeMaterials))

	matingpool.extend(childrens)
	return matingpool


'''
def selection(waste, pop, eliteSize):
	index = range(len(waste))
	tuplelist = [e for e in zip(index, waste)]
	tuplelist.sort(key=lambda tuplelist: tuplelist[1])
	popSelected = []
	for i in range(int(len(waste)*(eliteSize/100.0))):
		popSelected.append(pop[tuplelist[i][0]])
	return popSelected
'''

def selection(waste, pop, eliteSize):
	index = range(len(waste))
	random.shuffle(index)
	popSelected = []
	for i in range(int(len(waste)*(eliteSize/100.0))):
		popSelected.append(pop[index[i]])
	return popSelected


def computeWaste(pop):
	costGlobal = []
	for i in range(len(pop)):
		cost = 0
		for j in range(len(pop[i])):
			cost+= pop[i][j][-1]
		costGlobal.append(cost) 
	index = range(len(costGlobal))
	tuplelist = [e for e in zip(index, costGlobal)]
	tuplelist.sort(key=lambda tuplelist: tuplelist[1])
	bestSolution = pop[tuplelist[0][0]]
	bestWaste = tuplelist[0][1]
	return bestSolution,bestWaste


def orderingData(requerimentsList):
	requerimentsListZIP = zip(requerimentsList)
	requerimentsListZIP.sort(key=lambda requerimentsListZIP: requerimentsListZIP[0])
	requeriments = []
	typeClass= []

	for i in range(len(requerimentsListZIP)):
		typeClass.append(requerimentsList[i][0])
	typeClass = list(set(typeClass))

	for i in range(len(requerimentsListZIP)):
		requeriments.append(requerimentsListZIP[i][0])

	requeriments = np.array(requeriments)

	requerimentsForType = []
	for i in range(len(typeClass)):
		requerimentsForType.append(requeriments[np.where(requeriments[:,0] == typeClass[i])[0]])

	return requerimentsForType, typeClass

def mutate(individual, requerimentsList, materialsList, candidatesList, typeClass):

	indexForType = []
	for i in range(len(typeClass)):
		local = []
		for j in range(len(individual)):
			if individual[j][2] == typeClass[i]:
				local.append(individual[j])

		indexForType.append(local)


	random.shuffle(typeClass)

	child = []
	for i in range(len(typeClass)):
		child.append(individual[int(typeClass[i]-1)])

	return child



def mutatePopulation(pop, requerimentsList, materialsList, candidatesList, typeClass):
	newPopulation = []
	for i in range(len(pop)):
		newPopulation.append(mutate(pop[i], requerimentsList, materialsList, candidatesList, typeClass))
	return newPopulation



def nextGeneration(popInitial, waste, popSize, eliteSize, sizeMaterials, requerimentsList, materialsList, candidatesList, typeClass):
	matingpool = selection(waste, popInitial, eliteSize)
	children = breedPopulation(matingpool, popSize, sizeMaterials)
	#nextPopulation = mutatePopulation(children, requerimentsList, materialsList, candidatesList, typeClass)
#	return nextPopulation
	return children


def geneticAlgorithm(requeriments, materials, popSize, eliteSize, generations):

	[popInitial,waste, requerimentsList, materialsList, candidatesList] = initialPopulation(requeriments,materials, popSize)
	[requerimentsList, typeClass] = orderingData(requerimentsList)

	typesMaterials = len(materials)
	[bestSolution, bestWaste] = computeWaste(popInitial)
	bestSolutionLocal = []
	for i in range(generations):
		#print '\rGeneracion', i+1,'Min Cost ',bestWaste,
		print ('Generacion', i+1,'Min Cost ,',bestWaste)
		
		#sys.stdout.flush()
		pop = nextGeneration(popInitial, waste, popSize, eliteSize, typesMaterials, requerimentsList, materialsList, candidatesList, typeClass)
		[bestSolutionLocal, bestWasteLocal] = computeWaste(pop)
		if bestWasteLocal < bestWaste:
			bestSolution = bestSolutionLocal
			bestWaste = bestWasteLocal

	print ('Minimo desperdicio', bestWaste)

	cont = 0
	with open('Cortes de requerimientos.csv', 'wb') as csvfile:
		solutionCSV = csv.writer(csvfile)
		for i in range(len(bestSolution)):
			cont+= len(bestSolution[i][4::])
			solutionCSV.writerow(bestSolution[i])
		solutionCSV.writerow(['Desperdicio'])
		solutionCSV.writerow([bestWaste])



pathRequeriments = os.getcwd()+'/requeriments.csv'
pathStock = os.getcwd()+'/stock.csv'

[requeriments, materials] = loadCSV(pathRequeriments, pathStock)

geneticAlgorithm(requeriments, materials, popSize=5000, eliteSize=45, generations=5000)