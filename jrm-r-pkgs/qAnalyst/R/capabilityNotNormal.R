`capabilityNotNormal` <-
function(x,lsl=NULL,usl=NULL,target=NULL, distribution, name=deparse(substitute(x)), toler=6, histPars=c(NA,NA))
{

#coherence testing
if (is.null(lsl) && is.null(usl)) stop("Error! Capability analysis requires at least a specification limit")
if (!(toler>0)) stop("Error! tolerance constant must be positive")
#checks usl > lsl
if ((!(is.null(lsl))) && (!(is.null(usl)))) { if (!(usl>lsl)) stop("Error! usl shall be greather than lsl") }

capabilityObj=list()

#general info
summaryInfo=list()
summaryInfo$name=name
summaryInfo$lsl=ifelse(is.null(lsl),NA,lsl)
summaryInfo$usl=ifelse(is.null(usl),NA,usl)
summaryInfo$target=ifelse(is.null(target),NA,target)
#as is a normal capability
summaryInfo$distribution=distribution
summaryInfo$x=x

#general statistics
genStats=list()

#parameter settings and estimation
fitPars=fitdistr(x,distribution)
genStats$estimate1=ifelse(is.na(histPars[1]),fitPars$estimate[1],histPars[1])
genStats$estimate2=ifelse(is.na(histPars[2]),fitPars$estimate[2],histPars[2])

#limits setting
pl=pnorm(-toler/2,mean=0,sd=1)
pu=pnorm(toler/2,mean=0,sd=1)
pc=0.5
#distribution setting
qdist=paste("q",distribution,sep="")
pdist=paste("p",distribution,sep="")

nTotalX=length(x)
nCompleteX=length(na.omit(x))
nMissingX=nTotalX-nCompleteX
#groups not needed
nGroupsX=NA
meanX=mean(x,na.rm=TRUE)
sdOverallX=sd(x,na.rm=TRUE)

#ppm overall calculations
ppmLOss=NA
ppmUOss=NA
if (!is.null(lsl)) ppmLOss=1000000*(length(x[x<lsl]))/nCompleteX
if (!is.null(usl)) ppmUOss=1000000*(length(x[x>usl]))/nCompleteX
ppmTOss=sum(c(ppmLOss,ppmUOss), na.rm=TRUE)
#setted down

#setting parameters as defaul
cpm=NA; cp=NA; pp=NA
ppmLOv=NA; ppmUOv=NA;  percLOv=NA; percUOv=NA
ppmLPt=NA; ppmUPt=NA;  percPt=NA; percUPt=NA
ppmTOv=NA; ppmTPt=NA;  percTOv=NA; percTPt=NA
cpu=NA; ppu=NA; cpl=NA; ppl=NA; cpk=NA

zLslPt=NA;zUslPt=NA;zBenchPt=NA
zLslOv=NA;zUslOv=NA;zBenchOv=NA
p1Ov=NA; p2Ov=NA
#estimate within sdt
#as we're not in normal calse
#no need to estimate

sdWithinX=NA

#informations about distribution
infoFun=funInfoFun(x,distribution)

#setting specific distribution parameters
pdist=infoFun$pfun
qdist=infoFun$qfun
ddist=infoFun$dfun

#estimation ppm e ppl
if(!is.null(lsl)){
	p1Ov=do.call(pdist,list(q=lsl,as.numeric(fitPars$estimate[1]),as.numeric(fitPars$estimate[2])))
	ppmLOv=1000000*p1Ov
	ppl=(do.call(qdist,list(p=0.5,as.numeric(fitPars$estimate[1]), as.numeric(fitPars$estimate[2])))-lsl)/(diff(do.call(qdist,list(p=c(pl,0.5),as.numeric(fitPars$estimate[1]), as.numeric(fitPars$estimate[2])))))
	zLslOv=(toler/2)*ppl
	}

if(!is.null(usl)){
	p2Ov=(1-do.call(pdist,list(q=usl,as.numeric(fitPars$estimate[1]),as.numeric(fitPars$estimate[2]))))
	ppmUOv=1000000*p2Ov
	ppu=(usl-do.call(qdist,list(p=0.5,as.numeric(fitPars$estimate[1]), as.numeric(fitPars$estimate[2]))))/(diff(do.call(qdist,list(p=c(0.5,pu),as.numeric(fitPars$estimate[1]), as.numeric(fitPars$estimate[2])))))
	zUslOv=(toler/2)*ppu
	}

ppk=min(c(ppl,ppu),na.rm=TRUE)
ppmTOv=sum(c(ppmLOv,ppmUOv),na.rm=TRUE)



ppk=min(c(ppl,ppu),na.rm=TRUE)

#estimates cp and pp
if ((!is.null(lsl)) && (!is.null(usl)))
{
	pp=(usl-lsl)/(diff(do.call(qdist,list(p=c(pl,pu),as.numeric(fitPars$estimate[1]), as.numeric(fitPars$estimate[2])))))
	zBenchOv=qnorm(1-p1Ov-p2Ov)
}


#copy information about pdf and df
summaryInfo$qfun=qdist
summaryInfo$dfun=ddist
summaryInfo$pfun=pdist

#binding sd

#binding cpm

#observed / generaò
	genStats$nTotalX=nTotalX
	genStats$nCompleteX=nCompleteX
	genStats$nMissingX=nMissingX
	genStats$nGroupsX=nGroupsX
	genStats$meanX=meanX
	genStats$sdOverallX=sdOverallX
	genStats$sdWithinX=sdWithinX

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
