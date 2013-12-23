#' Compute PAP K-Ratios for Pd/Cu using GMRFilm
#' 
#' Compute the PdKa and CuKa K-ratios using GMRFilm for a vector
#' of accelerating voltages for specified Pd and Cu thickness values. 
#' Note: this corrects for continuum fluorescence
#'
#' @param v.kv A vector of kvs to simulate \code{v.kv}
#' @param t.pd Pd thickness in nm \code{t.pd}
#' @param t.cu Cu thickness in nm \code{t.cu}
#' @param toa take off angle for detector in deg \code{toa}
#' @param wrkDir Working directory \code{wrkDir}
#' @param clean Boolean to delete input/output files\code{clean}
#'
#' @return df A data frame with the kVs and the Pd and Cu K-a K-ratios 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### Not run
#' # v.kV <- 10:30
#' # print(v.kV)
#' # df <- df <- pap.sim.pd.cu(v.kV, 8.8, 861., 35.0, wrkDir='C:/Temp/', clean=FALSE)
#' # print(head(df))
#' 
pap.sim.pd.cu <- function(v.kv, t.pd, t.cu, toa,
                          wrkDir='C:/Temp/',
                          clean=FALSE){
  wd <- getwd()
  setwd(wrkDir)
  # get rid of old output files
  files <- list.files(pattern="^[F]")
  file.remove(files)
  make.gmrf.run.it(wrkDir)
  inFil <- paste0(wrkDir, './in.txt')
  write.gmrf.in.pd.cu(t.pd, t.cu, v.kv, inFil, toa=toa) 
  cmd <- "runIt"
  system(cmd, show.output.on.console=TRUE)
  k.fil  <- "./out.txt"
  df <- parse.pd.cu.gmrf.sg.out(k.fil)
  if(clean){
    file.remove(inFil, k.fil)
  }
  setwd(wd)
  return (df)
}