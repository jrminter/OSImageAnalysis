#' Write an input file for a StrataGem type simulation for CuNi
#' 
#' Write an input file for GMRFilm to construct an input file for
#' GMRFilm to compute the K-ratios for Ni Ka and Cu Ka for a
#' specified thickness of Ni and Cu for a vector of kV values.
#'
#' @param tNi Thickness of Ni in nm \code{tNi}
#' @param tCu Thickness of Cu in nm \code{tCu}
#' @param vkV A vector of voltage to simulate \code{vkV} 
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

writeInputNiCuSG <- function(tNi, tCu, vkV, fPath, toa=35){
  sink(fPath)
  cat("N\n")
  cat("F\n")
  cat("Y\n")
  cat("K\n")
  cat("\n")
  msg <- sprintf("%.1f\n", toa)
  cat(msg)
  cat("E\n")
  cat("Y\n")
  msg <- sprintf("%.1f\n", vkV[1])
  cat(msg)
  cat("3\n") # 3 layers
  cat("1\n") # 1 element each
  cat("1\n")
  cat("1\n")
  cat("NiKa\n")
  cat("CuKa\n")
  cat("C Ka\n")
  cat("8.90\n")
  cat("8.96\n")
  cat("a\n")
  # do the first thickness
  msg <- sprintf("%.1f\n", 10*tNi)
  cat(msg)
  msg <- sprintf("%.1f\n", 10*tCu)
  cat(msg)
  cat("n\n")
  l <- length(vkV)
  i <- 2
  while (i < l){
    cat("E\n")
    cat("Y\n")
    msg <- sprintf("%.1f\n", vkV[i])
    cat(msg)
    cat("n\n")
    i = i+1
  }
  # write the last kV
  cat("E\n")
  cat("y\n")
  msg <- sprintf("%.1f\n", vkV[l])
  cat(msg) 
  cat("N\n")
  cat("\n")
  cat("N\n")
  sink()
}
