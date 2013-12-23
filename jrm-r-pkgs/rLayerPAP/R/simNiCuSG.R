#' Compute PAP K-Ratios for Ni/Cu using GMRFilm
#' 
#' Compute the NiKa and CuKa K-ratios using GMRFilm for a vector
#' of accelerating voltages for specified Ni and Cu thickness values. 
#' Note: this corrects for continuum fluorescence
#'
#' @param vkV A vector of kvs to simulate
#' @param tNi Ni thickness in nm
#' @param tCu Cu thickness in nm
#' @param toa take off angle for detector in deg
#' @param waitSec time to wait for OS to rename output file
#' @param wrkDir Working directory 
#' @param echo Boolean to show/hide GMRFilm console output
#' @param clean Boolean to delete input/output files
#'
#' @return df A data frame with the kVs and the Ni L-a and Cu K-a K-ratios 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#' # vkV <- 10:30
#' # df <- simNiCuSG(vkV, 8.8, 861., 35.0, 0.1, wrkDir='C:/Temp/', echo=TRUE, clean=FALSE)
#' # print(head(df))
#' 

simNiCuSG <- function(vkV, tNi, tCu, toa, waitSec, 
                    wrkDir='C:/Temp/',
                    echo=TRUE, clean=FALSE){
  wd <- getwd()
  setwd(wrkDir)
  preClean(wrkDir)
  makeRunIt(wrkDir)
  inFil <- './in.txt'
  writeInputNiCuSG(tNi, tCu, vkV, inFil, toa=toa) 
  system("runIt", show.output.on.console=echo)
  k.fil  <- getOutputFile()
  df <- parseNiCuOut(k.fil)
  if(clean){
    file.remove(inFil, k.fil)
  }
  setwd(wd)
  return (df)
}