`limitsFun` <-
function(list)
{
vcall = unlist(list)
r = range(vcall, na.rm = TRUE)
delta = diff(r)
inc = delta*.05
lim = r+c(-inc, inc)
lim
}

