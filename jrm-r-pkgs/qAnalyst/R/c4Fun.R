`c4Fun` <-
function(x)
{
#bug: numeric overflow (corrected)
.calculate<-function(x)
{if (x<342) {
	num=gamma((x+1)/2)
	den=gamma(x/2)
	out=sqrt(2/x)*num/den
	#c4Fun limits to 1 when x -> Inf
	#but R creates numeric errors
	#then i is posed equal to one
	} else out=1
	invisible(out)
}
out=sapply(x,.calculate)
return(out)
}

