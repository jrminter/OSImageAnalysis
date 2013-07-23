rapidFitFun<-function(x,rounding=3, boxcox=FALSE, johnson=FALSE)
{
#this function fits some distributions to data and return goodness of fit stats
#list 
distributionToCheck=c("normal", "lognormal", "gamma", "weibull", "logistic", "cauchy")
if (boxcox==TRUE) distributionToCheck=c(distributionToCheck, "boxcox")
if (johnson==TRUE) distributionToCheck=c(distributionToCheck, "johnson")
#initial settings
theta1=rep(NA,length(distributionToCheck))
theta2=rep(NA, length(distributionToCheck))
theta1N=rep(NA,length(distributionToCheck))
theta2N=rep(NA,length(distributionToCheck))
ADpvalue=rep(NA,length(distributionToCheck))

for(i in 1:length(distributionToCheck))
{
	if (!(is.element(distributionToCheck[i], c("boxcox","johnson")))) {
	infoFun=funInfoFun(x=x,fun=distributionToCheck[i],adStats=TRUE)
	thetaVals=as.numeric(infoFun$theta)
	thetaNames=attr(infoFun$theta,"name")
	howManyPars=length(infoFun$theta)
	#there is at least one parameter whatever density we estimate
	theta1[i]=thetaVals[1]; theta1N[i]=thetaNames[1]
	if (howManyPars>1) { theta2[i]=thetaVals[2]; theta2N[i]=thetaNames[2] }
	ADpvalue[i]=as.numeric(infoFun$adInfo[2])} else {
	#johnson and box cox
	#parameters are normal data mean and sd log
	theta1N[i]="mean"; theta2N[i]="sd"
	if (distributionToCheck[i]=="boxcox") newX=boxcoxFun(x)$transformed else newX=johnsonFun(x)$transformed
	theta1[i]=mean(newX); theta2[i]=sd(newX)
	ADpvalue[i]=as.numeric(andersonDarlingFun(newX, "normal", c(mean(newX), sd(newX))))[2]
	}
}
#create summary data frame
fitFrame=data.frame(distributions=distributionToCheck, 
parameter1=theta1N, parameter2=theta2N,
theta1=round(theta1,digits=rounding), theta2=round(theta2,digits=rounding),  
ADpvalue=round(ADpvalue, digits=rounding), stringsAsFactors=FALSE)
cat("\n","Distributions fit output","\n", "---------------------","\n")

print(fitFrame)

indexBest=which(ADpvalue==max(ADpvalue))
cat("\n")
textToPrint=paste("Distribution with higher AD p-value is", distributionToCheck[indexBest])
cat("\n",textToPrint,"\n")
}
