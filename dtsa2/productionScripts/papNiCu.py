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


"""A series of scripts for PAP simulations of Ni on Cu on C wrapping calls to GMRFilm
These were designed to run with the version built by J. R. Minter with Visual Fortran 6.
At least this runs on 64 bit hardware. W00t!!!
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
               e0, tNi, tCu, krNiKa, krCuKa
  Example:
  import os
  import dtsa2.papNiCu as pap
  os.chdir("C:/Temp/")
  rptFil = "./qm-03960-S4-pap-rms-dev.csv"
  lKv = [12, 15, 20, 25, 30]
  lNiKaKr = [0.87582, 0.72544, 0.44970, 0.29367, 0.19886]
  lCuKaKr = [0.03778, 0.22748, 0.48349, 0.51801, 0.45176]
  lThNi   = [195, 260, 5]
  lThCu   = [535, 620, 5]
  pap.genNiCuPetPapMatchErr(lKv, lNiKaKr, lCuKaKr, lThNi, lThCu, rptFil)
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
      os.system(myCmd)
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
  os.remove("./runIt.cmd")

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
    e0 = v[0:l-3]
    e0 = float(e0)
    le0Mod.append(e0)
  
    rNi = 26*i + 16
    eNi = lines[rNi].split()[2]
    # convert to nm
    tNi = 0.1*float(lines[rNi+1].split()[5])
    # print(tNi)
    kNi = float(lines[rNi].split()[8])
    lNiKaMod.append(kNi)
    # print(kNi)

    rCu = 26*i+19
    eCu = lines[rCu].split()[2]
    # print(eCu)
    tCu = 0.1*float(lines[rCu+1].split()[5])
    # print(tCu)
    kCu = float(lines[rCu].split()[8])
    lCuKaMod.append(kCu)
  ret = [le0Mod, lNiKaMod, lCuKaMod]
  return (ret)
  
def parseLisNiCuKrGMRfilmOutFile(inPath, verbose=False):
  """parseLisNiCuKrGMRfilmOutFile(inPath, verbose=False)
  Parse the output file (fPath) from GMRFilm Output from input
  generated with writeGmrfInNiThCu
  This returns a lists of model energy , thickness, and and K-ratios
  for each voltage:
  [lEo, lNiTh, lCuTh, lNiKa, lCuKa]"""
  
  le0 = []
  lNiTh = []
  lCuTh = []
  lNiKa = []
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
    rNi = 15*i + 16
    # eNi = lines[rNi].split( )[2]
    tNi= 0.1*float(lines[rNi+1].split( )[5])
    lNiTh.append(tNi)
    # print(tNi)
    kNi = float(lines[rNi].split()[8])
    lNiKa.append(kNi)

    rCu = 15*i + 19
    # eCu = lines[rCu].split()[2]
    # print(eCu)
    tCu = 0.1*float(lines[rCu+1].split()[5])
    lCuTh.append(tCu)
    # print(tCu)
    kCu = float(lines[rCu].split()[8])
    lCuKa.append(kCu)
  
  ret = [le0, lNiTh, lCuTh, lNiKa, lCuKa]
  return (ret)
  
def writeGmrfInNiThCu(lNi, tCu, e0, fPath, toa=35):
  """writeGmrfInNiThCu(lNi, tCu, e0, fPath, toa=35)
  Write an input file to model a list of Ni thickness (nm) at
  a single Cu thickness (tCu) and kV (e0). Write to the desired
  report path (fPath). Optionally change the takeoff angle (toa).
  
  Example:
  import os
  import dtsa2.papNiCu as pap
  os.chdir("C:/Temp/")
  lNi = range(10, 14)
  pap.writeGmrfInNiThCu(lNi, 400, 15, './in.txt')
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
  f.write("NiKa\n")
  f.write("CuKa\n")
  f.write("C Ka\n")
  f.write("n\n")
  f.write("8.90\n")
  f.write("8.96\n")
  f.write("a\n")
  # do the first thickness
  msg= "%.1f\n" % (10.*lNi[0])
  f.write(msg)
  msg= "%.1f\n" % (10.*tCu)
  f.write(msg)
  l = len(lNi)
  i = 1
  while (i < l-1):
    f.write("Y\n")
    f.write("a\n")
    msg= "%.1f\n" % (10.*lNi[i])
    f.write(msg)
    msg= "%.1f\n" % (10.*tCu)
    f.write(msg)
    i += 1
  f.write("Y\n")
  f.write("a\n")
  msg= "%.1f\n" % (10.*lNi[l-1])
  f.write(msg)
  msg= "%.1f\n" % (10.*tCu)
  f.write(msg)
  f.write("N\n")
  f.write("\n")
  f.write("n\n")
  f.write("\n")
  f.write("\n")
  f.close()
  
