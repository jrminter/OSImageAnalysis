`iLimitsFun` <-
function(i)
{
n = length(i)
s = sort(rep(seq(1, n),2))
i1 = s[-1]
iForLimits  = c(i[i1], 1+i[n])-0.5
iForLimits
}

