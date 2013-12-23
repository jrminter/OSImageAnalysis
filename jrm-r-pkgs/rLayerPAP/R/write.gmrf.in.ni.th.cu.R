#' Write an input file for a simulation of a range Ni thickness on Cu
#' 
#' Write an input file for GMRFilm to construct an input file for
#' GMRFilm to compute the K-ratios for Ni Ka and Cu Ka for a
#' vector of Ni thickness (nm) a at a single Cu thickness (tCu)
# 'and kV (e0).
#'
#' @param v.ni A vector of thickness of Ni in nm \code{v.ni}
#' @param t.cu Thickness of Cu in nm \code{t.cu}
#' @param e0 A voltage (kV) to simulate \code{e0}
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
#' # setwd("C:/Temp/GMRFilm/")
#' # v.ni = c(50, 100, 200)
#' # write.gmrf.in.ni.th.cu(v.ni, 400, 15, './in.txt')
write.gmrf.in.ni.th.cu <- function(v.ni, t.cu, e0, fpath, toa=35){
  sink(fpath)
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
  msg <- sprintf("%.1f\n", 10*v.ni[1])
  cat(msg)
  msg <- sprintf("%.1f\n", 10*t.cu)
  cat(msg)
  l <- length(v.ni)
  i <- 2
  while (i < l){
    cat("Y\n")
    cat("a\n")
    msg <- sprintf("%.1f\n", 10*v.ni[i])
    cat(msg)
    msg <- sprintf("%.1f\n", 10*t.cu)
    cat(msg)
    i = i+1
  }
  # write the last layer
  cat("Y\n")
  cat("a\n")
  msg <- sprintf("%.1f\n", 10*v.ni[l])
  cat(msg)
  msg <- sprintf("%.1f\n", 10*t.cu)
  cat(msg) 
  cat("N\n")
  cat("\n")
  cat("n\n")
  cat("\n")
  cat("\n")
  sink()
}
# setwd("C:/Apps/GMRFilm/")
# v.ni = c(50, 100, 200)
# write.gmrf.in.ni.th.cu(v.ni, 400, 15, './in.txt')
