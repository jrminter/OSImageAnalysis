#' Parse a GMRFilm PAP simulation for CuOx on Cu
#' 
#' This reads an output file (fPath) produced by GMRFilm
#' using writeInputCuOxCu containing O K-alpha and
#' Cu L-alpha K-ratios for a single thickness thickness and e0
#'
#' @param fPath File path to the K-Ratio file \code{fPath}
#'
#' @return ret A vector with the e0, tOx, krOKa, krCuLa
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### not run
#' # wrkDir <- "C:/Temp/"
#' # e0 = 5
#' # setwd(wrkDir)
#' # preClean(wrkDir)
#' # makeRunIt(wrkDir)
#' # inFil <- './in.txt'
#' # writeInputCuOxCu.R(50.0, 0.1386, 0.8614, 3.0, 5.0, inFil, toa=35)
#' # system("runIt", show.output.on.console=TRUE)
#' # kFil  <- getOutputFile()
#' # res <- parseCuOxOut(kFil)
#' # print(res)
#'

parseCuOxOut <- function(fPath){

  parse.kv <- function(the.line){
    kv <- as.numeric(substr(the.line, 17, 19))
    kv
  }
  
  parse.ok.ox <- function(the.line){
    ok <- as.numeric(substr(the.line, 59, 59+6))
    ok
  }

  parse.cul.ox <- function(the.line){
    cul <- as.numeric(substr(the.line, 59, 59+6))
    cul
  }
  parse.t.ox <- function(the.line){
    t <- as.numeric(substr(the.line, 41, 41+6))
    t
  }

  parse.cul.sub <- function(the.line){
    cul <- as.numeric(substr(the.line, 59, 59+6))
    cul
  }

  
  a <- readLines(fPath, n = -1)
  e0 <- parse.kv(a[6])
  ok.ox <- parse.ok.ox(a[22])
  cul.ox <- parse.cul.ox(a[23])
  t.ox <- parse.t.ox(a[24]) / 10.0 # in nm
  cul.sub <- parse.cul.sub(a[26])
  res <- c(e0, t.ox, ok.ox, cul.ox+cul.sub)
  names(res) <-c("e0", "tOx nm", "KR O Ka", "KR CuLa")
  
  return(res)
}
