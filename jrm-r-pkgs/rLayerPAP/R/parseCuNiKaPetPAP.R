#' Parse a GMRFilm PAP simulation for Cu on Ni on PET
#' 
#' This reads in a vector of the acellerating voltages simulated
#' and the the file containing the K-ratios for Ni K-alpha and
#' Cu K-alpha lines and returns a data frame with the values. 
#' These are input to optimization routines.
#'
#' @param v.kv A vector with the simuted acellerationg voltages \code{v.kv}
#' @param kr.file.path file path to the K-Ratio file \code{kr.file.path}
#'
#' @return df A data frame with the e0, krNiKa, krCuKa
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' R code here showing how your function works

parseCuNiKaPetPAP <- function(v.kv, kr.file.path){
  # create a data.frame to store the results
  n.kv <- length(v.kv)
  res <- as.data.frame(matrix(data = 0.0, nrow = n.kv, ncol = 3, byrow = FALSE, dimnames = NULL))
  names(res) <- c('kV', 'kNiKa', 'kCuKa')
  res[,1] <- v.kv
  
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
  
  a <- readLines(kr.file.path, n = -1)
  for (j in 1:n.kv){
    off <- (j-1)*26+6
    kv <- parse.kv(a[off])
    res[j,1] <- kv
    
    off <- (j-1)*26+17
    vals <- parse.layer(a[off])
    ni <- vals[[2]][1]
    res[j,2] <- ni
    
    off <- (j-1)*26+20
    vals <- parse.layer(a[off])
    cu <- vals[[2]][1]
    res[j,3] <- cu
  }
  return(res)
}