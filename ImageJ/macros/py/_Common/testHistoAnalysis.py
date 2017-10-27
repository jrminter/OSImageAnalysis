from jarray import array, zeros  
from ij import IJ, ImagePlus

factor = 0.95
imp = IJ.getImage()
ip = imp.getProcessor()
maxGray = int(ip.getMax())
nBins = maxGray + 1
hist = ip.getHistogram(nBins)
# print(len(hist))

# print((hist[0], hist[nBins/2],hist[nBins-1]))

glVal = zeros(nBins, 'd')
glCum = zeros(nBins, 'f')

glSum = 0.0
maxCts = 0

totCts = 0
for i in range(0, nBins):
	glVal[i] = i
	cts = hist[i]
	if(cts > maxCts):
		maxCts = cts
	totCts += cts
	glCum[i] = float(totCts)

# print(totCts)

for i in range(0, nBins):
	glCum[i] /= totCts

frac = 1.0
n = 1
thr = 0
while(frac >= factor):
	thr = nBins-n
	frac = glCum[thr]
	n += 1

print(thr)

IJ.setMinAndMax(imp, 0, thr)


	
	
	
	

