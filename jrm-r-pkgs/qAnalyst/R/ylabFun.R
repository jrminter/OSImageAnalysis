`ylabFun` <-
function(xName, type = "xbar")
{
#XBar
if (type == "xbar")
{
ylab = paste("Averages of", xName)
}
#Rchart
if(type=="r")
{
ylab = paste("Sample ranges of", xName)
}
#Schart
if(type=="s")
{
ylab = paste("Sample standard deviations of", xName)
}
#I chart
if(type=="i")
{
ylab = paste("Individual values of",xName)
}
if(type=="mr")
#MR charrt
{
ylab = paste("Moving range of",xName)
}
#P chart
if(type=="p")
{
ylab = paste("Probability of",xName)
}
if(type=="np")
#genericamente "casi"
#NP charrt
{
ylab = paste("Cases of",xName)
}
#c chart
if(type=="c")
{
ylab=paste("Cases of", xName)
}
if(type=="u")
{
ylab=paste("Cases of", xName)
}

return(ylab)
}

