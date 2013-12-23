#' Compute PAP K-Ratios for Pd/Cu using GMRFilm
#' 
#' Compute the PdKa and CuKa K-ratios using GMRFilm for a vector
#' of accelerating voltages for specified Pd and Cu thickness values. 
#' Note: this corrects for continuum fluorescence
#'
#' @param vkV A vector of kvs to simulate
#' @param tPd Pd thickness in nm
#' @param tCu Cu thickness in nm
#' @param toa take off angle for detector in deg
#' @param wrkDir Working directory 
#' @param clean Boolean to delete input/output files
#'
#' @return df A data frame with the kVs and the Pd and Cu K-a K-ratios 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#' # vkV <- 10:30
#' # print(vkV)
#' # df <- simPdCuSG(vkV, 8.8, 861., 35.0, wrkDir='C:/Temp/', clean=FALSE)
#' # print(head(df))
#' 

simPdCuSG <- function(vkV, tPd, tCu, toa,
                    wrkDir='C:/Temp/',
                    clean=FALSE){
  wd <- getwd()
  setwd(wrkDir)
  preClean(wrkDir)
  makeRunIt(wrkDir)
  inFil <- './in.txt'
  writeInputPdCuSG(tPd, tCu, vkV, inFil, toa=toa) 
  system("runIt", show.output.on.console=FALSE)
  moveIt(wrkDir='C:/Temp/')
  k.fil  <- "./out.txt"
  df <- parsePdCuOut(k.fil)
  if(clean){
    file.remove(inFil, k.fil)
  }
  setwd(wd)
  return (df)
}