`statsSpcFun` <-
function(x,sg,type=type)
{
#general
numTot=length(x) #output
numNNmissing=length(na.omit(x)) #output
numMissing=numTot-numNNmissing #outpuit
#total mean and variance
meanX=mean(x,na.rm=TRUE) #output
varTotX=var(x,na.rm=TRUE)
sdTotX=sqrt(varTotX) #output
devTotX=(varTotX)*(countFun(x)-1) # sample variance
#minimi e massimi
minX=min(x,na.rm=TRUE) #output
maxX=max(x,na.rm=TRUE) #output

sdWithinX=0 #
sdBetweenX=sdTotX # 
meanRangeOfX=NA #
sdBetween=sdTotX

# verifies subgroup length
if (length(sg)>1)
{
if (!is.element(type, c("i","mr", "c", "p", "np", "u")))
{
nGroupsX=length(unique(sg)) # number of grup equal to numer of unique(groups)
} else {
nGroupsX=length(sg) }} else {
nGroupsX=sg #individual value chart 
}
#statistics for variable charts
if(!is.element(type,c("i","mr", "c", "p", "np", "u")))
{
#verify
meansVector = tapply(x, sg, mean, na.rm = TRUE)
niVector = tapply(x, sg, countFun)
variancesVector = tapply(x, sg, var, na.rm=TRUE)

#when sample variance is not computalble lengt(sg)=1 -> var=0
variancesVector[is.na(variancesVector)]=0
variancesVector[is.nan(variancesVector)]=0

deviancesVector=(variancesVector)*(niVector-1)

#varWithin
varWithin=sum(deviancesVector)/(numNNmissing-nGroupsX)
sdWithinX=sqrt(varWithin) #return

#var Between = var Tot
varBetween=max(0,varTotX-varWithin)
sdBetweenX=sqrt(varBetween) #return
vettoreRanges=tapply(x,sg,rFun)
meanRangeOfX=mean(vettoreRanges, na.rm=TRUE) #return
}
#
#
if (is.element(type,c("np", "p","u")))
{

#
if(type=="np" || type=="p")
{
#verify
#
probs=x/sg
varianzeGruppi=sg*probs*(1-probs)
#classiche scomposizioni basate sull'assunzione di binomialita all'interno dei sottogruppi
#vanno verificate perch<e non sommano ad 1
varWithin=mean(varianzeGruppi,na.rm=TRUE)
varBetween=var((sg*probs),na.rm=TRUE)
sdWithinX=sqrt(varWithin)
sdBetweenX=sqrt(varBetween)
#poniamo il range medio a maxX-minX
meanRangeOfX=maxX-minX
}
else #carte u
{
#verify
#hp poissoniana
varianzeGruppi=x 
varWithin=mean(varianzeGruppi,na.rm=TRUE)
varBetween=var(x,na.rm=TRUE)
sdWithinX=sqrt(varWithin)
sdBetweenX=sqrt(varBetween)
#averageRange=max - x
meanRangeOfX=maxX-minX
}
}


#individual value charts
if (is.element(type,c("i", "mr","c")))
{
movingrange=mean(mrangeFun(x),na.rm=TRUE)
meanRangeOfX=movingrange
}

statisticsList=list()
#general
statisticsList$numTot=numTot
statisticsList$numNNmissing=numNNmissing
statisticsList$numMissing=numMissing
statisticsList$nGroupsX=nGroupsX
#position
statisticsList$meanX=meanX
statisticsList$minX=minX
statisticsList$maxX=maxX
#variability
statisticsList$sdTotX=sdTotX
statisticsList$sdWithinX=sdWithinX
statisticsList$sdBetweenX=sdBetweenX

statisticsList$meanRangeX=meanRangeOfX
invisible(statisticsList)
}

