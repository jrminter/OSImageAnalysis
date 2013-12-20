# -*- coding: utf-8 -*-
# DTSA-II Script - J. R. Minter - 2013-10-15
#
# 2013-10-25 JRM Updated to use gmrfilm built using
#                Visual Fortran 6 and processing with
#                a cmd file so it works with Win7 x64
#
# 2013-10-31 JRM Added functions to model a layer on
#                a substrate.

import sys
import os
import glob
import shutil
import time
import math
import csv
import dtsa2

gmrfDir="C:/Apps/GMRFilm/"
gmrfApp="C:/Apps/GMRFilm/gmrfilm.exe"


"""A series of scripts for PAP simulations of Pd on Cu on C wrapping calls to GMRFilm
These were designed to run with the version built by J. R. Minter with Visual Fortran 6.
At least this runs on 64 bit hardware. W00t!!!
Place this file in DTSA_ROOT/lib/dtsa2/"""


def genPdCuPetPapMatchErr(lKv, lPdLaKr, lCuKaKr, lThPd, lThCu, outFilPath):
  """genPdCuPetPapMatchErr(lKv, lPdLaKr, lCuKaKr,  lThPd, lThCu, outFilPath)
  Generate the RMS error between measured and computed k-ratios
  for layers of Pd and Cu for a range of specified values
  of thickness on a PET substrate for a range of accelerating voltages using
  GMRFilm. Store these to a comma-delimited file for input into a plotting or
  k-ratio matching program. Approximate PET as C.
  Input:
  lKv        - a list of the accelerating voltages to simulate in kV.
  lCuKaKr    - a list of measured CuKa K-ratios corresponding to e0 in lKv
  lPdLaKr    - a list of measured PdLa K-ratios corresponding to e0 in lKv
  lThPd      - a list with the starting, ending, and step size for Pd thickness in nm
  lThCu      - a list with the starting, ending, and step size for Cu thickness in nm
  outFilPath - the path for the .csv file. This contains a line for each voltage with
               e0, tPd, tCu, krPdLa, krCuKa
  Example:
  import os
  import dtsa2.papPdCu as pap
  os.chdir("C:/Temp/")
  rptFil = "./qm-04025-KS1-pap-rms-dev.csv"
  lKv = [10, 12, 15, 20, 25, 30]
  lPdLaKr = [0.14713, 0.11593, 0.08533, 0.04546, 0.03498, 0.02327]
  lCuKaKr = [0.55999, 0.75381, 0.80997, 0.85107, 0.78985, 0.66039]
  lThPd   = [  5,  50, 1]
  lThCu   = [800, 850, 1]
  pap.genPdCuPetPapMatchErr(lKv, lPdLaKr, lCuKaKr, lThPd, lThCu, rptFil)
  """
               
  fCmd=open("./runIt.cmd", 'w')
  strLine = "@echo off \n"
  fCmd.write(strLine)
  strLine = "C:\Apps\GMRFilm\gmrfilm.exe < %1 \n"
  fCmd.write(strLine)
  strLine = "\n"
  fCmd.write(strLine)
  fCmd.close()
  myCmd = "runIt ./in.txt"

  # clean up any old output files in our working directory
  a = glob.glob('F*')
  if (len(a) > 0):
    os.remove(a[0])
  # open up the k-ratio output file and write the header line
  fRmsDev=open(outFilPath, 'w')
  strLine = "tPd, tCu, rmsDev\n"
  fRmsDev.write(strLine)

  # run the Cu thickness loop
  tCu = lThCu[0]
  sCu = lThCu[2]
  eCu = lThCu[1]+sCu
  while (tCu < eCu):
    # run the Pd thickness loop
    tPd = lThPd[0]
    sPd = lThPd[2]
    ePd = lThPd[1]+sPd
    while (tPd < ePd):
      # here is where we do the work...
      writeGmrfInPdCu(tPd, tCu, lKv, './in.txt', toa=35)
      os.system(myCmd)
      a = glob.glob('F*')
      if (len(a) > 0):
        # move the output where I want it and clean up
        shutil.copy2(a[0], './out.txt')
        os.remove(a[0])
        os.remove('./in.txt')
        os.remove('STANDARD.DAT')
        # parse the results
        mod = parsePdCuKaSGPlotGMRfilmOutFile('./out.txt', verbose=False)
        lPdKaMod = mod[1]
        lCuKaMod = mod[2]
        rmsDev = 0
        l = len(lPdKaMod)
        i = 0
        while (i < l):
          delPd = lPdKaMod[i] - lPdLaKr[i]
          delCu = lCuKaMod[i] - lCuKaKr[i]
          rmsV = math.sqrt(delPd*delPd + delCu*delCu)
          rmsDev += rmsV
          i += 1
        rmsDev = rmsV / float(l)
        strLine = "%.1f, %.1f, %.5f\n" % (tPd, tCu, rmsDev)
        fRmsDev.write(strLine)
        
        # clean up
        os.remove('./out.txt')
      tPd += sPd
    tCu += sCu
  # we are done, close the KR file
  fRmsDev.close()
  os.remove("./runIt.cmd")

