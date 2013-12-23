#' Compute PAP K-Ratios for Pd/Cu using GMRFilm
#' 
#' Compute the PdLa and CuKa K-ratios using GMRFilm for a vector
#' of accelerating voltages for specified Pd and Cu thickness values. 
#' Note: this corrects for continuum fluorescence
#'
#' @param vkV A vector of kvs to simulate
#' @param tPd Pd thickness in nm
#' @param tCu Cu thickness in nm
#' @param toa take off angle for detector in deg
#' @param waitSec time to wait for OS to rename output file
#' @param wrkDir Working directory 
#' @param echo Boolean to show/hide GMRFilm console output
#' @param clean Boolean to delete input/output files
#'
#' @return df A data frame with the kVs and the Pd L-a and Cu K-a K-ratios 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#' # vkV <- 10:30
#' # df <- simPdCuSG(vkV, 8.8, 861., 35.0, 0.1, wrkDir='C:/Temp/', echo=TRUE, clean=FALSE)
#' # print(head(df))
#' 

simPdCuSG <- function(vkV, tPd, tCu, toa, waitSec, 
                    wrkDir='C:/Temp/',
                    echo=TRUE, clean=FALSE){
  wd <- getwd()
  setwd(wrkDir)
  preClean(wrkDir)
  makeRunIt(wrkDir)
  inFil <- './in.txt'
  writeInputPdCuSG(tPd, tCu, vkV, inFil, toa=toa) 
  system("runIt", show.output.on.console=echo)
  k.fil  <- getOutputFile()
  df <- parsePdCuOut(k.fil)
  if(clean){
    file.remove(inFil, k.fil)
  }
  setwd(wd)
  return (df)
}