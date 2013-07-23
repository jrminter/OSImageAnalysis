#######################################
#    Anderson-Darling test
#    READAPTED VERSION FROM ORIGINAL ANDERSON DARLING FROM PEGORARO ENRICO
#    AND SPANO'
# Return value: a 2-dimensional vector containing AD test value and relative p-value
#######################################
andersonDarlingFun <- function(x, distribution, theta)
{
	#from
	fun=switchFun(type="distribution", argument=distribution)
	pdist = eval(parse(text = paste("p", fun, sep = "")))
	theta=as.numeric(theta)

	x  = sort(x)
	n  = length(x)
	vecti = 1:n

	# Test statistic calculation
	#accounting for number of estimated parameters
	#if distibution takes only one parameter then na.omit(theta)==1
	if (length(na.omit(theta))==2)
	{
		pd = pdist(x,  theta[1], theta[2] )
		pdRev = pdist(rev(x),  theta[1], theta[2])} else
	{
		pd = pdist(x,  theta[1])
		pdRev = pdist(rev(x),  theta[1])
	}
	testValue = sum((1 - 2 * vecti)/n * (log(pd) + log(1 - pdRev ))) -	n
	out = testValue
	# Calculates the pvalue

		if (testValue < 0.2) {pValue <- 1 - exp(-13.436 + 101.14 * testValue - 223.73 * testValue^2)}
	    else if (testValue < 0.34) {pValue <- 1 - exp(-8.318 + 42.796 * testValue - 59.938 * testValue^2)}
	    else if (testValue < 0.6) {pValue <- exp(0.9177 - 4.279 * testValue - 1.38 * testValue^2)}
	    else if (testValue < 100) {pValue <- exp(1.2937 - 5.709 * testValue + 0.0186 * testValue^2)}  # OK
		else pValue <- 0
	out = c(AD = testValue, pvalue = pValue)		
	#######################
	return (out)
} 
