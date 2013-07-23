summary.infoFun<-function(object,...)
{
	infoFunObj=object
	cat("\n","Hypotized distibution is ",infoFunObj$densfun, "\n")
	intermediate=c(attr(infoFunObj$theta, "name"))
	parsText=cat("\n","Estimated values for", intermediate,
	round(as.numeric(infoFunObj$theta),digits=3),"\n")
	parsText
	if (!is.na(as.numeric(infoFunObj$adInfo)[1]))  {
	cat("\n","AD statistic is", 
	round(as.numeric(infoFunObj$adInfo[1]),digits=3),
	", corresponding p-value", 
	round(as.numeric(infoFunObj$adInfo[2]),digits=3)
	,"\n")}
}