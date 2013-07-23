#########qAnalyst package v 2.0
#########
#########variables chart demo


require(qAnalyst)


#x-bar chart
data(cranks)
xbarchart=spc(x=cranks$crankshaft, sg=cranks$workingDay, type="xbar")
print(xbarchart)
plot(xbarchart)
summary(xbarchart)

cat("Press enter key to continue","\n")
foo <- readLines(stdin(), 1) 


#r-bar chart with testType=3
data(cranks)
rbarchart=spc(x=cranks$crankshaft, sg=cranks$workingDay, type="r", testType=3, k=6,p=6,nSigma=0, name="cranks")
plot(rbarchart)
summary(rbarchart)

cat("Press enter key to continue","\n")
foo <- readLines(stdin(), 1) 


#s-chart
data(faults)
sbarchart=spc(x=faults$faults, sg=faults$shift, type="s", name="faults")
plot(sbarchart)
summary(sbarchart)