def parsePdCuKaSGPlotGMRfilmOutFile(inPath, verbose=False):
  """parsePdCuKaSGPlotGMRfilmOutFile(inPath, verbose=False)
  Parse the output file (fPath) from a StrataGEM like computation
  This returns a lists of model energy and K-ratios for each voltage:
  [le0Mod, lPdKaMod, krCuKaMod]"""
  
  le0Mod = []
  lPdKaMod = []
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
    e0 = v[0:l-3]
    e0 = float(e0)
    le0Mod.append(e0)
  
    rPd = 26*i + 16
    ePd = lines[rPd].split()[2]
    # convert to nm
    tPd = 0.1*float(lines[rPd+1].split()[5])
    # print(tPd)
    kPd = float(lines[rPd].split()[8])
    lPdKaMod.append(kPd)
    # print(kPd)

    rCu = 26*i+19
    eCu = lines[rCu].split()[2]
    # print(eCu)
    tCu = 0.1*float(lines[rCu+1].split()[5])
    # print(tCu)
    kCu = float(lines[rCu].split()[8])
    lCuKaMod.append(kCu)
  ret = [le0Mod, lPdKaMod, lCuKaMod]
  return (ret)
  
def parseLisPdCuKrGMRfilmOutFile(inPath, verbose=False):
  """parseLisPdCuKrGMRfilmOutFile(inPath, verbose=False)
  Parse the output file (fPath) from GMRFilm Output from input
  generated with writeGmrfInPdThCu
  This returns a lists of model energy , thickness, and and K-ratios
  for each voltage:
  [lEo, lPdTh, lCuTh, lPdKa, lCuKa]"""
  
  le0 = []
  lPdTh = []
  lCuTh = []
  lPdKa = []
  lCuKa = []

  f = open(inPath, "r")
  lines = f.readlines()
  f.close()
  nLines = len(lines)
  if(verbose):
    print(nLines)
  recs = (nLines-13)/15 +1
  v = lines[5].split()[4]
  l = len(v)
  e0 = v[0:l-3]
  e0 = float(e0)
  for i in range(recs):
    le0.append(e0)
    rPd = 15*i + 16
    # ePd = lines[rPd].split( )[2]
    tPd= 0.1*float(lines[rPd+1].split( )[5])
    lPdTh.append(tPd)
    # print(tPd)
    kPd = float(lines[rPd].split()[8])
    lPdKa.append(kPd)

    rCu = 15*i + 19
    # eCu = lines[rCu].split()[2]
    # print(eCu)
    tCu = 0.1*float(lines[rCu+1].split()[5])
    lCuTh.append(tCu)
    # print(tCu)
    kCu = float(lines[rCu].split()[8])
    lCuKa.append(kCu)
  
  ret = [le0, lPdTh, lCuTh, lPdKa, lCuKa]
  return (ret)
  
