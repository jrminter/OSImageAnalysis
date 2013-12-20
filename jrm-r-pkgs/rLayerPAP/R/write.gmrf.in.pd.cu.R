#' Write an input file for a StrataGem type simulation for CuPd
#' 
#' Write an input file for GMRFilm to construct an input file for
#' GMRFilm to compute the K-ratios for Pd La and Cu Ka for a
#' vector of accelerating voltages and specified thickness values
#' by any spaces. 
#'
#' @param t.pd Thickness of Pd in nm \code{t.pd}
#' @param t.cu Thickness of Cu in nm \code{t.pd}
#' @param v.kv A vector of voltages to simulate \code{v.kv}
#' @param fpath full path to the output file (input for GMRFilm) \code{fPath}
#' @param toa The detector take-off angle, \code{v.kv}
#'
#' @return none No return value but writes the specified output 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' ### not run
#'
#' 
write.gmrf.in.pd.cu <- function(t.pd, t.cu, v.kv, fpath, toa=35){
  
  sink(fpath)
  cat("S\n")
  cat("N\n")
  cat("F\n")
  cat("Y\n")
  cat("K\n")
  msg <- sprintf("%.1f\n", toa)
  cat(msg)
  cat("e\n")
  msg <- sprintf("%.1f\n", v.kv[1])
  cat(msg)
  cat("3\n") # 3 layers
  cat("1\n") # 1 element each
  cat("1\n")
  cat("1\n")
  cat("PdLa\n")
  cat("CuKa\n")
  cat("C Ka\n")
  cat("n\n")
  cat("12.023\n")
  cat("8.96\n")
  cat("a\n")
  msg <- sprintf("%.1f\n", 10*t.pd)
  cat(msg)
  msg <- sprintf("%.1f\n", 10*t.cu)
  cat(msg)
  cat("n\n")
  cat("y\n")
  l <- length(v.kv)
  i <- 2
  while (i < l){
    cat("E\n")
    msg <- sprintf("%.1f\n", v.kv[i])
    cat(msg)
    cat("n\n")
    cat("y\n")
    i = i+1
  }
  cat("E\n")
  msg <- sprintf("%.1f\n", v.kv[l])
  cat(msg)
  cat("n\n")
  cat("n\n")
  sink()
}

# write.gmrf.in.pd.pd(200, 500, c(12, 15, 20, 25, 30), "C:/apps/GMRFilm/myTest.txt", toa=35)
