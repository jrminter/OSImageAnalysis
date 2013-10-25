# -*- coding: utf-8 -*-
# DTSA-II Script - J. R. Minter - 2013-10-15
#
# 2013-10-25 JRM Updated to use gmrfilm built using
#                Visual Fortran 6

import sys
import os
import glob
import shutil
import time
import math
import csv
import dtsa2

gmrfPth="C:/Apps/GMRFilm/gmrfilm.exe"

"""A series of scripts for PAP simulations of Ni on Cu on C wrapping calls to GMRFilm
Place this file in DTSA_ROOT/lib/dtsa2/"""


def genNiCuPetPapMatchErr(lKv, lNiKaKr, lCuKaKr, lThNi, lThCu, outFilPath):
  """genNiCuPetPapMatchErr(lKv, lNiKaKr, lCuKaKr,  lThNi, lThCu, outFilPath)
  Generate the RMS error between measured and computed k-ratios
  for layers of Ni and Cu for a range of specified values
  of thickness on a PET substrate for a range of accelerating voltages using
  GMRFilm. Store these to a comma-delimited file for input into a plotting or
  k-ratio matching program. Approximate PET as C.
  Input:
  lKv        - a list of the accelerating voltages to simulate in kV.
  lCuKaKr    - a list of measured CuKa K-ratios corresponding to e0 in lKv
  lNiKaKr    - a list of measured NiKa K-ratios corresponding to e0 in lKv
  lThNi      - a list with the starting, ending, and step size for Ni thickness in nm
  lThCu      - a list with the starting, ending, and step size for Cu thickness in nm
  outFilPath - the path for the .csv file. This contains a line for each voltage with
               e0, tNi, tCu, krNiKa, krCuKa"""
  
  # this is how we will run GMRFilm
  gmrfCmd = gmrfPth + " < ./in.txt"
  
  # clean up any old output files in our working directory
  a = glob.glob('F*')
  if (len(a) > 0):
    os.remove(a[0])
  # open up the k-ratio output file and write the header line
  fRmsDev=open(outFilPath, 'w')
  strLine = "tNi, tCu, rmsDev\n"
  fRmsDev.write(strLine)
  

  # run the Cu thickness loop
  tCu = lThCu[0]
  sCu = lThCu[2]
  eCu = lThCu[1]+sCu
  while (tCu < eCu):
    # run the Ni thickness loop
    tNi = lThNi[0]
    sNi = lThNi[2]
    eNi = lThNi[1]+sNi
    while (tNi < eNi):
      # here is where we do the work...
      writeGmrfInNiCu(tNi, tCu, lKv, './in.txt', toa=35)
      os.system(gmrfCmd)
      a = glob.glob('F*')
      if (len(a) > 0):
        # move the output where I want it and clean up
        shutil.copy2(a[0], './out.txt')
        os.remove(a[0])
        os.remove('./in.txt')
        os.remove('STANDARD.DAT')
        # parse the results
        mod = parseNiCuKaSGPlotGMRfilmOutFile('./out.txt', verbose=False)
        lNiKaMod = mod[1]
        lCuKaMod = mod[2]
        rmsDev = 0
        l = len(lNiKaMod)
        i = 0
        while (i < l):
          delNi = lNiKaMod[i] - lNiKaKr[i]
          delCu = lCuKaMod[i] - lCuKaKr[i]
          rmsV = math.sqrt(delNi*delNi + delCu*delCu)
          rmsDev += rmsV
          i += 1
        rmsDev = rmsV / float(l)
        strLine = "%.1f, %.1f, %.5f\n" % (tNi, tCu, rmsDev)
        fRmsDev.write(strLine)
        
        # clean up
        os.remove('./out.txt')
      tNi += sNi
    tCu += sCu
  # we are done, close the KR file
  fRmsDev.close()
  

