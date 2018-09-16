import csv
import math
import matplotlib.pyplot as plt
from scipy import stats

fertRate, mortRate, popEachYear, realPopEachYear = ([], [], [], [])
mortalityArray, fertilityArray = ([], [])


# Calculating the fertility and mortality rates in the future
def fertility(t):
	return -1.7467 * math.pow(t, 5) + 525 * math.pow(t, 3) + 1500510 * math.pow(t, 2) - 91052600 * t + 2937700000


def mortality(t):
	return abs(-2.27 * t + 4546.81) + 637.98


for i in range(2016, 2051):
	mortalityArray.append(mortality(i))
	fertilityArray.append(0.000000001 * (fertility(i - 1979)))

# Result due to aging #WORK IN PROGRESS
for i in range(0, 35):
	if 10 < i <= 15:
		mortalityArray[i] *= 1.3
	if i > 15:
		mortalityArray[i] *= 1.6

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
for a in range(36):
	factor = 1.00
	for i in range(a):
		factor *= (1 - float(mortRate[i]) / 1000.00 + float(fertRate[i]) / (114.0))

	total = factor * 969005000.00 - 1019429 * a
	popEachYear.append(int(math.ceil(total)))

print popEachYear[-1]
print mortRate[-2]
popEachYear.append(popEachYear[-1]*(1 - float(mortRate[-1])/1000.00 + 2*float(fertRate[-1])/114.0))
print popEachYear[-1]

print abs(float(popEachYear[-1] - popEachYear[-2])/float(popEachYear[-1]) * 100)

# Using matplotlib to graph the population
plt.plot(range(1979, 2016), popEachYear)
plt.plot(range(1979, 2016), realPopEachYear)
plt.ylabel("Population")
plt.show()
