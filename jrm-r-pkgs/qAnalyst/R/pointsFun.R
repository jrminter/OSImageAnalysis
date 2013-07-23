`pointsFun` <-
function(x, sg, type = "xbar")
{
#xbar
if (type == "xbar")
{
points = tapply(x, sg, mean, na.rm = TRUE)
}
#r
if(type=="r")
{
points = tapply(x,sg,rFun)
}
#s
if(type=="s")
{
points=tapply(x,sg,sd,na.rm=TRUE)
}
#i Rimuove le x missing
if(type=="i")
{
points=x
}
if(type=="mr")
{
#prima c'era interval
points=mrangeFun(x,sg=sg)
}
if(type=="p")
{
probs=x/sg
#controlla che le probabilita siano in un range sensato
ifelse((probs>1 || probs <0), stop("Error! Data uncoherent with specified chart: p <0 or p>1"),NA)
points=probs
}
if(type=="np")
{
#controlla che i difetti siano non negativi
ifelse((x<0), stop("Error! Negative values in input data"),NA)
ifelse(x>sg, stop("Error! Number of defect/successer higher than number of trials"), NA)
points=x
}
if(type=="c")
{
#controlla che i punti siano non negativi
ifelse((x<0), stop("Error! Negative values in input data"),NA)
points=x
}
if(type=="u")
{
#controlla che i punti siano non negativi
ifelse((x<0), stop("Error! Negative values in input data"),NA)
ifelse((sg<=0), stop("Error! Negative values in group sizes"),NA)
ui=x/sg
points=ui
}

#restituisce l'output
return(points)
}

