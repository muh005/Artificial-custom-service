import math
import random
import matplotlib.pyplot as plt

pop_size = 500	# population
max_value = 10	# max value of gene
chrom_length = 10 # length of chromosome
pc = 0.6		# probability of crossover
pm = 0.01		# probability of mutation
results = [[]]	# store the optimal value of each generation
fit_value = []	# fitness of each individual
fit_mean = []	# fitness of mean

def geneEncoding(pop_size, chrom_length):
	pop = [[]]
	for i in range(pop_size):
		temp = []
		for j in range(chrom_length):
			temp.append(random.randint(0, 1))
		pop.append(temp)

	return pop[1:]

pop = geneEncoding(pop_size, chrom_length)

def decodechrom(pop, chrom_length):
	temp = []
	for i in range(len(pop)):
		t = 0
		for j in range(chrom_length):
			t += pop[i][j] * (math.pow(2, j))
		temp.append(t)

	return temp

def calobjValue(pop, chrom_length, max_value):
	temp1 = []
	obj_value = []
	temp1 = decodechrom(pop, chrom_length)
	for i in range(len(temp1)):
		x = temp1[i] * max_value / (math.pow(2, chrom_length) - 1)
		obj_value.append(10 * math.sin(5*x) + 7 * math.cos(4*x))
	return obj_value

def calfitValue(obj_value):
	fit_value = []
	c_min = 0
	for i in range(len(obj_value)):
		if(obj_value[i] + c_min > 0):
			temp = c_min + obj_value[i]
		else:
			temp = 0.0
		fit_value.append(temp)
	return fit_value

def sum(fit_value):
	total = 0
	for i in range(len(fit_value)):
		total += fit_value[i]
	return total

def cumsum(fit_value):
	for i in range(len(fit_value)-2, -1, -1):
		t = 0
		j = 0
		while(j <= i):
			t += fit_value[j]
			j += 1
		fit_value[i] = t
		fit_value[len(fit_value)-1] = 1

def selection(pop, fit_value):
	newfit_value = []
	total_fit = sum(fit_value)
	for i in range(len(fit_value)):
		newfit_value.append(fit_value[i]/total_fit)

	cumsum(newfit_value)
	ms = []
	pop_len = len(pop)
	for i in range(pop_len):
		ms.append(random.random())
	ms.sort()
	fitin = 0
	newin = 0
	newpop = pop

	while newin < pop_len:
		if(ms[newin] < newfit_value[fitin]):
			newpop[newin] = pop[fitin]
			newin = newin + 1
		else:
			fitin = fitin + 1

	pop = newpop

def crossover(pop, pc):
	pop_len = len(pop)
	for i in range(pop_len - 1):
		if(random.random() < pc):
			cpoint = random.randint(0, len(pop[0]))
			temp1 = []
			temp2 = []
			temp1.extend(pop[i][0:cpoint])
			temp1.extend(pop[i+1][cpoint:len(pop[i])])
			temp2.extend(pop[i+1][0:cpoint])
			temp2.extend(pop[i][cpoint:len(pop[i])])
			pop[i] = temp1
			pop[i+1] = temp2

def mutation(pop, pm):
	px = len(pop)
	py = len(pop[0])

	for i in range(px):
		if(random.random() < pm):
			mpoint = random.randint(0, py - 1)
			if(pop[i][mpoint] == 1):
				pop[i][mpoint] = 0
			else:
				pop[i][mpoint] = 1

def b2d(b, max_value, chrom_length):
	t = 0
	for j in range(len(b)):
		t += b[j]*(math.pow(2, j))
	t = t* max_value/(math.pow(2, chrom_length) - 1)

	return t

def best(pop, fit_value):
	px = len(pop)
	best_individual = []
	best_fit = fit_value[0]
	for i in range(1, px):
		if(fit_value[i] > best_fit):
			best_fit = fit_value[i]
			best_individual = pop[i]
	return [best_individual, best_fit]

print("y = 10 * math.sin(5*x) + 7 * math.cos(4*x)")

for i in range(pop_size):
	obj_value = calobjValue(pop, chrom_length, max_value)
	fit_value = calfitValue(obj_value)
	best_individual, best_fit = best(pop, fit_value)
	results.append([best_fit, b2d(best_individual, max_value, chrom_length)])
	selection(pop, fit_value)
	crossover(pop, pc)
	mutation(pop, pm)

results = results[1:]
results.sort()

X = []
Y = []
for i in range(500):
	X.append(i)
	t = results[i][0]
	Y.append(t)

plt.plot(X, Y)
plt.show()



