`xLimitsFun` <-
function(x)
{
n = length(x)
s = sort(rep(seq(1, n),2))
x1 = s[-c(2*n)]
xForLimits = x[c(x1,n)]
xForLimits
}

