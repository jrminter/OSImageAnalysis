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
#' @export
#' 
#' @examples
#' ### Not run
#' # make.gmrf.run.it()
make.gmrf.run.it <- function(wrkDir='C:/Temp/'){
  start.wd <- getwd()
  setwd(wrkDir)
  sink("./runIt.cmd")
  cat("@echo off\n")
  # get rid of any previous output files
  cat("DEL /S /Q /F F*.* \n")
  cat("C:\\Apps\\GMRFilm\\gmrfilm.exe < %1 \n")
  cat("MV F*.* out.txt\n")
  cat("DEL /S /Q /F standard.dat \n")
  cat("\n")
  sink()
}
# make.gmrf.run.it()