def writeGmrfInPdThCu(lPd, tCu, e0, fPath, toa=35):
  """writeGmrfInPdThCu(lPd, tCu, e0, fPath, toa=35)
  Write an input file to model a list of Pd thickness (nm) at
  a single Cu thickness (tCu) and kV (e0). Write to the desired
  report path (fPath). Optionally change the takeoff angle (toa).
  
  Example:
  import os
  import dtsa2.papPdCu as pap
  os.chdir("C:/Temp/")
  lPd = range(10, 14)
  pap.writeGmrfInPdThCu(lPd, 400, 15, './in.txt')
  """
  f=open(fPath, 'w')
  f.write("N\n")
  f.write("F\n")
  f.write("Y\n")
  f.write("K\n")
  f.write("N\n")
  msg = "%.1f\n" % toa
  f.write(msg)
  f.write("e\n")
  f.write("Y\n")
  msg = "%.1f\n" % e0
  f.write(msg)
  f.write("3\n") # 3 layers
  f.write("1\n") # 1 element each
  f.write("1\n")
  f.write("1\n")
  f.write("PdLa\n")
  f.write("CuKa\n")
  f.write("C Ka\n")
  f.write("n\n")
  f.write("12.023\n")
  f.write("8.96\n")
  f.write("a\n")
  # do the first thickness
  msg= "%.1f\n" % (10.*lPd[0])
  f.write(msg)
  msg= "%.1f\n" % (10.*tCu)
  f.write(msg)
  l = len(lPd)
  i = 1
  while (i < l-1):
    f.write("Y\n")
    f.write("a\n")
    msg= "%.1f\n" % (10.*lPd[i])
    f.write(msg)
    msg= "%.1f\n" % (10.*tCu)
    f.write(msg)
    i += 1
  f.write("Y\n")
  f.write("a\n")
  msg= "%.1f\n" % (10.*lPd[l-1])
  f.write(msg)
  msg= "%.1f\n" % (10.*tCu)
  f.write(msg)
  f.write("N\n")
  f.write("\n")
  f.write("n\n")
  f.write("\n")
  f.write("\n")
  f.close()
  
def writeGmrfInElThOnSub(lThLayEl, e0, fPath, lineLayEl="PdLa", rhoLayEl="12.023", lineSubEl="CuKa", toa=35):
  """writeGmrfInElThOnSub(lThLayEl, e0, fPath, lineLayEl="PdLa", rhoLayEl="12.023", lineSubEl="CuKa", toa=35)
  Write an input file to model a list of thickness values (lThLayEl, nm) 
  from an element with X-ray line (lineLayEl) and density
  (rhoLayEl) on a a substrate with X-ray line (lineSubEl)
  for a desired kV (e0) and takeoff angle (toa). Write to the desired
  report path (fPath).
  
  Example:
  import os
  import dtsa2.papPdCu as pap
  os.chdir("C:/Temp/")
  lPd = range(10, 14)
  pap.writeGmrfInElThOnSub(lPd, fPath='./in.txt')
  """
  f=open(fPath, 'w')
  f.write("N\n")
  f.write("F\n")
  f.write("Y\n")
  f.write("K\n")
  f.write("N\n")
  msg = "%.1f\n" % toa
  f.write(msg)
  f.write("e\n")
  f.write("Y\n")
  msg = "%.1f\n" % e0
  f.write(msg)
  f.write("2\n") # 3 layers
  f.write("1\n") # 1 element each
  f.write("1\n")
  f.write(lineLayEl + "\n")
  f.write(lineSubEl + "\n")
  f.write("n\n")
  f.write(rhoLayEl + "\n")
  f.write("a\n")
  # do the first thickness
  msg= "%.1f\n" % (10.*lThLayEl[0])
  f.write(msg)
  l = len(lThLayEl)
  i = 1
  while (i < l-1):
    f.write("Y\n")
    f.write("a\n")
    msg= "%.1f\n" % (10.*lThLayEl[i])
    f.write(msg)
    i += 1
  f.write("Y\n")
  f.write("a\n")
  msg= "%.1f\n" % (10.*lThLayEl[l-1])
  f.write(msg)
  f.write("N\n")
  f.write("\n")
  f.write("n\n")
  f.write("\n")
  f.write("\n")
  f.close()
  
