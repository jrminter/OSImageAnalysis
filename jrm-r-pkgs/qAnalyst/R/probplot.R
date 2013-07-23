probplot<-function (x, distribution, theta,confintervals=FALSE, confidence=.95, name=deparse(substitute(x)))
{
	options(warn=-1)
	if(missing(theta))
	{
	#parameters shall be estimated
	#estimates parameters and saves in interval variabiles
#	print("here")
	infoFun=funInfoFun(x, fun=distribution, adStats=TRUE)
     qdist=infoFun$qfun
     pfun=infoFun$pfun
	theta=infoFun$theta
	#used in building legend
	densfun=infoFun$densfun
	estimatesValues=round(as.numeric(infoFun$theta),digits=2)
	estimatesNames=attr(infoFun$theta, "name")
	adValues=round(as.numeric(infoFun$adInfo),digits=2)
	adNames=attr(infoFun$adInfo, "name")
	} else {
	#when parameters are given
	#gives fun a standard name
	fun=switchFun(type="distribution", argument=distribution)
	qdist = eval(parse(text = paste("q", fun, sep = "")))
	pfun= eval(parse(text = paste("p", fun, sep = "")))
	theta=as.numeric(theta)
	densfun=distribution
	estimatesValues=round(theta,digits=2)
	#get specific distribution values
	estimatesNames=attr(funInfoFun(x,distribution,adStats=FALSE)$theta,"name")
	adValues=round(andersonDarlingFun(x,distribution,theta),digits=2)
	adNames=c("AD","pvalue")
	}
	#this function treats no more than 2 parameters
	if (length(theta)>1){
     	theta1=theta[1]
		theta2=theta[2]
	} else {
		theta1=theta[1]
		theta2=NA}
     xlab = name
     x <- sort(na.omit(x))
	#internal function to calculate  quantiles easier
    .QFUN <- function(p) {
	    if (!is.na(theta2))
		    {qdist(p, theta1, theta2)}
		else
		   {qdist(p, theta1)}
    }
	#calculates theoretical quantioles 
   y <- .QFUN(ppoints(length(x)))
	#determining probs to plot
        probs <- c(0.01, 0.05, seq(0.1, 0.9, by = 0.1), 0.95, 
            0.99)
        if (length(x) >= 1000) 
            probs <- c(0.001, probs, 0.999)
	qprobs <- .QFUN(probs)

	#some graphical settings
	textCex=2
	stripCex=2
	stripDim=3
	scalesCex=2
	stripDim=2

	rangeY=range(c(y, qprobs))
    ablineH= qprobs#, col = "grey")
	ablineV=quantile(x,probs)#, col="grey")
    xl <- quantile(x, c(0.25, 0.75))
    yl <- qdist(c(0.25, 0.75), theta1, theta2)
    slope <- diff(yl)/diff(xl)
    int <- yl[1] - slope * xl[1]
	if (confintervals==TRUE)
	{
	  teor=int+slope*x
	  theorF=pfun(teor,theta1, theta2)
	 #variance of theorical distr
	  varF=theorF*(1-theorF)/length(x)
	#confidence interval
	  cu=theorF+qnorm(1-(1-confidence)/2)*sqrt(varF)
	  cl=theorF+qnorm((1-confidence)/2)*sqrt(varF)
	#not plot all points that have probability <0 >1
	  warnUp=which(cu>max(probs))
	  warnDown=which(cl<min(probs))
	  warns=union(warnUp, warnDown)
	  xToPlot=x[-warns]
	  cuToPlot=cu[-warns]
	  clToPlot=cl[-warns]
	#calculates quantiles
	  quToPlot=qdist(cuToPlot,theta1, theta2)
  	  qlToPlot=qdist(clToPlot,theta1, theta2)
	}
	{
		#info about thetas and AD 
		legendText=distribution
		#adds informations about parameters
		#create legend
		for (i in 1:length(estimatesValues))
		{
			addItem=paste(estimatesNames[i], estimatesValues[i], sep=" ")
			legendText=c(legendText, addItem)
		}
		#adds information about ad
		#adds AD
		for (i in 1:length(adValues))
		{
			addItem=paste(adNames[i], adValues[i], sep=" ")
			legendText=c(legendText, addItem)
		}			
	}
	titleXYPlot=paste(distribution, "probability plot", sep=" ")
	trellis.par.set('layout.heights', list (strip = stripDim))
	xyplot(y~x|titleXYPlot, 
	xlab=list(name, cex=textCex), ylab=list("probability", cex=textCex),
	scales=list(cex=scalesCex, y=list(at = qprobs, labels = format(probs,digits=4))),
	strip = strip.custom (par.strip.text = list(cex = stripCex,col="blue")),
	ylim = rangeY,
	panel=function(x,y,...)
	{
		panel.points(x,y,col="red",pch=16,cex=0.5,...)
		panel.abline(h=ablineH,col="grey")
		panel.abline(v=ablineV,col="grey")
		panel.abline(a=int, b=slope, col = "blue", lwd=2)
	if (confintervals==TRUE){ 
		panel.lines(xToPlot, quToPlot, type="l",lwd=2,lty=5,col="black" )
		 panel.lines(xToPlot, qlToPlot, type="l",lwd=2, lty=5,col="black" )}	
	}
	 ,key=list(text=list(legendText,cex=1.5),space="right")
	)
}
