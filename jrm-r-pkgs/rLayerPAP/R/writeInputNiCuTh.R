#' Write an input file to simulate of a range Ni thickness on Cu
#' 
#' Write an input file for GMRFilm to construct an input file for
#' GMRFilm to compute the K-ratios for Ni Ka and Cu Ka for a
#' vector of Ni thickness (nm) a at a single Cu thickness (tCu)
#' and kV (e0).
#'
#' @param vNi A vector of thickness of Ni in nm \code{vNi}
#' @param tCu Thickness of Cu in nm \code{tCu}
#' @param e0 A voltage (kV) to simulate \code{e0}
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

writeInputNiCuTh <- function(vNi, tCu, e0, fPath, toa=35){
  sink(fPath)
  cat("N\n")
  cat("F\n")
  cat("Y\n")
  cat("K\n")
  cat("N\n")
  msg <- sprintf("%.1f\n", toa)
  cat(msg)
  cat("e\n")
  cat("Y\n")
  msg <- sprintf("%.1f\n", e0)
  cat(msg)
  cat("3\n") # 3 layers
  cat("1\n") # 1 element each
  cat("1\n")
  cat("1\n")
  cat("NiKa\n")
  cat("CuKa\n")
  cat("C Ka\n")
  cat("n\n")
  cat("8.90\n")
  cat("8.96\n")
  cat("a\n")
  # do the first thickness
  msg <- sprintf("%.1f\n", 10*vNi[1])
  cat(msg)
  msg <- sprintf("%.1f\n", 10*tCu)
  cat(msg)
  l <- length(vNi)
  i <- 2
  while (i < l){
    cat("Y\n")
    cat("a\n")
    msg <- sprintf("%.1f\n", 10*vNi[i])
    cat(msg)
    msg <- sprintf("%.1f\n", 10*tCu)
    cat(msg)
    i = i+1
  }
  # write the last layer
  cat("Y\n")
  cat("a\n")
  msg <- sprintf("%.1f\n", 10*vNi[l])
  cat(msg)
  msg <- sprintf("%.1f\n", 10*tCu)
  cat(msg) 
  cat("N\n")
  cat("\n")
  cat("n\n")
  cat("\n")
  cat("\n")
  sink()
}
