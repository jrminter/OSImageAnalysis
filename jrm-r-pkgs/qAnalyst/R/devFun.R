`devFun` <-
function(x, center="mean")
{
#if center is "mean" allora
if (center=="mean")
{
xbar=mean(x,na.rm=TRUE)
diffs=(x-xbar)^2
}
else
{
diffs=(x-center)^2
}
out=sum(diffs,na.rm=TRUE)
return(out)
}

