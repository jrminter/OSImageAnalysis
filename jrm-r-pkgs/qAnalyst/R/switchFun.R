`switchFun` <-
function(type,argument)
{
#utent input parsing#
#analysis of charts
	if (type=="chart")
	{
		#converte i codici delle distribuzioni nel suffisso interno ad r
		out=switch(argument,"XBAR"="xbar", 
		"X-BAR"="xbar", 
		"x-bar"="xbar",
		"range"="r",
		"sd"="s",
		"individuals"="i",
		"individual"="i",
		"moving range"="mr")
		#if not finding returns whot sentd
		if (is.null(out)) out=argument
	}
#analysis of distribution
	if (type=="distribution")
	{
		#converte i codici delle distribuzioni nel suffisso interno ad r
		out=switch(argument,"normal"="norm",
		"normale"="norm",
		"dnorm"="norm",
		"dweibull"="weibull",
		"log-normal"="lnorm",
		"dlnorm"="lnorm",
		"lognormal"="lnorm",
		"exponential"="exp",
		"chi-squared"="chisq",
		"logistic"="logis"
		)
		#se l'argomento e' macciato allora restituisce il default
		if (is.null(out)) out=argument
	}
invisible(out)
}

