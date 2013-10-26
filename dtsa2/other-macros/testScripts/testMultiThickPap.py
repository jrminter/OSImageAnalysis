import sys
import os
import glob
import shutil
# testMultiThickPap.py

import time
import math
import csv

os.chdir("C:/Temp/")
f = open("out.txt", "r")
lines = f.readlines()
nLines = len(lines)
print(nLines)
recs = (nLines-13)/15
print(recs)

v = lines[5].split()[4]
l = len(v)
e0 = v[0:l-3]
e0 = float(e0)
print(e0)

for i in range(recs+1):
  rNi = 15*i + 16
  eNi = lines[rNi].split( )[2]
  print(eNi)
  tNi= 0.1*float(lines[rNi+1].split( )[5])
  print(tNi)
  kNi = float(lines[rNi].split()[8])
  print(kNi)

  rCu = 15*i + 19
  eCu = lines[rCu].split()[2]
  print(eCu)
  tCu = 0.1*float(lines[rCu+1].split()[5])
  print(tCu)
  kCu = float(lines[rCu].split()[8])
  print(kCu)