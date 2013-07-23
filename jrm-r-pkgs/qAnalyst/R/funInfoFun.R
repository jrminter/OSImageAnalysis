funInfoFun = function(x, fun, adStats=TRUE)
	{
	#changes distribution name
	fun=switchFun(type="distribution", argument=fun)
	#uses internal function to fit parameters
	hasEstimate=FALSE

	if (fun == "norm") 
	{
		densfun="normal"
		functionFit=fitdistr(x,densfun=densfun)
		theta=as.numeric(functionFit$estimate)
		hasEstimate=TRUE
		
	} 
	if  (fun == "exp") 
	{
		densfun="exponential"
		functionFit=fitdistr(x,densfun=densfun)
		theta=as.numeric(functionFit$estimate)
		hasEstimate=TRUE
	} 
	if (fun == "chisq") 
	{
		densfun="chi-squared"
		functionFit=fitdistr(x,densfun=densfun)
		theta=as.numeric(functionFit$estimate)
		hasEstimate=TRUE
	} 
	if (fun == "logis")
	{
		densfun="logistic"
		functionFit=fitdistr(x,densfun=densfun)
		theta=as.numeric(functionFit$estimate)
		hasEstimate=TRUE
	}
	if (fun == "lnorm")
	{
		densfun="lognormal"
		functionFit=fitdistr(x,densfun=densfun)
		theta=as.numeric(functionFit$estimate)
		hasEstimate=TRUE
	} #ossia stima la gamma, la f, la beta, la t, la weibull, HASESTIMATE=STILL FALSE
	if (hasEstimate==FALSE)
	{
		densfun=fun
		functionFit=fitdistr(x, densfun=fun)
		theta=as.numeric(functionFit$estimate)
		hasEstimate==TRUE
	}
	#Density Function
	dfun = eval(parse(text = paste("d", fun, sep = "")))
	#Quantile Function
	qfun = eval(parse(text = paste("q", fun, sep = "")))
	#Probability Function
	pfun = eval(parse(text = paste("p", fun, sep = "")))
  #Random generation Function
	rfun = eval(parse(text = paste("r", fun, sep = "")))
	#put names
	thetaNames=attr(functionFit$estimate,"name")
	attr(theta,"name")=thetaNames
	#calculates anderson darling if requiresd
	adInfo=c(NA,NA)
	attr(adInfo, "name")=c("AD", "pvalue")	
	infoFun = list(densfun=densfun, theta = theta, qfun = qfun, dfun = dfun, pfun = pfun, rfun=rfun, adInfo=adInfo)
	if (adStats==TRUE)
	{
		adInfo=andersonDarlingFun(x=x,distribution=fun, theta=theta)
		infoFun = list(densfun=densfun, theta = theta, qfun = qfun, dfun = dfun, pfun = pfun, rfun=rfun, adInfo=adInfo)
	}
	class(infoFun)="infoFun"
	return(infoFun)
}
