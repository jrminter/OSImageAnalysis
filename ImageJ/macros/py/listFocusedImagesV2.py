# test script for the Centre course
# Kota Miura 20131129
# fiji --headless --mem=500m /g/almf/software/scripts2/getIntensityRange3.py '0076-14--2006-01-23'

import sys, os, csv, re
from ij import ImagePlus, IJ
from org.jfree.data.statistics import BoxAndWhiskerCalculator
from java.util import ArrayList, Arrays
from ij.io import Opener

class InstBWC(BoxAndWhiskerCalculator):
    def __init__(self):
        pass



def measureOneFile(nucfilepath):
  #parent = os.path.dirname(nucfilepath)
  #gparent = os.path.dirname(parent)
  #gparentname = os.path.basename(gparent)
  #ggparent = os.path.dirname(gparent)
  iodefectflag = 0
  op = Opener()
  filetype = op.getFileType(nucfilepath)
  if filetype == Opener.TIFF:
    imp = op.openImage(nucfilepath)
    imgtitle = imp.getTitle()
    imgstats = imp.getStatistics()
    intrange = imgstats.max - imgstats.min
    #print imgtitle, imp.getWidth(), 'x', imp.getWidth(), 'Max - Min', intrange, 'SD', imgstats.stdDev
    print imgtitle, imp.getWidth(), 'x', imp.getWidth(), 'Mean', imgstats.mean, 'SD', imgstats.stdDev

  #outfilename = gparentname + imgtitle + ".csv"
  #outdir = os.path.join(ggparent, 'outfiles')
  #if not os.path.isdir(outdir):
    #os.mkdir(outdir)
  #outpath = os.path.join(ggparent, 'outfiles', outfilename)
  #print outpath
  #outlist = ["'" + imgtitle + "'", intrange, imgstats.stdDev]
    outlist = ["'" + imgtitle + "'", imgstats.mean, imgstats.stdDev]
  else:
    iodefectflag = 1
    filename = os.path.basename(nucfilepath)
    print "****** Could not open:",filename 
    outlist = ["'" + filename + "'", 1.0, 1.0]
  return outlist, nucfilepath, iodefectflag

'''
def measureWrap(path, filepathA, meanA, sdevA, ratioA, resultsList):
      results, nucfilepath = measureOneFile(path)
      resultsList.append(results)
      filepathA.append(nucfilepath)
      meanA.append(results[1])
      sdevA.append(results[2])
      ratioA.append(results[2]/results[1])
'''
def measureWrap(path, measA, resultsList):
      results, nucfilepath, iodefectflag = measureOneFile(path)
      resultsList.append(results)
      measA[0].append(nucfilepath) 
      measA[1].append(results[1]) #mean
      measA[2].append(results[2]) # sd
      measA[3].append(results[2]/results[1]) #ratio
      measA[4].append(iodefectflag) # io problem

def outlierDetection(pattern, measA):
  filtsdevA = []
  for ind, sd in enumerate(measA[2]):
    if not measA[4][ind]:
      filtsdevA.append(sd)
  #sdevlist = ArrayList(Arrays.asList(measA[2]))
  sdevlist = ArrayList(Arrays.asList(filtsdevA))
  bwc = InstBWC()
  ans = bwc.calculateBoxAndWhiskerStatistics(sdevlist)
  q1 = ans.getQ1()
  q3 = ans.getQ3()
  intrange = q3 - q1 
  outlier_offset = intrange * 1.5
  outlow = q1 - outlier_offset
  outup = q3 + outlier_offset
  filtersummary = { 'n': len(measA[2]),'Mean': ans.getMean(), 'Median': ans.getMedian(), 'Outlier-Low': outlow, 'Outlier-Up': outup }
  for i, filep in enumerate(measA[0]):
    #res = re.search(pattern, filep)
    if (measA[2][i] < outlow) or (measA[2][i] > outup):
      #print 'xxxW', res.group(2), measA[2][i]
      measA[4][i] = 1
#    else:
      #print 'W', res.group(2), measA[2][i]
      #measA[4].append(0)
  return filtersummary

def main(srcDir):
  resultsList = []
#nuc_filepathA = [] 
#nuc_meanA = []
#nuc_sdevA = []
#nuc_ratioA = []

