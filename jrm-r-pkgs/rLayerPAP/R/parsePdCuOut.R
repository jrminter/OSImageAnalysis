#' Parse a GMRFilm PAP simulation for Pd on Cu on PET
#' 
#' This reads an output file (fPath) produced by GMRFilm
#' using writeInputPdCuSG containing Pd L-alpha and
#' Cu K-alpha K-ratios for specified values of Pd and Cu thickness
#' and a vector of accelerating voltages and returns a data frame
#' with the values.
#' 
#' These are input to optimization routines.
#'
#' @param fPath File path to the K-Ratio file
#'
#' @return df A data frame with the e0, krPdLa, krCuKa
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### not run
#' # wrkDir <- "C:/Temp/"
#' # vkV <- 10:30
#' # setwd(wrkDir)
#' # preClean(wrkDir)
#' # makeRunIt(wrkDir)
#' # inFil <- './in.txt'
#' # writeInputPdCuSG(200, 400, vkV, inFil) 
#' # system("runIt", show.output.on.console=TRUE)
#' # kFil  <- getOutputFile()
#' # df <- parsePdCuOut(kFil)
#' # print(df)
#'

parsePdCuOut <- function(fPath){
  # create empty vectors to store the results  
  v.kV <- vector(mode = "numeric", length = 0)
  v.kPdLa <- vector(mode = "numeric", length = 0)
  v.kCuKa <- vector(mode = "numeric", length = 0)
  
  parse.kv <- function(the.line){
    kv <- as.numeric(substr(the.line, 17, 19))
    kv
  }
  
  parse.layer <- function(the.line){
    elem <- substr(the.line, 12, 13)
    names(elem) <- 'elem'
    kr     <- as.numeric(substr(the.line,59,65))
    f.char <- as.numeric(substr(the.line,67,72))
    f.cont <- as.numeric(substr(the.line,74,78))
    nr     <- c( kr, f.char, f.cont)
    names(nr) <- c('K-Ratio', 'F-Char', 'F-cont')
    ret <- list(elem, nr)
    ret
  }
  
  a <- readLines(fPath, n = -1)
  n.kv <- length(a)/26
  for (j in 1:n.kv){
    off <- (j-1)*26+6
    kV <- parse.kv(a[off])
    v.kV <- append(v.kV, kV)
     
    off <- (j-1)*26+17
    vals <- parse.layer(a[off])
    ni <- vals[[2]][1]
    v.kPdLa <- append(v.kPdLa, ni)
    
    off <- (j-1)*26+20
    vals <- parse.layer(a[off])
    cu <- vals[[2]][1]
    v.kCuKa <- append(v.kCuKa, cu)
  }
  res <- data.frame(kV=v.kV, kPdLa=v.kPdLa, kCuKa=v.kCuKa)
  return(res)
}
