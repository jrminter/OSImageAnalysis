invCpFun = function(x,  cp=1, fun="normal")
{
#some checks
#rm na
x=as.numeric(na.omit(x))

infoFun = funInfoFun(x, fun)
	#parameters
theta = infoFun$theta	
	#Density Function
	#dfun = infoFun$dfun
	#Quantile Function
qfun = infoFun$qfun
	#spec limits for Cp = CpK = 1
out = qfun(pnorm(c(-cp*3, cp*3)), theta[1], theta[2])
	#y lim for density
attr(out,"names")=c("lsl", "usl")
return(out)
}
