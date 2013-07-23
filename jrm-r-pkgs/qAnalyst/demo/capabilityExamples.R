#########qAnalyst package v 2.0
#########
#########normal data capability analysis demo

require(qAnalyst)

#normal data
data(brakeCap)
hdnssCap=capabilityNormal(x=brakeCap$hardness, sg=brakeCap$subgroup, lsl=39, usl=41, target=40.2,  name="HARDNESS")
summary(hdnssCap)
plot(hdnssCap)

cat("Press enter key to continue\n")
foo <- readLines(stdin(), 1) 



#non normal data

data(warpTiles)
wrpCap=capabilityNotNormal(x=warpTiles$warping, usl=8, distribution="weibull")
plot(wrpCap)
summary(wrpCap)