def writeGmrfInElThOnSub(lThLayEl, e0, fPath, lineLayEl="NiKa", rhoLayEl="8.90", lineSubEl="CuKa", toa=35):
  """writeGmrfInElThOnSub(lThLayEl, e0, fPath, lineLayEl="NiKa", rhoLayEl="8.90", lineSubEl="CuKa", toa=35)
  Write an input file to model a list of thickness values (lThLayEl, nm) 
  from an element with X-ray line (lineLayEl) and density
  (rhoLayEl) on a a substrate with X-ray line (lineSubEl)
  for a desired kV (e0) and takeoff angle (toa). Write to the desired
  report path (fPath).
  
  Example:
  import os
  import dtsa2.papNiCu as pap
  os.chdir("C:/Temp/")
  lNi = range(10, 14)
  pap.writeGmrfInElThOnSub(lNi, fPath='./in.txt')
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
    # print(tNi)
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
  
def prepNiCuKrForMatch(lNi, lCu, csvFil, e0=15, toa=35):
  """prepNiCuKrForMatch(lNi, lCu, csvFil, e0=15, toa=35)
  Compute PAP K-ratios for a range of Ni (lNi) thickness
  and a range of Ni (lNi) thickness at a single kV (e0)
  for a given take of angle (toa). Write these to a csv
  file for import into R for later matching.
  Example:
  import os
  import dtsa2.papNiCu as pap
  os.chdir("C:/Temp/")
  lNi = [10, 20, 30, 40]
  lCu = [200, 210, 220, 230, 240]
  pap.prepNiCuKrForMatch(lNi, lCu, './modelTest.csv', 15, 35)
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
  strLine = "e0, tNi, tCu, krNiKa, krCuKa\n"
  fRpt.write(strLine)
  fRpt.close()
  for tCu in lCu:
    writeGmrfInNiThCu(lNi, tCu, e0, './in.txt', toa=35)
    # rin GMRfilm
    os.system(myCmd)
    a = glob.glob('F*')
    if (len(a) > 0):
      # move the output where I want it and clean up
      shutil.copy2(a[0], './out.txt')
      os.remove(a[0])
      os.remove('./in.txt')
      os.remove('STANDARD.DAT')
      res = parseLisNiCuKrGMRfilmOutFile('./out.txt')
      # res = [le0, lNiTh, lCuTh, lNiKa, lCuKa]
      vEo = res[0]
      vNiTh = res[1]
      vCuTh = res[2]
      vNiK = res[3]
      vCuK = res[4]
      l = len(vEo)
      if (l > 0):
        fRpt=open(csvFil, 'a')
        i = 0
        while (i < l-1):
          # strLine = "e0, tNi, tCu, krNiKa, krCuKa\n"
          strLine = "%.1f, %.1f, %.1f, %.5f, %.5f\n" % (vEo[i], vNiTh[i], vCuTh[i], vNiK[i], vCuK[i])
          fRpt.write(strLine)
          i+=1
        fRpt.close()
        
    # clean up

def modNiCuLayers(tNi, tCu, lKv, rptPath):
  """modNiCuLayers(tNi, tCu, lKv, rptPath)
  Compute the model StrataGEM plot curve for a given layer structure of
  tNi nm of Ni on tCu nm of Cu for the list of accelerating voltages lKv.
  Write the results (e0, krNiKa, kaCuKa) to a .csv file at rptPath
  Example:
  import os
  import dtsa2.papNiCu as pap
  os.chdir("C:/Temp/")
  pap.modNiCuLayers(200, 400, range(10,31), "foo.csv")
  """
  
  fCmd=open("./runIt.cmd", 'w')
  strLine = "@echo off \n"
  fCmd.write(strLine)
  strLine = "C:\Apps\GMRFilm\gmrfilm.exe < %1 \n"
  fCmd.write(strLine)
  strLine = "\n"
  fCmd.write(strLine)
  fCmd.close()
  

  writeGmrfInNiCu(tNi, tCu, lKv, './in.txt', toa=35)
  
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
    mod = parseNiCuKaSGPlotGMRfilmOutFile('./out.txt', verbose=False)
    lNiKaMod = mod[1]
    lCuKaMod = mod[2]
    fRpt=open(rptPath, 'w')
    strLine = "e0, krNiKa, krCuKa\n"
    fRpt.write(strLine)
    i = 0
    l = len(lNiKaMod)
    while(i < l):
      strLine = "%.1f, %.5f, %.5f\n" % (lKv[i], lNiKaMod[i], lCuKaMod[i])
      fRpt.write(strLine)
      i += 1
    fRpt.close()
    os.remove('./out.txt')