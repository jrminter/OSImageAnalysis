# testParsePapOut.py

import sys
import os
import glob
import shutil
import time
import math
import csv
import dtsa2

i=0
inPath = "out.txt"

os.chdir("C:/Apps/GMRFilm")

f = open(inPath, "r")
lines = f.readlines()
f.close()
nLines = len(lines)
print(nLines)
recs = nLines/26
print(recs)
rKv = 26*i + 5
v = lines[rKv].split()[4]
l = len(v)
e0 = v[0:l-3]
e0 = float(e0)
print(e0)

rNi = 26*i + 16
eNi = lines[rNi].split()[2]
print(eNi)

# print(lines[rNi+1].split())
tNi = 0.1*float(lines[rNi+1].split()[5])
print(tNi)
kNi = float(lines[rNi].split()[8])
print(kNi)

rCu = 26*i+19
eCu = lines[rCu].split()[2]
print(eCu)
tCu = 0.1*float(lines[rCu+1].split()[5])
print(tCu)
kCu = float(lines[rCu].split()[8])


