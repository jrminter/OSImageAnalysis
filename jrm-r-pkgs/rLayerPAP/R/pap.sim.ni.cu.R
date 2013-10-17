#' Compute PAP K-Ratios for Ni/Cu using GMRFilm
#' 
#' Compute the NiKa and CuKa K-ratios using GMRFilm for a vector
#' of accelerating voltages for specified Ni and Cu thickness values. 
#' Note: this corrects for continuum fluorescence
#'
#' @param v.kv A vector of kvs to simulate \code{v.kv}
#' @param t.ni Ni thickness in nm \code{t.ni}
#' @param t.cu Cu thickness in nm \code{t.cu}
#' @param toa take off angle for detector in deg \code{toa}
#' @param pgDir location of GMRFilm \code{pgDir}
#' @param clean Boolean to delete input/output files\code{clean}
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
pap.sim.ni.cu <- function(v.kv, t.ni, t.cu, toa,
                          pgDir='C:/Apps/GMRfilm',
                          clean=TRUE){
  wd <- getwd()
  setwd(pgDir)
  # get rid of old output files
  files <- list.files(pattern="^[F]")
  file.remove(files)
  inFil <- paste0(pgDir, '/myTest.txt')
  write.gmrf.in.ni.cu(t.ni, t.cu, v.kv, inFil, toa=toa) 
  cmd <- "gmrfilm < myTest.txt"
  system(cmd, show.output.on.console=TRUE)
  files <- list.files(pattern="^[F]")
  file.rename(files[1], "myOut.txt")
  
  # print(list.files())
  k.fil  <- "C:/apps/GMRFilm/myOut.txt"
  df <- parseCuNiKaPetPAP(v.kv, k.fil)
  # print(df)
  if(clean){
    file.remove(inFil, k.fil)
  }
  setwd(wd)
  return (df)
}