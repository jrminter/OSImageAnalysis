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
#' @param wrkDir Working directory
#' @param clean Boolean to delete input/output files
#'
#' @return df A data frame with the kVs and the Ni and Cu K-a K-ratios 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#'

simNiCuSG <- function(vkV, tNi, tCu, toa,
                      wrkDir='C:/Temp/',
                      clean=FALSE){
  start.wd <- getwd()
  setwd(wrkDir)
  preClean(wrkDir)
  makeRunIt(wrkDir)
  inFil <- './in.txt'
  writeInputNiCuSG(tNi, tCu, vkV, inFil, toa=toa) 
  system("runIt", show.output.on.console=FALSE)
  moveIt(wrkDir='C:/Temp/')
  k.fil  <- "./out.txt"
  df <- parseNiCuOut(k.fil)
  # print(df)
  if(clean){
    file.remove(inFil, k.fil)
  }
  setwd(start.wd)
  return (df)
}