`sgFun` <-
function(x,sg,type)
{
num=length(x)
lensg=length(sg)
#checks dimension
if(lensg>1 && (num!=lensg)) stop("Error! If sg is a vector, it shall have the same dimension of x")
#checks NA
if (lensg==1 && is.na(sg)) stop("Error! Sg must be specified")

#individual values charts
#not need to change sg
#beacause it is the width of moving range
if (is.element(type,c("i", "mr")))
{
	sg=sg
}

if (type=="c")
{
	#subgroups are individual values
	sg=rep(1,num)
}
#attribute charts
if(is.element(type,c("p", "np", "u")))
{
if (lensg==1) sg=rep(sg,num)
}
#subgroups chart or capability analysis
if(is.element(type,c("xbar", "r", "s", "capability")))
{
if (lensg==1)
{
	dimens=sg
	#quanti sono i sottogruppi
	ns=ceiling(num/dimens)
	#replica da uno a ns ciascuno max dimens per un totale di num elementi
	sg=rep(1:ns, each=dimens, len=num)
}
}

##if chart is not i, mr, c
##sg is a vector
##it makes that this vector is between 1 and length(unique(sg))
if (!is.element(type, c("i", "mr", "c","p","np", "u")))
{
	currentIndex=1
	sgOld=sg
	sg[1]=1
	for (i in 2:length(sg))
	{
		if (sgOld[i]==sgOld[i-1]) sg[i]=currentIndex else {currentIndex=currentIndex+1; sg[i]=currentIndex}
	}
}
return(sg)
}
