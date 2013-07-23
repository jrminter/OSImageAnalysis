`capabilityNormal` <-
function(x,sg=length(x),lsl=NULL,usl=NULL,target=NULL, name=deparse(substitute(x)), toler=6, historicalMean = NA, historicalSd = NA)
{

#coherence testing
if (is.null(lsl) && is.null(usl)) stop("Error! Capability analysis requires at least a specification limit")
if (!(toler>0)) stop("Error! tolerance constant must be positive")
#checks usl > lsl
if ((!(is.null(lsl))) && (!(is.null(usl)))) { if (!(usl>lsl)) stop("Error! usl shall be greather than lsl") }

#codes subgroup
sg=sgFun(x=x, sg=sg, type="capability")
#geenrate object
capabilityObj=list()

#general info
summaryInfo=list()
summaryInfo$name=name
if (is.null(lsl)) summaryInfo$lsl=NA else summaryInfo$lsl=lsl
if (is.null(usl)) summaryInfo$usl=NA else summaryInfo$usl=usl
if (is.null(target)) summaryInfo$target=NA else summaryInfo$target=target
#as is a normal capability
summaryInfo$distribution="normal"
summaryInfo$x=x

#general statistics
genStats=list()

nTotalX=length(x)
nCompleteX=length(na.omit(x))
nMissingX=nTotalX-nCompleteX
nGroupsX=length(unique(sg))
meanX=ifelse(is.na(historicalMean), mean(x,na.rm=TRUE), historicalMean)
sdOverallX=sd(x,na.rm=TRUE)

#ppm overall calculations
ppmLOss=NA
ppmUOss=NA
if (!is.null(lsl)) ppmLOss=1000000*(length(x[x<lsl]))/nCompleteX
if (!is.null(usl)) ppmUOss=1000000*(length(x[x>usl]))/nCompleteX
ppmTOss=sum(c(ppmLOss,ppmUOss))
#setted down

#setting parameters as defaul
cpm=NA; cp=NA; pp=NA
ppmLOv=NA; ppmUOv=NA;  percLOv=NA; percUOv=NA
ppmLPt=NA; ppmUPt=NA;  percPt=NA; percUPt=NA
ppmTOv=NA; ppmTPt=NA;  percTOv=NA; percTPt=NA
cpu=NA; ppu=NA; cpl=NA; ppl=NA; cpk=NA

zLslPt=NA;zUslPt=NA;zBenchPt=NA
zLslOv=NA;zUslOv=NA;zBenchOv=NA

#estimate within sdt
#if given no problem
#need to distinguish one o more subgroups
#use mrange if more than 1 per groups

#informations about distribution
infoFun=funInfoFun(x,summaryInfo$distribution)

#setting specific distribution parameters
pdist=infoFun$pfun
qdist=infoFun$qfun
ddist=infoFun$dfun




if (is.na(historicalSd)==TRUE) {
	if (nGroupsX<nTotalX) {
		#need a deviance vector
		devVector=tapply(x,sg,devFun,center="mean")
		sampleVector=tapply(x,sg,countFun)
		#find pooled sd
		tempVector=sampleVector-1
		sdPooled=sqrt(sum(devVector,na.rm=TRUE)/sum(tempVector,na.rm=TRUE))
		#use unbiasing costant
		degOfFreedom=sum(tempVector,na.rm=TRUE)
		unbias=c4Fun(degOfFreedom+1)
		sdWithinX=sdPooled/unbias
	} else 	{
		movingRange=mrangeFun(x)
		rbar=sum(movingRange,na.rm=TRUE)/(nCompleteX-2+1) # 2=w=dimensioen sottogruppo, ossia intervallo moving range =1
		#use unbiasing constant d2(2)=1.128. Before 0.8865
		sdWithinX=rbar/getCoeffFun(2, "d2")
	}
} else {sdWithinX=historicalSd}


#estimation ppm
if(!is.null(lsl)){
	ppmLOv=1000000*pnorm(q=lsl,mean=meanX,sd=sdOverallX)
	ppmLPt=1000000*pnorm(q=lsl,mean=meanX,sd=sdWithinX)
	}
if(!is.null(usl)){
	ppmUOv=1000000*(1-pnorm(q=usl,mean=meanX,sd=sdOverallX))
	ppmUPt=1000000*(1-pnorm(q=usl,mean=meanX,sd=sdWithinX))
	}
#estimates ppm
ppmTOv=sum(c(ppmLOv,ppmUOv),na.rm=TRUE)
ppmTPt=sum(c(ppmLPt,ppmUPt),na.rm=TRUE)

#estimate capability maind indexes
if(!is.null(lsl))
{
#with cp
	ppl=(meanX-lsl)/((toler/2)*sdOverallX)
	cpl=(meanX-lsl)/((toler/2)*sdWithinX)
#with z
	zLslOv=(meanX-lsl)/(sdOverallX)
	zLslPt=(meanX-lsl)/(sdWithinX)
	p1Ov=1-pnorm(zLslOv)
	p1Pt=1-pnorm(zLslPt)
}
if(!is.null(usl))
{
	ppu=(usl-meanX)/((toler/2)*sdOverallX)
	cpu=(usl-meanX)/((toler/2)*sdWithinX)
#with z
	zUslOv=(usl-meanX)/(sdOverallX)
	zUslPt=(usl-meanX)/(sdWithinX)
	p2Ov=1-pnorm(zUslOv)
	p2Pt=1-pnorm(zUslPt)
}
#estimates cpk
ppk=min(c(ppl,ppu),na.rm=TRUE)
cpk=min(c(cpl,cpu),na.rm=TRUE)

#estimates cp and pp
if ((!is.null(lsl)) && (!is.null(usl)))
{
#cp
	pp=(usl-lsl)/(toler*sdOverallX)
	cp=(usl-lsl)/(toler*sdWithinX)
#z
	zBenchPt=qnorm(1-p1Pt-p2Pt)
	zBenchOv=qnorm(1-p1Ov-p2Ov)
}
#cpm analysis: there is olway by inly i normal
if(!is.null(target)){

	midpoint=(lsl+usl)/2
	#subcases
	#case n°1 target equal to  midpoint defined usl and lsl
	if ((target==midpoint) && (!is.null(usl) && !is.null(lsl)))
	{
		num=usl-lsl
		den=toler*(devFun(x=x,center=target)/(nCompleteX-1))^0.5
		cpm=num/den
	}
	#subcase
	#target different from and exists usl and lsl
	if ((target!=midpoint) && (!is.null(usl) && !is.null(lsl)))
	{
		num=min(target-lsl,usl-target)
		den=(toler/2)*(devFun(x=x,center=target)/(nCompleteX-1))^0.5
		cpm=num/den
	}
	#subcase
	#case n 3: you have only usl and lsl
	if (!is.null(usl) && is.null(lsl))
	{
		num=usl-target
		den=(toler/2)*(devFun(x=x,center=target)/(nCompleteX-1))^0.5
		cpm=num/den
	}
	#subcase
	#case four: you have only target and lsl
	if (is.null(usl) && !is.null(lsl))
	{
		num=target-lsl
		den=(toler/2)*(devFun(x=x,center=target)/(nCompleteX-1))^0.5
		cpm=num/den
	}
}


#copy information about pdf and df
summaryInfo$qfun=qdist
summaryInfo$dfun=ddist
summaryInfo$pfun=pdist

#binding sd

#binding cpm

#observed / general
	genStats$nTotalX=nTotalX
	genStats$nCompleteX=nCompleteX
	genStats$nMissingX=nMissingX
	genStats$nGroupsX=nGroupsX
	genStats$meanX=meanX
	genStats$sdOverallX=sdOverallX
	genStats$sdWithinX=sdWithinX
	genStats$estimate1=meanX
	genStats$estimate2=sdOverallX

	genStats$ppmLOss=ppmLOss
	genStats$ppmUOss=ppmUOss
	genStats$ppmTOss=ppmTOss
	genStats$percLOss=ppmLOss/10000
	genStats$percUOss=ppmUOss/10000
	genStats$percTOss=ppmTOss/10000
	genStats$cpm=cpm
#potential
	potentialStats=list()
	
	potentialStats$percLPt=ppmLPt/10000
	potentialStats$percUPt=ppmUPt/10000
	potentialStats$percTPt=ppmTPt/10000
	potentialStats$ppmLPt=ppmLPt
	potentialStats$ppmUPt=ppmUPt
	potentialStats$ppmTPt=ppmTPt
	
	potentialStats$cp=cp
	potentialStats$cpl=cpl
	potentialStats$cpu=cpu
	potentialStats$cpk=cpk
	potentialStats$zLslPt=zLslPt
	potentialStats$zUslPt=zUslPt
	potentialStats$zBenchPt=zBenchPt
#overall
	overallStats=list()

	overallStats$percLOv=ppmLOv/10000
	overallStats$percUOv=ppmUOv/10000
	overallStats$percTOv=ppmTOv/10000
	overallStats$ppmLOv=ppmLOv
	overallStats$ppmUOv=ppmUOv
	overallStats$ppmTOv=ppmTOv
	overallStats$pp=pp

	overallStats$ppl=ppl
	overallStats$ppu=ppu
	overallStats$ppk=ppk
	overallStats$zLslOv=zLslOv
	overallStats$zUslOv=zUslOv
	overallStats$zBenchOv=zBenchOv

capabilityObj=list()
capabilityObj$summaryInfo=summaryInfo
capabilityObj$genStats=genStats
capabilityObj$potentialStats=potentialStats
capabilityObj$overallStats=overallStats
capabilityObj$call=match.call()
class(capabilityObj) = "capability"
invisible(capabilityObj)
}
