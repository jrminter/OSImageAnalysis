`getCoeffFun` <-
function(sampleSize, coeff)
{
n = length(sampleSize)
out = numeric(n)
for(i in 1:n)
{
	 #GETPARAMETER takes in account also n=1 dimension
	out[i] = getParameterFun(sampleSize[i],coeff)
}
out
}

