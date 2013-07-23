#########qAnalyst package v 2.0
#########
#########individual values chart


require(qAnalyst)



#i-chart, moving range to estimate st. dev. is equal to 2 points with testType=1
data(rawWeight)
ichart=spc(x=rawWeight$rawWeight, sg=2, type="i", name="weight", testType=1)
plot(ichart)
summary(ichart)


cat("Press enter key to continue\n")
foo <- readLines(stdin(), 1) 



#mr-chart, moving range is equal to two points
mrchart=spc(x=rawWeight$rawWeight, sg=2, type="mr", name="weight")
plot(mrchart)
summary(mrchart)



cat("Press enter key to continue\n")
foo <- readLines(stdin(), 1) 

#c chart
data(blemish)
cchart=spc(x=blemish$blemish,  type="c", name="blemish on linen")
plot(cchart)
summary(cchart)

