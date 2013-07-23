`summary.spc` <-
function (object, ...) 
{
    spcObj = object
    titleObj = paste(spcObj$general$chartType, " chart of ", 
        spcObj$general$xName, sep = "")
    cat("\n", titleObj, "\n")
    cat("\n", spcObj$general$xName, " main stats", "\n", "------------------------------------------", 
        "\n")
    namesGenStats = c("Total observations", "complete observations", 
        "missing observations", "number of groups", "Mean", "min", 
        "max", "total std. dev.", "average range")
    genStats = c(spcObj$general$numTot, spcObj$general$numNNmissing, 
        spcObj$general$numMissing, spcObj$general$nGroupsX, spcObj$general$meanX, 
        spcObj$general$minX, spcObj$general$maxX, spcObj$general$sdTotX, 
        spcObj$general$meanRangeX)
    genStats = as.matrix(genStats)
    colnames(genStats) = c("value")
    rownames(genStats) = c(namesGenStats)
    format(genStats, digits = 5, scientific = FALSE)
    print(genStats)
    cat("\n", "Control chart tests results", "\n", "------------------------------------------", 
        "\n")
    if (!is.null(spcObj$testResults$testOutput)) {
        cat("\n", "Matrix of points failing required tests", 
            "\n")
        if (class(spcObj$testResults$testOutput) == "numeric") 
            print(spcObj$testResults$testOutput)
        else {
            if (dim(spcObj$testResults$testOutput)[1] == 0) 
                cat("\n", "All tests successful", "\n")
            else print(spcObj$testResults$testOutput)
        }
        cat("\n", "Probability of having such a number of Test1 failing points:\n")
        cat(spcObj$testResults$probPointsEqual,"\n")
        cat("\n", "Probability of having a number of Test1 failing points greater or equal to:\n")
        cat(spcObj$testResults$probPointsGreaterEqual,"\n")
    }
    else {
        cat("No tests have been required on analyzed data set", 
            "\n")
    }
    cat("\n", "Control chart elements table", "\n", "------------------------------------------", 
        "\n")

    # If there is an unique center value (same number of observations for each subgroup) then repeat it for every points.
    if(length(spcObj$graphPars$center)==1) {
        centro = rep(spcObj$graphPars$center, spcObj$general$nGroupsX)
    } else {
        centro = spcObj$graphPars$center
    }

    punti = as.vector(spcObj$graphPars$points)
    lcl3s = as.vector(spcObj$graphPars$lcl3)
    lcl2s = as.vector(spcObj$graphPars$lcl2)
    lcl1s = as.vector(spcObj$graphPars$lcl1)
    ucl1s = as.vector(spcObj$graphPars$ucl1)
    ucl2s = as.vector(spcObj$graphPars$ucl2)
    ucl3s = as.vector(spcObj$graphPars$ucl3)
    dfTableCarta = cbind(punti, lcl3s, lcl2s, lcl1s, centro, 
        ucl1s, ucl2s, ucl3s)
    dfTableCarta = as.data.frame(dfTableCarta)
    names(dfTableCarta) = c("points", "lcl3s", "lcl2s", "lcl1s", 
        "center line", "ucl1s", "ucl2s", "ucl3s")
    print(dfTableCarta, digits = 5)
    invisible(NULL)
}
