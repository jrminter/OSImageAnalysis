plot.transformation<-function(x,...)
{
#graph settings
textCex=2
stripCex=2
stripDim=2
scalesCex=2
lineLwd=2
stripDim=2
options(warn=-1)
transfObj=x
#plot original data
dataPlot=transfObj$original
trellis.par.set('layout.heights', list (strip = stripDim))
originalHist=histogram(~dataPlot|"original distribution",
xlab=list("x variable", cex=textCex),
ylab=list("density", cex=textCex),
scales=list(cex=scalesCex),
type="density",
strip = strip.custom(par.strip.text = list(cex = stripCex, col = "blue")),
panel=function(x,y,...){
panel.histogram(x,col="orange",...)
panel.mathdensity(dmath = dnorm, args = list(mean=mean(dataPlot), sd=sd(dataPlot)),
                  n = 50, col="red", lwd=2,...)}
)
#plot transformed data
dataPlot2=transfObj$transformed
transformation=transfObj$type
trellis.par.set('layout.heights', list (strip = stripDim))
transformedHist=histogram(~dataPlot2|paste(transformation,"transformed distribution",sep=" "),
xlab=list("x variable", cex=textCex),
ylab=list("density", cex=textCex),
scales=list(cex=scalesCex),
type="density",
strip = strip.custom(par.strip.text = list(cex = stripCex, col = "blue")),
panel=function(x,y,...){
panel.histogram(x,col="orange",...)
panel.mathdensity(dmath = dnorm, args = list(mean=mean(dataPlot2), sd=sd(dataPlot2)),
                  n = 50, col="red", lwd=2,...)}
)
#binds plots together
print(originalHist, position=c(0,0,.50,1), more=TRUE)
print(transformedHist, position=c(.50,0,1,1), more=TRUE)
options(warn=1)
}
