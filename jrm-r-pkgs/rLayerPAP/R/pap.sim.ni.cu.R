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
#' @param wrkDir Working directory \code{wrkDir}
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
#' # v.kV <- 10:30
#' # print(v.kV)
#' # df <- pap.sim.ni.cu(v.kV, 8.8, 861., 35.0, wrkDir='C:/Temp/', clean=FALSE)
#' # print(head(df))
#' 
pap.sim.ni.cu <- function(v.kv, t.ni, t.cu, toa,
                          wrkDir='C:/Temp/',
                          clean=FALSE){
  wd <- getwd()
  setwd(wrkDir)
  # get rid of old output files
  files <- list.files(pattern="^[F]")
  file.remove(files)
  make.gmrf.run.it(wrkDir)
  inFil <- paste0(wrkDir, './in.txt')
  write.gmrf.in.ni.cu(t.ni, t.cu, v.kv, inFil, toa=toa) 
  cmd <- "runIt"
  system(cmd, show.output.on.console=TRUE)
  k.fil  <- "./out.txt"
  df <- parse.ni.cu.gmrf.sg.out(k.fil)
  # print(df)
  if(clean){
    file.remove(inFil, k.fil)
  }
  setwd(wd)
  return (df)
}