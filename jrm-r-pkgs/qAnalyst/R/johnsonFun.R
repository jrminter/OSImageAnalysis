johnsonFun<-function(x)
{
#internal function to trasform data
#according to specifif capameters
.trasformData<-function(x,parList)
{
#unlist parameters bundled in parList
gamma=parList$gamma
delta=parList$delta
xi=parList$xi
lambda=parList$lambda
type=parList$type
#for formula see JohnsonFit help from package SuppDists
u=(x-xi)/lambda
#choiche f(u)
if(type=="SL") fu=u
if(type=="SU") fu=u+sqrt(1+u^2)
if(type=="SB") fu=u/(1-u)
if(type=="SN") fu=exp(u)
#return trasformatio
out=gamma+delta*log(fu)
return(out)
}
#fit distribution, standard method
parList=JohnsonFit(x)
#calculate trasformation
y=.trasformData(x,parList)
#remove ma
y=y[!is.na(y)]
#create object
outList=list(type="johnson", parameters=as.list(parList), original=x,
transformed=y)
class(outList)="transformation"
invisible(outList)
}
