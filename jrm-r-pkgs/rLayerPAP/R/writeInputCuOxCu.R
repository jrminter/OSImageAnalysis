#' Write an input file for a GMRFilm simulation of CuOx on Cu
#' 
#' Write an input file for GMRFilm to construct an input file for
#' GMRFilm to compute the K-ratios for O Ka and Cu La for a
#' specified thickness of CuOx and Cu for a single e0 values.
#'
#' @param tOx Thickness of CuOx in nm \code{tOx}
#' @param wfOx weight fraction O in oxide layer \code{wfOx}
#' @param wfCu weight fraction Cu in oxide layer \code{wfCu}
#' @param rhoOx density of oxide layer \code{rhoOx}
#' @param e0 A kV to simulate \code{e0} 
#' @param fPath full path to the output file \code{fPath}
#' @param toa The detector take-off angle \code{toa}
#'
#' @return none
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### not run

writeInputCuOxCu.R <- function(tOx, wfOx, wfCu, rhoOx, e0, fPath, toa=35){
  sink(fPath)
  cat("N\n")
  cat("F\n")
  cat("Y\n")
  cat("K\n")
  cat("N\n")
  msg <- sprintf("%.1f\n", toa)
  cat(msg)
  cat("E\n")
  cat("Y\n")
  msg <- sprintf("%.1f\n", e0)
  cat(msg)
  cat("2\n") # 2 layers
  cat("2\n") # 2 elements in first
  cat("1\n") # 1 in second
  cat("O Ka,s\n") # input stoichiometry
  cat("CuLa,s\n") # input stoichiometry
  cat("CuLa\n") # substrate is pure
  msg <- sprintf("%.1f\n", rhoOx)
  cat(msg)
  cat("a\n")
  # do the first thickness
  msg <- sprintf("%.1f\n", 10*tOx)
  cat(msg)
  cat("w\n")
  msg <- sprintf("%.4f\n", wfOx)
  cat(msg)
  msg <- sprintf("%.4f\n", wfCu)
  cat(msg)
  cat("n\n")
  cat("\n")
  cat("\n")
  sink()
}
