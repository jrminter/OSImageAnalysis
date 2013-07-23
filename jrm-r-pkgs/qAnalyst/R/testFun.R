`testFun` <- 
function(x, sg, type, xbarVariability, testType, k, p,  nSigma, mu = NA, sigma = NA) {

###########################################################
#verifies that test are between one and eight
if (!all(is.element(testType, 1:8))) {
  stop ("Error! Test must be between 1 and 8")
}

###########################################################
#uncheck down if all parameters must be specified. They are passed as c(NA) default. Lenght c(NA)==1
#if ((all(c(length(k)==1, length(p)==1, length(nSigma)==1))) && any(c(is.na(k), is.na(p), is.na(nSigma)))) stop("Error! Parameters must be specified")

howManyTests=length(testType)

#if more than one test and parameters unspecificed (one dimension vector NA)
#return length(testType) vector of parameters

if ((howManyTests>1) && all(c(length(nSigma), length(k), length(p)) == 1 )) {
	filler=rep(NA,howManyTests)
	#fills nSigma
	filler[1]=nSigma
	nSigma=filler
	#fills k
	filler[1]=k
	k=filler
	#fills p
	filler[1]=p
	p=filler
}

#checks parameters coherence
k = ifelse(is.na(k), 0, k)
p = ifelse(is.na(p), 0, p)

#if more than one tests, parameters shall be of same length
if (!all(c(length(nSigma), length(k), length(p)) == length(testType))) {
  stop("Error! testType, k, p and nSigma must be of same length")
}
############################################################
#Ordering
ord = order(testType, decreasing = TRUE)
testType = testType[ord]
k=k[ord]
p=p[ord]
nSigma=nSigma[ord]
############################################################
#Color Legend
col9="#40f907" #brilliant green (all ok)
col8="#3f8c27" #green dark
col7="#4b6111" #green olive
col6="#b8f11f" #green ugly
col5="#d2af23" #green yellow
col4="#fdd600" #yellow
col3="#f8650d" #orange
col2="#7b0303" #dark red
col1="#fa0909" #red (very wrong)
colorLegend= c(col1, col2, col3, col4,col5, col6, col7, col8, col9)
################################################################
#Mat of all passed tests ... initial state
points = pointsFun (x = x, sg = sg, type = type)
#initial matrix to archive results
matrixTest = matrix(0, ncol = length(testType), nrow = length(points))
############################################################
############################################################
############################################################

#Define internal function
.rollsumFun = function(x, range) {
  x <- unclass(x)
  x[is.na(x)] <- 0
  n <- length(x) 
  y <- x[range:n] - x[c(1, 1:(n-range))] # difference from previous
  y[1] <- sum(x[1:range])		 # find the first
  rval <- rep(0, n)
  rval[range:n] <- cumsum(y)
  return(rval)
}

.testFun = function(x, sg, testType, type , k, p, nSigma, points = points){

#############################################################
# procedure di inizializzazione generali
#############################################################
n = length(points)
center = centerFun (x = x, sg= sg, type = type, mu = mu, sigma = sigma) # (revision 0.6.1, Nicola)
center = rep(center, n)

# Default value for nSigma and definition of Zone A, Zone B, Zone C     # (revision 0.6.2, Nicola)
nSigma  = ifelse(is.na(nSigma), 3, nSigma)

upperA = clFun(x=x, sg=sg, nSigma = nSigma, cl="u", type = type, xbarVariability = xbarVariability, mu = mu, sigma = sigma)
lowerA = clFun(x=x, sg=sg, nSigma = nSigma, cl="l", type = type, xbarVariability = xbarVariability, mu = mu, sigma = sigma)
upperB = center + (2/3)*(upperA-center)
lowerB = center + (2/3)*(lowerA-center)
upperC = center + (1/3)*(upperA-center)
lowerC = center + (1/3)*(lowerA-center)

############################################################
# test 1
# At least k out of p points in a row beyond Zone A (outside the control limits)
# default values: k = p = 1, nSigma = 3
############################################################
if (testType == 1) {                # revision 0.6.2, Nicola
  # Default values
  k = ifelse(k == 0, 1, k)
  p = ifelse(p == 0, k, p)

  # Check parameters coherence
  if(p > n){stop("Error! p must be lower or equal than n")}
  if(p < k){stop("Error! p shall be not lower than k")}
  
  # Perform test
  onetest <- as.numeric(points < lowerA | points > upperA)
  ptest   <- .rollsumFun(x=onetest, range = p)
  out     <- as.numeric(ptest >= k)
}



############################################################
# test 2
# At least k out of p points in a row on one side of central line
# default values: k = p = 9
############################################################
if (testType == 2) {                # revision 0.6.2, Nicola
  # Default values
  k = ifelse(k == 0, 9, k)
  p = ifelse(p == 0, k, p)
  
  # Check parameters coherence
  if(p > n) {stop("Error! p must be lower or equal than n")}
  if(p < k) {stop("Error! p shall be not lower than k")}

  # Perform test
  # At least k out of p points in a row over central line
  onetestOver  <- as.numeric(points > center)
  ptestOver    <- .rollsumFun(x=onetestOver, range = p)
  outOver      <- as.numeric(ptestOver >= k)
  # At least k out of p points in a row under central line
  onetestUnder <- as.numeric(points < center)
  ptestUnder   <- .rollsumFun(x=onetestUnder, range = p)
  outUnder     <- as.numeric(ptestUnder >= k)
  # At least k out of points in a row on one side of central line
  out          <- outOver + outUnder

}



############################################################
# test 3
# At least k out of p points in a row all increasing or all decreasing
# default values: k = p = 6
############################################################
if (testType == 3) {                # revision 0.6.2, Nicola
  # Default values
  k = ifelse(k == 0, 6, k)
  p = ifelse(p == 0, k, p)
  
  # Check parameters coherence
  if(p > n){stop("Error! p must be lower or equal than n")}
  if(p < k){stop("Error! p shall be not lower than k")}
  
  # Perform test
  # At least k out of p points in a row all increasing
  onetestOver  <- as.numeric(points[1:n] > c(NA,points[1:(n-1)]))
  ptestOver    <- .rollsumFun(x=onetestOver, range = p)
  outOver      <- as.numeric(ptestOver >= k)
  # At least k out of p points in a row all decreasing
  onetestUnder <- as.numeric(points[1:n] < c(NA,points[1:(n-1)]))
  ptestUnder   <- .rollsumFun(x=onetestUnder, range = p)
  outUnder     <- as.numeric(ptestUnder >= k)
  # At least k out of p points in a row all increasing or all decreasing
  out          <- outOver + outUnder

}



############################################################
# test 4
# At least k out of p points in a row all up and down
# default values: k = p = 14
############################################################
if (testType == 4) {                # revision 0.6.2, Nicola
  # Default values
  k = ifelse(k == 0, 14, k)
  p = ifelse(p == 0, 14, p)
  
  # Check parameters coherence
  if(p < 5){stop("Error! p must be greater than 4")}
  if(p > n){stop("Error! p must be lower or equal than n")}
  if(p < k){stop("Error! p must be greater or equal to k")}

  # Perform test
  plusminus <- c(rep(c(1,-1),trunc((n-1)/2)),rep( 1,ceiling(((n-1)/2)-trunc((n-1)/2))))
  minusplus <- c(rep(c(-1,1),trunc((n-1)/2)),rep(-1,ceiling(((n-1)/2)-trunc((n-1)/2))))
  oneTestPM <- as.numeric(sign(diff(points))*plusminus == 1)
  oneTestMP <- as.numeric(sign(diff(points))*minusplus == 1)
  onetest   <- c(oneTestPM + oneTestMP)
  ptest     <- .rollsumFun(x=onetest, range = p)
  out       <- c(0,as.numeric(ptest >= k))
  
}



############################################################
# test 5
# At least k out of p points in a row in Zone A or beyond (> (2/3)*nSigma*sigma from central line; same side of central line)
# default values: k = 2, p = 3, nSigma = 3
############################################################
if (testType == 5) {                # revision 0.6.2, Nicola
  # Default values
  k = ifelse(k == 0, 2, k)
  p = ifelse(p == 0, k+1, p)

  # Check parameters coherence
  if(p > n){stop("Error! p must be lower or equal than n")}
  if(p < k){stop("Error! p shall be not lower than k")}
 
  # Perform test
  # At least k out of p points in a row in Zone A or beyond (over central line)
  onetestOver  <- as.numeric(points > upperB)
  ptestOver    <- .rollsumFun(x=onetestOver, range = p)
  outOver      <- as.numeric(ptestOver >= k)
  # At least k out of p points in a row in Zone A or beyond (under central line)
  onetestUnder <- as.numeric(points < lowerB)
  ptestUnder   <- .rollsumFun(x=onetestUnder, range = p)
  outUnder     <- as.numeric(ptestUnder >= k)
  # At least k out of p points in a row in Zone A or beyond (same side of the central line)
  out          <- outOver + outUnder

}



############################################################
# test 6
# At least k out of p points in a row in Zone B or beyond (> (1/3)*nSigma*sigma from central line; on one side of central line)
# default values: k = 4, p = 5, nSigma = 3
############################################################
if (testType == 6) {                # revision 0.6.2, Nicola
  # Default values
  k = ifelse(k == 0, 2, k)
  p = ifelse(p == 0, k+1, p)

  # Check parameter coherence
  if(p > n){stop("Error! p must be lower or equal than n")}
  if(p < k){stop("Error! p shall be not lower than k")}
  
  # Perform test
  # At least k out of p points in a row in Zone B or beyond (over central line)
  onetestOver  <- as.numeric(points > upperC)
  ptestOver    <- .rollsumFun(x=onetestOver, range = p)
  outOver      <- as.numeric(ptestOver >= k)
  # At least k out of p points in a row in Zone B or beyond (under central line)
  onetestUnder <- as.numeric(points < lowerC)
  ptestUnder   <- .rollsumFun(x=onetestUnder, range = p)
  outUnder     <- as.numeric(ptestUnder >= k)
  # At least k out of p points in a row in Zone B or beyond (same side of the central line)
  out          <- outOver + outUnder
  
}



############################################################
# test 7
# At least k out of p points in a row in Zone C (both sides of central line)
# default values: p = k = 15, nSigma = 3
############################################################
if (testType==7) {
  # Default values
  k = ifelse(k == 0, 15, k)
  p = ifelse(p == 0, k, p)

  # Check parameters coherence
  if(p > n){stop("Error! p must be lower or equal than n")}
  if(p < k){stop("Error! p shall be not lower than k")}

  # Perform test
  onetest <- as.numeric(points < upperC & points > lowerC)
  ptest   <- .rollsumFun(x=onetest, range = p)
  out     <- as.numeric(ptest >= k)

}



############################################################
# test 8
# At least k out of p points in a row with no one in Zone C
# default values: p = k = 8, nSigma = 3
############################################################
if (testType==8) {
  # Default values
  k = ifelse(k == 0, 8, k)
  p = ifelse(p == 0, k, p)
  
  # Check parameters coherence
  if(p > n){stop("Error! p must be lower or equal than n")}
  if(p < k){stop("Error! p shall be not lower than k")}
  
  # Perform test
  onetest <- as.numeric(points < lowerC | points > upperC)
  ptest   <- .rollsumFun(x=onetest, range = p)
  out     <- as.numeric(ptest >= k)

}



############################################################
#where NA 0
out=ifelse(is.na(out),0,out)
invisible(out)
}
############################################################
#End Define internal function
############################################################
############################################################
############################################################

#execute each of defined test in testType and saves results  in tcolumns of matrixTest
for (i in 1:length(testType)){
matrixTest[,i] = .testFun(x, type = type, testType = testType[i], k=k[i], p=p[i] , sg = sg, nSigma=nSigma[i], points = points)
}
#coluns naming
dimnames(matrixTest) = list(NULL, paste("Test", testType, sep = ""))
#creates a matrix with each rows containigns test codes
colMat = matrix(testType, ncol = length(testType), nrow = length(points), byrow = TRUE)
colMat = matrixTest*colMat
colMat[colMat == 0] = 9
#where a test does not fail code equal 9
colVec = apply(colMat, 1, min)
#the color index of colorLegend is defined as minimum color for each rows in mtatrixTest
color = character(length(points))
for ( i in 1:length(points)){
color[i] = colorLegend[colVec[i]]
}

#creates response matrix
matrixTest = cbind(index = 1:length(points), matrixTest)[apply(matrixTest, 1, max) > 0,]
#list(color, matrixTest)
responseList=list(colorSet=color,testMatrix=matrixTest)
return(responseList)
}






