print.transformation<-function(x,...)
{
	#get trasformation object 
	trasfObj=x
	#pretty prints name
	variableName=deparse(substitute(x))
	cat("\n", trasfObj$type, " transformation of variable ", variableName, "\n")
	cat("Parameter(s) estimation","\n")
	##prints parameters
	print(trasfObj$parameters)
}