def parseLayOnSubGMRfilmOutFile(inPath, csvFil, verbose=False):
  """parseLayOnSubGMRfilmOutFile(inPath, csvFil, verbose=False)
  Parse the output file (fPath) from GMRFilm Output from input
  generated with writeGmrfInElThOnSub a csv file on csvFil
  This returns a lists of model energy , thickness, and and K-ratios
  for each voltage:
  [lEo, lLayTh, lLayKR, lSubKR]"""
  
  le0 = []
  lLayTh = []
  lLayKR = []
  lSubKR = []

  f = open(inPath, "r")
  lines = f.readlines()
  f.close()
  nLines = len(lines)
  if(verbose):
    print(nLines)
  recs = int((nLines-13)/12) +1
  if(verbose):
    print(recs)
  # get the voltage
  v = lines[5].split()[4]
  l = len(v)
  e0 = v[0:l-3]
  e0 = float(e0)
  # get the layer trans
  v = lines[8].split()[3]
  layLin = "KR" + v.replace(";","")
  v = lines[9].split()[1]
  subLin = "KR" + v.replace(";","")
  for i in range(recs):
    le0.append(e0)
    rLay = 12*i + 15
    # eLay = lines[rLay].split( )[2]
    tLay= 0.1*float(lines[rLay+1].split( )[5])
    lLayTh.append(tLay)
    # print(tPd)
    kLay = float(lines[rLay].split()[8])
    lLayKR.append(kLay)

    rSub = 12*i + 18
    # eSub = lines[rCu].split()[2]
    # print(eSub)
    #print(lines[rSub].split())
    kSub = float(lines[rSub].split()[7])
    lSubKR.append(kSub)
  l = len(le0)
  fRpt=open(csvFil, 'w')
  strLine = "e0, tLay, %s, %s\n" % (layLin, subLin)
  fRpt.write(strLine)
  i = 0
  while (i < l):
    # strLine = "e0, tLay, krLay, krSub\n"
    strLine = "%.1f, %.1f, %.5f, %.5f\n" % (le0[i], lLayTh[i], lLayKR[i], lSubKR[i])
    fRpt.write(strLine)
    i+=1
  fRpt.close()



def writeGmrfInPdCu(tPd, tCu, vKv, fPath, toa=35):
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
  f.write("PdLa\n")
  f.write("CuKa\n")
  f.write("C Ka\n")
  f.write("n\n")
  f.write("12.023\n")
  f.write("8.96\n")
  f.write("a\n")
  msg= "%.1f\n" % (10.*tPd)
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
  
