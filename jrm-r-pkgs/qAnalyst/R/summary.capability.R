`summary.capability` <-
function(object,printPotential=TRUE, printOverall=TRUE, printPerc=FALSE, printZeta=FALSE,...)
{
capabilityObj=object
#initial settins
options("digits"=5)
options("scipen"=12)

#analized variable presentation
#general statistics
cat("\n", "summary of ", capabilityObj$summaryInfo$name, " capability analysis \n")
cat("\n", "Assumed distribution: ", capabilityObj$summaryInfo$distribution, "\n")
cat("\n", "---------------------", "\n")
cat("\n", "Summary statistics ","\n")

summaryStatInfo=c(capabilityObj$genStats$nTotalX,capabilityObj$genStats$nCompleteX, capabilityObj$genStats$nMissingX, capabilityObj$genStats$nGroupsX, capabilityObj$genStats$meanX, capabilityObj$genStats$sdOverallX, capabilityObj$genStats$sdWithinX)
statInfoNames=c("Total obs.", "Non missing obs.", "Missing Obs.", "Groups", "Mean", "Overall st. dev.", "Within st. dev.")
summaryStatInfo=as.matrix(summaryStatInfo)
colnames(summaryStatInfo)=c("value")
rownames(summaryStatInfo)=c(statInfoNames)
print(summaryStatInfo, digits=5)

#usl, lsl, target

cat("\n", "lsl, usl, target", "\n")
if (!is.na(capabilityObj$summaryInfo$lsl)) {	cat("Set lsl of ",capabilityObj$summaryInfo$name," is ", capabilityObj$summaryInfo$lsl, "\n")}
if (!is.na(capabilityObj$summaryInfo$usl)) {	cat("Set usl of ",capabilityObj$summaryInfo$name," is ", capabilityObj$summaryInfo$usl, "\n")}
if (!is.na(capabilityObj$summaryInfo$target)) {	cat("Set target of ",capabilityObj$summaryInfo$name," is ", capabilityObj$summaryInfo$target, "\n")}
cat("\n")

#observed ppm
#always
cat("\n", "Observed performance","\n")
if (printPerc==FALSE) 
	summaryPPMOss=c(capabilityObj$genStats$ppmTOss, capabilityObj$genStats$ppmLOss, capabilityObj$genStats$ppmUOss)
else
	summaryPPMOss=c(capabilityObj$genStats$percTOss, capabilityObj$genStats$percLOss, capabilityObj$genStats$percUOss)	

if (printPerc==FALSE) 
	ppmOssNames=c("PPM Total", "PPM < LSL", "PPM > USL")
else
	ppmOssNames=c("Perc Total", "Perc < LSL", "Perc > USL")

summaryPPMOss=as.matrix(summaryPPMOss)
colnames(summaryPPMOss)=c("value")
rownames(summaryPPMOss)=c(ppmOssNames)
format(print(summaryPPMOss, digits=5),scientific=FALSE)

#overall ppm
if (printOverall==TRUE)
{
cat("\n", "Expected overall performance","\n")

if (printPerc==FALSE) 
	summaryPPMOv=c(capabilityObj$overallStats$ppmTOv, capabilityObj$overallStats$ppmLOv, capabilityObj$overallStats$ppmUOv)
else
	summaryPPMOv=c(capabilityObj$overallStats$percTOv, capabilityObj$overallStats$percLOv, capabilityObj$overallStats$percUOv)

if (printPerc==FALSE) 
	ppmOvNames=c("PPM Total", "PPM < LSL", "PPM > USL")
else
	ppmOvNames=c("Perc Total", "Perc < LSL", "Perc > USL")

summaryPPMOv=as.matrix(summaryPPMOv)
colnames(summaryPPMOv)=c("value")
rownames(summaryPPMOv)=c(ppmOvNames)
format(print(summaryPPMOv, digits=5),scientific=FALSE)
}
#potential ppm #only normal
if (printPotential==TRUE)
{
	if (capabilityObj$summaryInfo$distribution=="normal")
	{
	cat("\n", "Expected within performance","\n")
		if (printPerc==FALSE) 
			summaryPPMPt=c(capabilityObj$potentialStats$ppmTPt, capabilityObj$potentialStats$ppmLPt, capabilityObj$potentialStats$ppmUPt)
		else
			summaryPPMPt=c(capabilityObj$potentialStats$percTPt, capabilityObj$potentialStats$percLPt, capabilityObj$potentialStats$percUPt)

		if (printPerc==FALSE) 
			ppmPtNames=c("PPM Total", "PPM < LSL", "PPM > USL")
		else
			ppmPtNames=c("Perc Total", "Perc < LSL", "Perc > USL")
	summaryPPMPt=as.matrix(summaryPPMPt)
	colnames(summaryPPMPt)=c("value")
	rownames(summaryPPMPt)=c(ppmPtNames)
	format(print(summaryPPMPt, digits=5),scientific=FALSE)
	}
}
#cp overall
if (printOverall==TRUE)
{
	cat("\n", "Overall Capability", "\n")
		if (printZeta==FALSE)
			summaryCapOverall=c(capabilityObj$overallStats$pp, capabilityObj$overallStats$ppl, capabilityObj$overallStats$ppu, capabilityObj$overallStats$ppk) else summaryCapOverall=c(capabilityObj$overallStats$zBenchOv, capabilityObj$overallStats$zLslOv, capabilityObj$overallStats$zUslOv, capabilityObj$overallStats$ppk)

		if (printZeta==FALSE)
			capOverallNames=c("pp", "ppl", "ppu", "ppk") else capOverallNames=c("zBenchOv", "Z.LSL", "Z.USL", "ppk")
 
	#if defined, com is reported
	if (!is.na(capabilityObj$genStats$cpm))
	{
		summaryCapOverall=c(summaryCapOverall, capabilityObj$genStats$cpm)
		capOverallNames=c(capOverallNames, "cpm")
	}

	summaryCapOverall=as.matrix(summaryCapOverall)
	colnames(summaryCapOverall)=c("value")
	rownames(summaryCapOverall)=capOverallNames
	print(summaryCapOverall, digits=5)
}
#potential capability
if (printPotential==TRUE)
{
	if (capabilityObj$summaryInfo$distribution=="normal")
	{
		cat("\n", "Potential Capability", "\n")
		if (printZeta==FALSE)
			summaryCapPotential=c(capabilityObj$potentialStats$cp, capabilityObj$potentialStats$cpl, capabilityObj$potentialStats$cpu, capabilityObj$potentialStats$cpk) else summaryCapPotential=c(capabilityObj$potentialStats$zBenchPt, capabilityObj$potentialStats$zLslPt, capabilityObj$potentialStats$zUslPt, capabilityObj$potentialStats$cpk)

		if (printZeta==FALSE)
			capPotentialNames=c("cp", "cpl", "cpu", "cpk") else capPotentialNames=c("zBenchOv", "Z.LSL", "Z.USL", "cpk")
		summaryCapPotential=as.matrix(summaryCapPotential)
		colnames(summaryCapPotential)=c("value")
		rownames(summaryCapPotential)=capPotentialNames
		print(summaryCapPotential, digits=5)
	}
}
}
