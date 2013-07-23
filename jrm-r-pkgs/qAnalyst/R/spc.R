`spc` <-
function (x, sg = NULL, type = "xbar", xbarVariability = "auto", name = deparse(substitute(x)), 
    testType = 1, k = NA, p = NA, nSigma = 3, mu = NA, sigma = NA) {

    type = switchFun(argument = type, type = "chart")
    if (!is.element(type, c("xbar", "s", "r", "i", "mr", "p", "np", "c", "u"))) {
        stop("Error! Unrecognized chart")
    }
    if (!is.element(xbarVariability, c("auto", "r", "s"))) {
        stop("Error! Unrecognized variability type for xbar chart")
    }
    if ((is.null(sg)) && (!type == "c"))  {
        stop("Error! sg is always required with the exception of c charts")
    }
    if (!is.numeric(x)) {
        stop("Error! x is not numeric")
    }
    if (is.element(type, c("i", "mr"))) {
        sg = sg - 1
        if (sg < 1) 
            stop("Error! width of the moving range window must be at least equal to 2")
    }
    
    sg = sgFun(x = x, sg = sg, type = type)
    
    if (is.element(type, c("xbar", "s", "r"))) {
        sgSize = as.numeric(tapply(x, sg, countFun))
        # At least one subgroup with only an observation
        sgSizeTest = ifelse(sgSize > 1, 1, 0)
        if (sum(sgSizeTest) < length(sgSizeTest)) {
            warning("At least one subgroup with dimension lower than 2 in a variable chart for subgroups", 
                call. = FALSE, immediate. = TRUE)
        }
        # Different sample size (chart Xbar) (release 0.6.2, Nicola)
        if(((max(sgSize)-min(sgSize)) >= 1) && (type == "xbar") && (xbarVariability == "r")) {
            warning("Variable sample size. Each sample has a different number of observations. It is suggested the use of \"s\" (or \"auto\") for xbarVariability", 
                call. = FALSE, immediate. = TRUE)
        }
        # Different sample size (chart R) (release 0.6.1, Nicola)
        if(((max(sgSize)-min(sgSize)) >= 1) && (type == "r")) {
            warning("Variable sample size. Each sample has a different number of observations. R chart may be difficult to interpret: S chart would be preferable.", 
                call. = FALSE, immediate. = TRUE)
        }
    }
    
    # if name is too long substitute create two vectors and plot will work in an unpredictable mode (release 0.6.2, Enrico e Nicola)
    if(length(name) > 1) {
      name <- paste(name, collapse="")
    }
    
    # xbar and i charts: mu and sigma must be both provided (release 0.6.1, Nicola)
    if((is.element(type,c("xbar","i"))) & (((!is.na(mu) && is.na(sigma))) || (is.na(mu) && !is.na(sigma)))) {
        stop("mu and sigma must be both (or neither) provided")
    }

    # s and r charts: only sigma should be provided (release 0.6.1, Nicola)
    if((is.element(type,c("s", "r", "mr"))) & (!is.na(mu))) {
        warning(paste("only sigma should be provided in the",type,"chart: mu ignored"), call. = FALSE, immediate. = TRUE)
    }
    
    # s, r, mr, p, np, c and u charts: only mu should be provided (release 0.6.1, Nicola)
    if((is.element(type,c("p", "np", "c", "u"))) & (!is.na(sigma))) {
        warning(paste("only mu should be provided in the",type,"chart: sigma ignored"), call. = FALSE, immediate. = TRUE)
    }

    # sigma must be positive  (release 0.6.1, Nicola)
    if(!is.na(sigma) && sigma <= 0) {
        stop("sigma must be positive")
    }

  
    xName = name
    points = pointsFun(x = x, sg = sg, type = type)
    i = iFun(points)
    
    # Compute center line
    center = centerFun(x = x, sg = sg, type = type, mu = mu, sigma = sigma)
    if(length(center)==1) {
        center = rep(center, length(points))
    }
    center[is.na(points)] <- NA  # center line is NA when the point is NA
    
    nSigmaForTests = rep(nSigma, length(testType)) # Modifica della chiamata alla procedura per permettere generazione corretta delle carte con nSigma non standard (3). release 0.5.4 Pgo *****
    
    ucl3 = clFun(x = x, sg = sg, nSigma = nSigma, cl = "u", type = type, xbarVariability = xbarVariability, mu = mu, sigma = sigma)
    if(length(ucl3)==1) {ucl3 <- rep(ucl3, length(points))}
    ucl3[is.na(points)] <- NA # if point is NA then confidence limit is also NA
    lcl3 = clFun(x = x, sg = sg, nSigma = nSigma, cl = "l", type = type, xbarVariability = xbarVariability, mu = mu, sigma = sigma)
    if(length(lcl3)==1) {lcl3 <- rep(lcl3, length(points))}
    lcl3[is.na(points)] <- NA # if point is NA then confidence limit is also NA
    
    ucl2 = center + (2/3)*(ucl3-center)
    ucl2[is.na(points)] <- NA # if point is NA then confidence limit is also NA
    lcl2 = center - (2/3)*(center-lcl3)
    lcl2[is.na(points)] <- NA # if point is NA then confidence limit is also NA
    ucl1 = center + (1/3)*(ucl3-center)
    ucl1[is.na(points)] <- NA # if point is NA then confidence limit is also NA
    lcl1 = center - (1/3)*(center-lcl3)
    lcl1[is.na(points)] <- NA # if point is NA then confidence limit is also NA
    
    # Limits for plot
    iForLimits = iLimitsFun(i)
    ucl3ForLimits = xLimitsFun(ucl3)
    lcl3ForLimits = xLimitsFun(lcl3)
    
    if (is.null(testType)) {
        resultsOfTest = list()
        resultsOfTest$colorSet = "#40f907"
        resultsOfTest$testMatrix = NULL
    } else {
        resultsOfTest = testFun(x = x, sg = sg, type = type, testType = testType, xbarVariability = xbarVariability, nSigma = nSigma, k = k, p = p, mu = mu, sigma = sigma)
    }
    ylim = limitsFun(list(points[!is.na(points)], ucl3[ucl3<Inf], lcl3[lcl3>-Inf]))
    ylab = ylabFun(xName, type = type)
    xlab = ifelse(is.element(type, c("i", "mr")), "index", "subgroups")
    statisticsList = statsSpcFun(x = x, sg = sg, type = type)

    # Probabilita' di avere il numero di fuori controllo uguale o maggiore/uguale al numero effettivamente trovato (0.5.4. PGO)
    if(c(testType %in% c(1))) {
        probSingleFailure=unique(pnorm(-nSigmaForTests[testType==1])*2) # Calcolo forzatamente approssimato: le carte di controllo approssimano la distribuzione con una gaussiana. Facciamo lo stesso anche noi
        if(is.vector(resultsOfTest$testMatrix)) { # Se c'e' solo un punto fuori controllo la matrice testMatrix diventa un vettore
            numTest1Fail=sum(resultsOfTest$testMatrix["Test1"])
        }
        else {
            numTest1Fail=sum(resultsOfTest$testMatrix[,"Test1"])
        }
        probLessEqualPoints=pbinom(q=numTest1Fail,size=statisticsList$nGroupsX,prob=probSingleFailure)
        probEqualPoints=pbinom(q=numTest1Fail,size=statisticsList$nGroupsX,prob=probSingleFailure)-ifelse(numTest1Fail==0,0,pbinom(q=numTest1Fail-1,size=statisticsList$nGroupsX,prob=probSingleFailure))
        probGreatEqualPoints=1-probLessEqualPoints+probEqualPoints
    }
    else {
        probLessEqualPoints=NA
        probEqualPoints=NA
        probGreatEqualPoints=NA
    }
    # Fine probabilita' 

    general = list()
    general$chartType = type
    general$xName = xName
    general$numTot = statisticsList$numTot
    general$numNNmissing = statisticsList$numNNmissing
    general$numMissing = statisticsList$numMissing
    general$nGroupsX = statisticsList$nGroupsX
    general$meanX = statisticsList$meanX
    general$minX = statisticsList$minX
    general$maxX = statisticsList$maxX
    general$sdTotX = statisticsList$sdTotX
    general$sdWithinX = statisticsList$sdWithinX
    general$sdBetweenX = statisticsList$sdBetweenX
    general$meanRangeX = statisticsList$meanRangeX
    general$testType = testType
    general$nSigma = nSigmaForTests

    graphPars = list()
    graphPars$xlab = xlab
    graphPars$ylab = ylab
    graphPars$points = as.numeric(points)
    graphPars$i = i
    graphPars$center = center
    graphPars$ylim = ylim
    graphPars$ucl3 = ucl3
    graphPars$lcl3 = lcl3
    graphPars$ucl2 = ucl2
    graphPars$lcl2 = lcl2
    graphPars$ucl1 = ucl1
    graphPars$lcl1 = lcl1
    graphPars$iForLimits = iForLimits
    graphPars$ucl3ForLimits = ucl3ForLimits
    graphPars$lcl3ForLimits = lcl3ForLimits
    graphPars$colors = resultsOfTest$colorSet

    testResults = list()
    testResults$testOutput = resultsOfTest$testMatrix
    testResults$probPointsEqualTest1 = probEqualPoints
    testResults$probPointsGreaterEqualTest1 = probGreatEqualPoints

    spcObj = list(general = general, graphPars = graphPars, testResults = testResults, 
        call = match.call())
    class(spcObj) = "spc"
    invisible(spcObj)
}
