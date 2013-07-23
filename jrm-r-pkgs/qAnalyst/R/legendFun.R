`legendFun` <-
function(capabilityObj)
{
if(capabilityObj$summaryInfo$distribution=="normal") 	textKey=c("potential", "overall") else 	textKey="overall"
if(capabilityObj$summaryInfo$distribution=="normal") linesColorKey=c("green", "blue") else  linesColorKey="blue"
if(capabilityObj$summaryInfo$distribution=="normal") linesLtyKey=c(1,5) else linesLtyKey=5
if(capabilityObj$summaryInfo$distribution=="normal") numColumns=2 else numColumns=1
#defines lines colors lty
if (!is.null(capabilityObj$summaryInfo$lsl)) {textKey=c(textKey,"LSL"); linesColorKey=c(linesColorKey, "dark red"); linesLtyKey=c(linesLtyKey,1); numColumns=numColumns+1 }
if (!is.null(capabilityObj$summaryInfo$usl)) {textKey=c(textKey,"USL"); linesColorKey=c(linesColorKey, "dark red"); linesLtyKey=c(linesLtyKey,1); numColumns=numColumns+1 }
if (!is.null(capabilityObj$summaryInfo$target)) {textKey=c(textKey,"TARGET"); linesColorKey=c(linesColorKey, "red"); linesLtyKey=c(linesLtyKey,5); numColumns=numColumns+1 }
legendOut=list()
legendOut$textKey=textKey
legendOut$linesColorKey=linesColorKey
legendOut$linesLtyKey=linesLtyKey
legendOut$numColumns=numColumns
return(legendOut)
}

