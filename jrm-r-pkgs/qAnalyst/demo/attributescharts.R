
#########qAnalyst package v 2.0
#########
#########attributes charts demo


require(qAnalyst)

#p chart
data(tubes)
pchart=spc(x=tubes$rejects, sg=tubes$sampled, type="p", name="defective tubes", testType=1,nSigma=3, k=1,p=1)
plot(pchart)
summary(pchart)

cat("Press enter key to continue","\n")
foo <- readLines(stdin(), 1) 


#npchart
npchart=spc(x=tubes$rejects, sg=tubes$sampled, type="np", name="defective tubes")
plot(npchart)
summary(npchart)

cat("Press enter key to continue","\n")
foo <- readLines(stdin(), 1) 


#u chart
data(toyCarsDefects)
uchart=spc(x=toyCarsDefects$defects, sg=toyCarsDefects$sampled, type="u", name="Toy car defects")
plot(uchart)
summary(uchart)


