# Local system configuration options
import os
home=os.environ['HOME']


# relative path to where we want to store the data
relStd="/work/proj/QM13-02-05D-Irving/dat/dtsa-sim/std/"

# refDir is the location of the references
refDir = home+relStd
spcFile = refDir+"CuO-50nm-std.msa"
# print spcFile

cuo = ept.SpectrumFile.open(spcFile)[0]
cuo.getProperties().setNumericProperty(epq.SpectrumProperties.FaradayBegin,1.0)
display(cuo)
