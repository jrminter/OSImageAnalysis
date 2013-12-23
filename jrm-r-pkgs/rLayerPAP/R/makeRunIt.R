#' Make a run-it cmd file for GMRFilm
#' 
#' Compute the NiKa and CuKa K-ratios using GMRFilm for a vector
#' of accelerating voltages for specified Ni and Cu thickness values. 
#' Note: this corrects for continuum fluorescence
#'
#' @param wrkDir Working directory for GMRFilm simulation \code{wrkDir}
#'
#' @return none
#'
#' @keywords keywords
#' 
#' @examples
#' ### Not run
#' # makeRunIt()

makeRunIt <- function(wrkDir='C:/Temp/'){
  setwd(wrkDir)
  sink("./runIt.cmd")
  cat("@echo off\n")
  cat("C:\\Apps\\GMRFilm\\gmrfilm.exe < in.txt \n")
  cat("\n")
  sink()
}
