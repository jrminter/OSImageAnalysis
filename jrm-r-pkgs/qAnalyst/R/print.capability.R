`print.capability` <-
function(x,...)
{
capabilityObj=x

#initial settings
#initial settins
options("digits"=2)
options("scipen"=6)

#essential object presentation
cat("\n", "Capability analysis of ", capabilityObj$summaryInfo$name, "\n")
cat("mean of ",capabilityObj$summaryInfo$name," is ", capabilityObj$genStats$meanX, "\n")
cat("Total observations of ",capabilityObj$summaryInfo$name," ",  capabilityObj$genStats$nTotalX,"\n")
cat("Non missing observations: ", capabilityObj$genStats$nCompleteX, "\n")
cat("total ppm observed of ",capabilityObj$summaryInfo$name," are ", capabilityObj$genStats$ppmTOss, "\n")

#usl, lsl, target
if (!is.na(capabilityObj$summaryInfo$lsl)) {	cat("Set lsl of ",capabilityObj$summaryInfo$name," is ", capabilityObj$summaryInfo$lsl, "\n")}
if (!is.na(capabilityObj$summaryInfo$usl)) {	cat("Set usl of ",capabilityObj$summaryInfo$name," is ", capabilityObj$summaryInfo$usl, "\n")}
if (!is.na(capabilityObj$summaryInfo$target)) {	cat("Set target of ",capabilityObj$summaryInfo$name," is ", capabilityObj$summaryInfo$target, "\n")}

#base statistics presentation. If present only overall statistics
if (!is.na(capabilityObj$overallStats$pp)) {	cat("Estimated pp of ",capabilityObj$summaryInfo$name," is ", capabilityObj$overallStats$pp, "\n")}
if (!is.na(capabilityObj$overallStats$ppl)) {cat("Estimated ppl of ",capabilityObj$name," is ", capabilityObj$overallStats$ppl, "\n")}
if (!is.na(capabilityObj$overallStats$ppu)) {cat("Estimated ppu of ",capabilityObj$name," is ", capabilityObj$overallStats$ppu, "\n")}
if (!is.na(capabilityObj$overallStats$ppk)) {cat("Estimated ppk of ",capabilityObj$name," is ", capabilityObj$overallStats$ppk, "\n")}
if (!is.na(capabilityObj$genStats$cpm)) {cat("Estimated cpm of ",capabilityObj$name," is ", capabilityObj$genStats$cpm, "\n")}
}

