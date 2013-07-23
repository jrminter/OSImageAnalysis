`plot.capability` <-
function(x,...)
{
capabilityObj=x
#general graphical settings
xLab=capabilityObj$summaryInfo$name
xName=paste("Capability histogram of", capabilityObj$summaryInfo$name)
hStrip=2
cexStrip=2
cexAxes=2
cexScales=2
linesWidth=2
#settings of ylim
quantiles=capabilityObj$summaryInfo$qfun(ppoints(100), 
	capabilityObj$genStats$estimate1, capabilityObj$genStats$estimate2)
densities=capabilityObj$summaryInfo$dfun(quantiles,capabilityObj$genStats$estimate1, capabilityObj$genStats$estimate2)
yLimMaxCanditate=1.1*max(densities)
##if distribution is normal shall investigate also within

if (capabilityObj$summaryInfo$distribution=="normal")
{
	quantilesWithin=capabilityObj$summaryInfo$qfun(ppoints(100), 
		capabilityObj$genStats$meanX, capabilityObj$genStats$sdWithinX)
	densities=capabilityObj$summaryInfo$dfun(quantilesWithin,capabilityObj$genStats$meanX, capabilityObj$genStats$sdWithinX)
	yLimMaxCanditate=max(yLimMaxCanditate,1.1*max(densities))
}

yLimVector=c(0,yLimMaxCanditate)


#distribution plot
options(warn=-1)
trellis.par.set('layout.heights', list (strip = hStrip))
pl = histogram( ~ capabilityObj$summaryInfo$x | xName,
strip = strip.custom (par.strip.text = list(cex = cexStrip, col = "blue")),
xlab = list(xLab, cex = cexAxes), ylab = list("Density", cex = cexAxes),
scales = list(cex=cexScales),
xlim=limitsFun(list(capabilityObj$summaryInfo$x,capabilityObj$summaryInfo$lsl, capabilityObj$summaryInfo$usl)),
,ylim=yLimVector,
,type = "density",
panel = function(x, ...) {
	panel.histogram(x, col = "lightgrey",...)
	#if normality: capability overall & capability within
	if (capabilityObj$summaryInfo$distribution=="normal")
	{
		panel.mathdensity(dmath = dnorm, col = "blue", lty=5,lwd = linesWidth,n =200,	args = list(capabilityObj$genStats$meanX, capabilityObj$genStats$sdOverallX))
		panel.mathdensity(dmath = dnorm, col = "green", lwd = linesWidth,n =200,	args = list(capabilityObj$genStats$meanX, capabilityObj$genStats$sdWithinX))
	}
	else
	{
#		panel.mathdensity(dmath = eval(parse(text = paste("d", capabilityObj$summaryInfo$distribution, sep = ""))), col="blue", lty=5, wd = linesWidth,n =200,args = list(capabilityObj$genStats$estimate1, capabilityObj$genStats$estimate2))
		panel.mathdensity(dmath = capabilityObj$summaryInfo$dfun, col="blue", lty=5, wd = linesWidth,n =200,args = list(capabilityObj$genStats$estimate1, capabilityObj$genStats$estimate2))
	}
	panel.rug(x, lwd = 1,col = "blue", ...)
	if (!is.null(capabilityObj$summaryInfo$lsl)) {panel.abline(v = capabilityObj$summaryInfo$lsl, col = "dark red", lty=1,lwd = linesWidth)}
	if (!is.null(capabilityObj$summaryInfo$usl)) {panel.abline(v = capabilityObj$summaryInfo$usl, col = "dark red", lty=1,lwd = linesWidth)}
	if (!is.null(capabilityObj$summaryInfo$target)) {panel.abline(v = capabilityObj$summaryInfo$target, col = "red", lty=5,lwd = linesWidth)}
	#			panel.abline(v = cl166, col = "green", lwd = 4)
	},
#key generation
	key = list(text =  list(legendFun(capabilityObj)$textKey, cex = 1.5), lines = list(col=legendFun(capabilityObj)$linesColorKey, lwd=2, lty=legendFun(capabilityObj)$linesLtyKey),space = "bottom", columns = legendFun(capabilityObj)$numColumns)
	)
	print(pl)
}