#[filepathA, meanA, sdevA, ratioA, defectFlagA]
  nucA = [[], [], [], [], []]
  vsvA = [[], [], [], [], []]
  pmA = [[], [], [], [], []]
     
  pattern = re.compile('(.*)--W(.*)--P(.*)--Z(.*)--T(.*)--(.*)\.(.*)')
  for root, directories, filenames in os.walk(srcDir):
    filenames = sorted(filenames)
    for filename in filenames:
      path = os.path.join(root, filename)
      if filename.endswith("dapi.tif"):
        measureWrap(path, nucA, resultsList)
      if filename.endswith("cfp.tif"):
        measureWrap(path, vsvA, resultsList)
      if filename.endswith("647.tif"):
        measureWrap(path, pmA, resultsList)                 
      #print path
      #results, nucfilepath = measureOneFile(path)
      #resultsList.append(results)
      #filepathA.append(nucfilepath)
      #meanA.append(results[1])
      #sdevA.append(results[2])
      #ratioA.append(results[2]/results[1])

      #IJ.log(path)
      #imp = IJ.openImage(path)
      #imp.show()
        #imp.close()

    #print ans.getOutliers()
  nucOutliers = outlierDetection(pattern, nucA)
  vsvOutliers = outlierDetection(pattern, vsvA)
  pmOutliers = outlierDetection(pattern, pmA)

  prefixpattern = re.compile('(.*)--(.*)\.tif')
  print "nuc n =", len(nucA[4]), nucOutliers
  print "vsvg n =", len(vsvA[4]), vsvOutliers
  print "pm n=", len(pmA[4]), pmOutliers
  for i, filep in enumerate(vsvA[0]):
    res = re.search(prefixpattern, filep)
    filename = os.path.basename(filep)
    print filename, (nucA[4][i] or vsvA[4][i] or pmA[4][i]), nucA[4][i], vsvA[4][i], pmA[4][i], nucA[2][i], vsvA[2][i], pmA[2][i] 
#  print 'W', res.group(2), nucA[4][i], vsvA[4][i], pmA[4][i], nucA[2][i], vsvA[2][i], pmA[2][i] 
#  print 'W', res.group(2), vsvA[4][i], vsvA[2][i] 


  outfilename = aplate + ".csv"
  statfilename = aplate + "_Stats.csv"
  outdir = os.path.join(folderpath, 'prescreen')
  if not os.path.isdir(outdir):
    os.mkdir(outdir)
  outpath = os.path.join(outdir, outfilename)
  outstatpath = os.path.join(outdir, statfilename)
  print outpath
  print outstatpath
  headerstr = ["'filename'", "'rejection'", "'nuc_outlier'", "'vsvg_outlier'", "'pm_outlier'", "'nuc_sd'", "'vsvg_sd'", "'pm_sd'"]
  f = open(outpath, 'wb')
  writer = csv.writer(f)
  writer.writerow(headerstr)
#for res in resultsList:
#  writer.writerow(res)
  for i, filep in enumerate(nucA[0]):
    filename = os.path.basename(filep)
    res = ["'" + filename + "'", (nucA[4][i] or vsvA[4][i] or pmA[4][i]), nucA[4][i], vsvA[4][i], pmA[4][i], nucA[2][i], vsvA[2][i], pmA[2][i]]
    writer.writerow(res)
    #print res   
  f.close()

  f = open(outstatpath, 'wb')
  writer = csv.writer(f)
  writer.writerow(["'Nucleus'"])
  writer.writerow(nucOutliers.keys())
  writer.writerow(nucOutliers.values())
  writer.writerow(["'VSVG'"])
  writer.writerow(vsvOutliers.keys())
  writer.writerow(vsvOutliers.values())
  writer.writerow(["'PM'"])
  writer.writerow(pmOutliers.keys())    
  writer.writerow(pmOutliers.values())    
  f.close()

def filterdirs(folderpath):
  dirs = os.listdir(folderpath)
  pattern = re.compile('(.*)-(.*)--(.*)')
  dirlist = []
  for d in dirs:
#  if os.path.isdir(d) and d.startswith('0'):
    if d.startswith('0'):
      res = re.search(pattern, d)
      #if int(res.group(1)) > 9 and int(res.group(1)) < 160:
      if int(res.group(1)) > 45 and int(res.group(1)) < 160:
        dirlist.append(d)
  return sorted(dirlist)
  
folderpath = '/g/data/bio-it_centres_course/data/VSVG'
#folderpath = '/Volumes/data/bio-it_centres_course/data/VSVG'
#plates = ['0076-14--2006-01-23', '0308-01--2007-04-03', '0310-08--2007-04-09'] # ...will be extended
#aplate = '0076-14--2006-01-23' # name of a plate, or a folder name
#aplate = '0001-03--2005-08-01'
#aplate = '0001-04--2005-09-08'
#aplate = '0146-46--2006-01-04'
#aplate = '0010-43--2005-10-05'
#aplate = '0046-41--2005-09-27'
#aplate = '0046-48--2005-09-02'

aplate = sys.argv[1] #name of a plate, or a folder name as an argument

srcDir = os.path.join(folderpath, aplate, 'data')
print srcDir
main(srcDir)
#nucfilepath = sys.argv[1]