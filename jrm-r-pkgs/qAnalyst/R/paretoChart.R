paretoChart=function (x, mergeThr=.90, addLine=TRUE, abbrev=FALSE)
 {
 ##############prepare table to plot
if ((mergeThr>1) || (mergeThr<0)) stop("Error! Merge threshold should be between 0 and 1")
options(warn=-1)
 name=deparse(substitute(x))
#converts in a charatcet
 x=as.character(x)
 x<-x[!is.na(x)]
 howMany=length(unique(x))
 x <- table(x)
 #increasing sort and remove na
 x <- sort(x)
 total=sum(x)
 #decreasing sort
 x <- rev(x)
 #create cusum
 cumulate <- cumsum(x)
	#determine after which cumulated frequency categories shall be aggregated
 threshold=mergeThr*total
#creates a temporany dataframe
 xFrame=as.data.frame(x)
 categories=rownames(xFrame)
 frequencies=as.numeric(x)
 #cumulate +
 aggregateYN=integer(howMany)
#determine which cartegories aggregate
 for (i in 2:howMany)
 {
	 if(cumulate[i-1]>threshold) aggregateYN[i]=TRUE
 }
 tempFrame=data.frame(categories=categories, frequencies=as.numeric(frequencies), cumulated=as.numeric(cumulate), aggregateYN=as.numeric(aggregateYN), stringsAsFactors=FALSE)
#remove aggregation flag from temporany dataFrame
 tempFrame=tempFrame[tempFrame$aggregateYN==0,-4]
 rownames(tempFrame)=NULL
 #cateogies not aggregable
 nRows=dim(tempFrame)[1]

 if(tempFrame[nRows,3]<total) {tempFrame=rbind(tempFrame, newInfo=data.frame(categories="Others", frequencies=total-(tempFrame[nRows,3]), cumulated=total))}
#add a flag field from 1 to howMany
howMany=dim(tempFrame)[1]
uniqueID=1:howMany
tempFrame=cbind(tempFrame, uniqueID)
rownames(tempFrame)=NULL 
#graphics setting
titleName=paste("Pareto chart of ",name,sep=" ")
xlab=name
ylim <- max(c(0,tempFrame$cumulated)) * 1.05
textCex=2
stripCex=2
stripDim=2
scalesCex=2
lineLwd=2
stripDim=2


trellis.par.set('layout.heights', list (strip = stripDim))
barchart(frequencies~uniqueID|titleName,data=tempFrame,horizontal=FALSE,
	scales=list(cex=scalesCex,x=list(labels=tempFrame$categories, abbreviate=abbrev)),
	strip = strip.custom(par.strip.text = list(cex = stripCex, col = "blue")),
	ylab=list("frequencies",cex=textCex),
	xlab=list("categories",cex=textCex), 
	ylim=c(0,ylim),
	panel = function(x, y, ...){
	panel.barchart(x, y, col="orange",...)
	if (addLine==TRUE) panel.xyplot(x=x,y=tempFrame$cumulated,type="b",col="red", lwd=lineLwd,...)
	}
)

}
