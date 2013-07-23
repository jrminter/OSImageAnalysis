`mrangeFun` <-
function(x=x, sg=1)
{
if (length(x) <=sg) stop("Error! Too wide specified lag interval")
out1=diff(x,lag=sg)
#put absolute values
out1=abs(out1)
#output showes as  NA as much is initial lag set
initials=rep(NA,sg)
#li concatena e re
out=c(initials,out1)
return(out)
}

