#' Write an input file for a StrataGem type simulation for CuPd
#' 
#' Write an input file for GMRFilm to construct an input file for
#' GMRFilm to compute the K-ratios for Pd Ka and Cu Ka for a
#' specified thickness of Pd and Cu for a vector of kV values.
#'
#' @param t.pd Thickness of Pd in nm \code{t.pd}
#' @param t.cu Thickness of Cu in nm \code{t.cu}
#' @param v.kV a vector of voltage (kV) to simulate \code{v.kV}
#' @param fpath full path to the output file (input for GMRFilm) \code{fPath}
#' @param toa The detector take-off angle, \code{toa}
#'
#' @return none No return value but writes the specified output 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### not run
#' # 
#' # setwd("C:/Apps/GMRFilm/")
#' # v.kV = c(10, 12, 15, 20, 25, 30)
#' # write.gmrf.in.pd.cu(200, 400, v.kV, './in.txt')
write.gmrf.in.pd.cu <- function(t.pd, t.cu, v.kV, fpath, toa=35){
  sink(fpath)
  cat("N\n")
  cat("F\n")
  cat("Y\n")
  cat("K\n")
  cat("\n")
  msg <- sprintf("%.1f\n", toa)
  cat(msg)
  cat("E\n")
  cat("Y\n")
  msg <- sprintf("%.1f\n", v.kV[1])
  cat(msg)
  cat("3\n") # 3 layers
  cat("1\n") # 1 element each
  cat("1\n")
  cat("1\n")
  cat("PdLa\n")
  cat("CuKa\n")
  cat("C Ka\n")
  cat("12.023\n")
  cat("8.96\n")
  cat("a\n")
  # do the first thickness
  msg <- sprintf("%.1f\n", 10*t.pd)
  cat(msg)
  msg <- sprintf("%.1f\n", 10*t.cu)
  cat(msg)
  cat("n\n")
  l <- length(v.kV)
  i <- 2
  while (i < l){
    cat("E\n")
    cat("Y\n")
    msg <- sprintf("%.1f\n", v.kV[i])
    cat(msg)
    cat("n\n")
    i = i+1
  }
  # write the last kV
  cat("E\n")
  cat("y\n")
  msg <- sprintf("%.1f\n", v.kV[l])
  cat(msg) 
  cat("N\n")
  cat("\n")
  cat("N\n")
  sink()
}
# setwd("C:/Apps/GMRFilm/")
# v.kV = c(10, 12, 15, 20, 25, 30)
# write.gmrf.in.pd.cu(200, 400, v.kV, './in.txt')
