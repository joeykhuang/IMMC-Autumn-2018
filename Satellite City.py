import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.style as style

fertRate, mortRate, popEachYear, realPopEachYear = ([], [], [], [])
mortalityArray, fertilityArray = ([], [])

#Self-controlled variables
startingCalcYear = 1979
endCalcYear = 2050
cityStartPop = 9000000   #1979 Population
cityUrbanArea = 1630

#Dependent variables
yearsAfter15 = endCalcYear - 2015
yearsAfter79 = startingCalcYear - 1979
cityMetArea = 3460
if cityUrbanArea < 2000:
	cityCarryCap = cityUrbanArea * 14000
elif cityUrbanArea >= 2000:
	cityCarryCap = cityUrbanArea * 9800


# Calculating the fertility and mortality rates in the future
def fertility(t):
	return -1.7467 * math.pow(t, 5) + 525 * math.pow(t, 3) + 1500510 * math.pow(t, 2) - 91052600 * t + 2937700000


def mortality(t):
	return abs(-2.27 * t + 4546.81) + 637.98


def futLogPop(t, startPop, carryCap, rateChange):
	return float(startPop*carryCap*math.exp(rateChange*t))/float((float(carryCap)+float(startPop)*(math.exp(rateChange*t) - 1)))


for i in range(2016, endCalcYear+1):
	mortalityArray.append(mortality(i))
	fertilityArray.append(0.000000001 * (fertility(i - 1979)))

# Result due to aging #WORK IN PROGRESS
for i in range(yearsAfter15):
	if 10 < i <= 15:
		mortalityArray[i] *= 1.3
	elif i > 15:
		mortalityArray[i] *= 1.6
	elif i >= 27 :
		mortalityArray[i] *= 0.97

# Reading currently available data
with open('FertilityRate.csv', 'rb') as csvfile:
	fertReader = csv.reader(csvfile, delimiter='\t', quotechar='|')
	for row in fertReader:
		for letter in row:
			fertRate.append(letter)
with open('MortalityRate.csv', 'rb') as csvfile1:
	mortReader = csv.reader(csvfile1, delimiter='\t', quotechar='|')
	for row in mortReader:
		for letter in row:
			mortRate.append(letter)
with open('PopulationData.csv', 'rb') as csvfile2:
	popReader = csv.reader(csvfile2, delimiter='\t', quotechar='|')
	for row in popReader:
		for letter in row:
			realPopEachYear.append(int(letter))

# Using our model to calculate the past population trends
for a in range(37):
	factor = 1.00
	for i in range(a):
		factor *= (1 - float(mortRate[i]) / 1000.00 + float(fertRate[i]) / (114.0))
	total = 0
	if popEachYear != []:
		if a > 25:
			total = factor * cityStartPop + popEachYear[-1] * 0.010 * a
		elif 5 <= a <= 25:
			total = factor * cityStartPop + popEachYear[-1] * 0.009 * a
		else:
			total = factor * cityStartPop + popEachYear[-1] * 0.002 * a
	else:
		total = cityStartPop

	popEachYear.append(int(math.ceil(total)))

# Using our model to predict future population trends
for a in range(yearsAfter15):
	factor = 1.00
	if a <= 4:
		for i in range(1, a):
			factor *= (1 - mortalityArray[i] / 100000 + fertilityArray[i] / 114.0)
		total = factor * popEachYear[36]
	elif a == 5:
		for i in range(1, a):
			factor *= (1 - mortalityArray[i] / 100000 + fertilityArray[i] / 114.0)
		total = factor * (popEachYear[40] - 200000)
	elif a == 6:
		for i in range(1, a):
			factor *= (1 - mortalityArray[i] / 100000 + fertilityArray[i] / 114.0)
		total = factor * (popEachYear[40] - 240000)
	elif a == 7:
		for i in range(1, a):
			factor *= (1 - mortalityArray[i] / 100000 + fertilityArray[i] / 114.0)
		total = factor * (popEachYear[40] - 260000)
	else:
		for i in range(1, a):
			factor *= (1 - mortalityArray[i] / 100000 + fertilityArray[i] / 114.0)
			total = factor * (popEachYear[40] - 700000)
	popEachYear.append(int(math.ceil(total)))

nriArray = []
for i in range(len(fertilityArray)):
	nriArray.append(1 + (float(fertilityArray[i]) / float(popEachYear[i]) * 1000.0 / 114.0 - mortalityArray[i] / 1000))
for eachElement in nriArray:
	if eachElement >= 0:
		eachElement = 1 - eachElement


futureLogArray = []
for i in range(endCalcYear - startingCalcYear + 1):
	futureLogArray.append(futLogPop(i, cityStartPop, cityCarryCap, 0.075))


a = []
for t in range(len(popEachYear)):
	a.append([abs(int(cityCarryCap * 0.92 - popEachYear[t])), t])
smallest = [a[0][0], 0]
for i in range(len(a)):
	if a[i][0] < smallest[0]:
		smallest[0] = a[i][0]
		smallest[1] = i
print smallest[1] + startingCalcYear


years = []
for i in range(1979, 2051):
	years.append(int(i))

np.savetxt('1979-2051_PopulationModelBeijingSatellite.csv', (years, popEachYear, futureLogArray), fmt='%10.5f', delimiter=',')
print cityCarryCap

# Using matplotlib to graph the population
plt.plot(range(startingCalcYear + yearsAfter79, endCalcYear+1), popEachYear[yearsAfter79:])
plt.plot(range(startingCalcYear + yearsAfter79, endCalcYear+1), futureLogArray[yearsAfter79:])
plt.plot(range(startingCalcYear + yearsAfter79, endCalcYear+1), [cityCarryCap]*len(popEachYear[yearsAfter79:]))

plt.ylabel("Population")
plt.xlabel("Year")
plt.show()
