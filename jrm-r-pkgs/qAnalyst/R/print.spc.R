print.spc <-
function(x, ...)
{
spcObj = x
title=paste(spcObj$general$chartType, " chart of ", spcObj$general$xName, sep="")
cat("\n",title,"\n")
#prints out gerneral statistics

cat("\n",spcObj$general$xName, " main stats", "\n", "------------------------------------------","\n")

namesGenStats=c("Total observations", "complete observations", "missing observations", "number of groups",
		"Mean", "min", "max","total std. dev." , "average range")
			
genStats=c(spcObj$general$numTot, spcObj$general$numNNmissing, spcObj$general$numMissing, spcObj$general$nGroupsX,
		spcObj$general$meanX, spcObj$general$minX, spcObj$general$maxX,
		spcObj$general$sdTotX,  spcObj$general$meanRangeX)
#creates a matrix
genStats=as.matrix(genStats)
colnames(genStats)=c("value")
rownames(genStats)=c(namesGenStats)
print(genStats)
}
