import os
import dtsa2.papNiCu as pap
os.chdir("C:/Temp/")
pap.modNiCuLayers(200, 400, range(10,31), "foo.csv")


import os
import dtsa2.papNiCu as pap
os.chdir("C:/Temp/")
rptFil = "./qm-03960-S4-pap-rms-dev.csv"
lKv = [12, 15, 20, 25, 30]
lNiKaKr = [0.87582, 0.72544, 0.44970, 0.29367, 0.19886]
lCuKaKr = [0.03778, 0.22748, 0.48349, 0.51801, 0.45176]
lThNi   = [195, 260, 1]
lThCu   = [535, 620, 1]
pap.genNiCuPetPapMatchErr(lKv, lNiKaKr, lCuKaKr, lThNi, lThCu, rptFil)