def prepPdCuKrForMatch(lPd, lCu, csvFil, e0=15, toa=35):
  """prepPdCuKrForMatch(lPd, lCu, csvFil, e0=15, toa=35)
  Compute PAP K-ratios for a range of Pd (lPd) thickness
  and a range of Pd (lPd) thickness at a single kV (e0)
  for a given take of angle (toa). Write these to a csv
  file for import into R for later matching.
  Example:
  import os
  import dtsa2.papPdCu as pap
  os.chdir("C:/Temp/")
  lPd = [10, 20, 30, 40]
  lCu = [200, 210, 220, 230, 240]
  pap.prepPdCuKrForMatch(lPd, lCu, './modelTest.csv', 15, 35)
  """
  # first make a runIt command
  os.chdir("C:/Temp/")
  myCmd = "runIt ./in.txt"
  fCmd=open("./runIt.cmd", 'w')
  strLine = "@echo off \n"
  fCmd.write(strLine)
  strLine = "C:\Apps\GMRFilm\gmrfilm.exe < %1 \n"
  fCmd.write(strLine)
  strLine = "\n"
  fCmd.write(strLine)
  fCmd.close()
  # write the header to the csv file
  fRpt=open(csvFil, 'w')
  strLine = "e0, tPd, tCu, krPdLa, krCuKa\n"
  fRpt.write(strLine)
  fRpt.close()
  for tCu in lCu:
    writeGmrfInPdThCu(lPd, tCu, e0, './in.txt', toa=35)
    # rin GMRfilm
    os.system(myCmd)
    a = glob.glob('F*')
    if (len(a) > 0):
      # move the output where I want it and clean up
      shutil.copy2(a[0], './out.txt')
      os.remove(a[0])
      os.remove('./in.txt')
      os.remove('STANDARD.DAT')
      res = parseLisPdCuKrGMRfilmOutFile('./out.txt')
      # res = [le0, lPdTh, lCuTh, lPdKa, lCuKa]
      vEo = res[0]
      vPdTh = res[1]
      vCuTh = res[2]
      vPdK = res[3]
      vCuK = res[4]
      l = len(vEo)
      if (l > 0):
        fRpt=open(csvFil, 'a')
        i = 0
        while (i < l-1):
          # strLine = "e0, tPd, tCu, krPdLa, krCuKa\n"
          strLine = "%.1f, %.1f, %.1f, %.5f, %.5f\n" % (vEo[i], vPdTh[i], vCuTh[i], vPdK[i], vCuK[i])
          fRpt.write(strLine)
          i+=1
        fRpt.close()
        
    # clean up

def modPdCuLayers(tPd, tCu, lKv, rptPath):
  """modPdCuLayers(tPd, tCu, lKv, rptPath)
  Compute the model StrataGEM plot curve for a given layer structure of
  tPd nm of Pd on tCu nm of Cu for the list of accelerating voltages lKv.
  Write the results (e0, krPdLa, kaCuKa) to a .csv file at rptPath
  Example:
  import os
  import dtsa2.papPdCu as pap
  os.chdir("C:/Temp/")
  pap.modPdCuLayers(20, 400, range(10,31), "foo.csv")
  """
  
  fCmd=open("./runIt.cmd", 'w')
  strLine = "@echo off \n"
  fCmd.write(strLine)
  strLine = "C:\Apps\GMRFilm\gmrfilm.exe < %1 \n"
  fCmd.write(strLine)
  strLine = "\n"
  fCmd.write(strLine)
  fCmd.close()
  

  writeGmrfInPdCu(tPd, tCu, lKv, './in.txt', toa=35)
  
  myCmd = "runIt ./in.txt"
  os.system(myCmd)

  a = glob.glob('F*')
  if (len(a) > 0):
    # move the output where I want it and clean up
    shutil.copy2(a[0], './out.txt')
    os.remove(a[0])
    os.remove('./in.txt')
    os.remove('STANDARD.DAT')
    os.remove('./runIt.cmd')
    # parse the results
    mod = parsePdCuKaSGPlotGMRfilmOutFile('./out.txt', verbose=False)
    lPdKaMod = mod[1]
    lCuKaMod = mod[2]
    fRpt=open(rptPath, 'w')
    strLine = "e0, krPdLa, krCuKa\n"
    fRpt.write(strLine)
    i = 0
    l = len(lPdKaMod)
    while(i < l):
      strLine = "%.1f, %.5f, %.5f\n" % (lKv[i], lPdKaMod[i], lCuKaMod[i])
      fRpt.write(strLine)
      i += 1
    fRpt.close()
    os.remove('./out.txt')