def parseNiCuKaSGPlotGMRfilmOutFile(inPath, verbose=False):
  """parseNiCuKaSGPlotGMRfilmOutFile(inPath, verbose=False)
  Parse the output file (fPath) from a StrataGEM like computation
  This returns a lists of model energy and K-ratios for each voltage:
  [le0Mod, lNiKaMod, krCuKaMod]"""
  
  le0Mod = []
  lNiKaMod = []
  lCuKaMod = []

  f = open(inPath, "r")
  lines = f.readlines()
  f.close()
  nLines = len(lines)
  if(verbose):
    print(nLines)
  recs = nLines/26
  for i in range(recs):
    rKv = 26*i + 5
    v = lines[rKv].split()[4]
    l = len(v)
    e0 = float(v[0:l-3])
    le0Mod.append(e0)
  
    rNi = 26*i + 16
    eNi = lines[rNi].split()[2]
    # convert to nm
    tNi = 0.1*float(lines[rNi].split()[6])
    # print(tNi)
    kNi = float(lines[rNi].split()[8])
    lNiKaMod.append(kNi)
    # print(kNi)

    rCu = 26*i+19
    eCu = lines[rCu].split()[2]
    # print(eCu)
    tCu = 0.1*float(lines[rCu].split()[6])
    # print(tCu)
    kCu = float(lines[rCu].split()[8])
    lCuKaMod.append(kCu)
  ret = [le0Mod, lNiKaMod, lCuKaMod]
  return (ret)

def writeGmrfInNiCu(tNi, tCu, vKv, fPath, toa=35):
  f=open(fPath, 'w')
  # f.write("S\n")
  f.write("N\n")
  f.write("F\n")
  f.write("Y\n")
  f.write("K\n")
  f.write("N\n")
  msg = "%.1f\n" % toa
  f.write(msg)
  f.write("e\n")
  f.write("Y\n")
  msg = "%.1f\n" % vKv[0]
  f.write(msg)
  f.write("3\n") # 3 layers
  f.write("1\n") # 1 element each
  f.write("1\n")
  f.write("1\n")
  f.write("NiKa\n")
  f.write("CuKa\n")
  f.write("C Ka\n")
  f.write("n\n")
  f.write("8.90\n")
  f.write("8.96\n")
  f.write("a\n")
  msg= "%.1f\n" % (10.*tNi)
  f.write(msg)
  msg= "%.1f\n" % (10.*tCu)
  f.write(msg)
  f.write("n\n")
  # f.write("y\n")
  l = len(vKv)
  i = 1
  while (i < l-1):
    f.write("E\n")
    f.write("Y\n")
    msg= "%.1f\n" % vKv[i]
    f.write(msg)
    f.write("N\n")
    # f.write("y\n")
    i += 1

  f.write("E\n")
  f.write("Y\n")
  msg= "%.1f\n" % vKv[l-1]
  f.write(msg)
  f.write("N\n")
  f.write("\n")
  f.write("n\n")
  f.write("\n")
  f.write("\n")
  f.close()

def modNiCuLayers(tNi, tCu, lKv, rptPath):
  """modNiCuLayers(tNi, tCu, lKv, rptPath)
  Compute the model StrataGEM plot curve for a given layer structure of
  tNi nm of Ni on tCu nm of Cu for the list of accelerating voltages lKv.
  Write the results (e0, krNiKa, kaCuKa) to a .csv file at rptPath
  Example:
  import os
  os.chdir("c:/temp")
  import dtsa2.papNiCu as pap
  pap.modNiCuLayers(200, 400, range(10,31), "./foo.csv")
  """
  gmrfCmd = gmrfPth + " < ./in.txt"

  writeGmrfInNiCu(tNi, tCu, lKv, './in.txt', toa=35)
  os.system(gmrfCmd)
  a = glob.glob('F*')
  if (len(a) > 0):
    # move the output where I want it and clean up
    shutil.copy2(a[0], './out.txt')
    os.remove(a[0])
    os.remove('./in.txt')
    os.remove('STANDARD.DAT')
    # parse the results
    mod = parseNiCuKaSGPlotGMRfilmOutFile('./out.txt', verbose=False)
    lNiKaMod = mod[1]
    lCuKaMod = mod[2]
    fRpt=open(rptPath, 'w')
    strLine = "e0, krNiKa, krCuLa\n"
    fRpt.write(strLine)
    i = 0
    l = len(lNiKaMod)
    while(i < l):
      strLine = "%.1f, %.5f, %.5f\n" % (lKv[i], lNiKaMod[i], lCuKaMod[i])
      fRpt.write(strLine)
      i += 1
    fRpt.close()
    os.remove('./out.txt')