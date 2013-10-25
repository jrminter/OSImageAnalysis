import os
import sys

os.chdir("c:/temp")
import dtsa2.papNiCu as pap
pap.writeGmrfInNiCu(200, 400, [12,15,20,25,30], "./in.txt", toa=35)



gmrfDir = "C:/Apps/gmrf-vf/"


gmrfCmd = gmrfDir + "gmrfilm < in.txt"
print(gmrfCmd)
os.system(gmrfCmd)



pap.modNiCuLayers(200, 400, range(10,31) , "./foo.csv")




gmrfCmd = gmrfDir + "gmrfilm < in.txt"
print(gmrfCmd)
os.system(gmrfCmd)
