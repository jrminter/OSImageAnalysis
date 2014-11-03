# test script for the Centre course
# Kota Miura 20131129
# fiji --mem=500m /g/almf/software/scripts2/getIntensityRange.py
# https://gist.githubusercontent.com/cmci/7711190/raw/320d6dcca85e1e2f86cf58c443b8e3760cd9e5ed/getIntensityRange.py

import sys, os, csv
from ij import ImagePlus, IJ

nucfilepath = sys.argv[1]
#nucfilepath = '/Volumes/cmci/vsvgraw/0021-02--2005-09-14/data/--W00001--P00001--Z00000--T00000--dapi.tif'
#nucfilepath = '/g/cmci/vsvgraw/0021-02--2005-09-14/data/--W00001--P00001--Z00000--T00000--dapi.tif'
#nucfilepath = '/g/data/bio-it_centres_course/data/VSVG/0076-14--2006-01-23/data/--W00100--P00001--Z00000--T00000--nucleus-dapi.tif'

parent = os.path.dirname(nucfilepath)
gparent = os.path.dirname(parent)
gparentname = os.path.basename(gparent)
ggparent = os.path.dirname(gparent)

imp = IJ.openImage(nucfilepath)
imgtitle = imp.getTitle()
imgstats = imp.getStatistics()
intrange = imgstats.max - imgstats.min

print imgtitle, imp.getWidth(), 'x', imp.getWidth(), 'Max - Min', intrange, 'SD', imgstats.stdDev

outfilename = gparentname + imgtitle + ".csv"
outpath = os.path.join(ggparent, 'outfiles', outfilename)
print outpath

outlist = [intrange, imgstats.stdDev]

f = open(outpath, 'wb')
writer = csv.writer(f)
writer.writerow(outlist)
f.close()
