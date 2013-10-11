#' Write an input file for a StrataGem type simulation for CuNi
#' 
#' Write an input file for GMRFilm to construct an input file for
#' GMRFilm to compute the K-ratios for Ni Ka and Cu Ka for a
#' vector of acellerating voltages and specifed thickeness values
#' by any spaces. 
#'
#' @param t.ni Thickness of Ni in nm \code{t.ni}
#' @param t.cu Thickness of Cu in nm \code{t.ni}
#' @param v.kv A vector of voltages to simulate \code{v.kv}
#' @param fpath full path to the output file (input for GMRFilm) \code{fPath}
#'
#' @return none No return value but writes the specified output 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' R code here showing how your function works
#' 
write.gmrf.in.ni.cu <- function(t.ni, t.cu, v.kv, fpath, toa=35){
  
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
  cat("NiKa\n")
  cat("CuKa\n")
  cat("C Ka\n")
  cat("n\n")
  cat("8.90\n")
  cat("8.96\n")
  cat("a\n")
  msg <- sprintf("%.1f\n", 10*t.ni)
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

# write.gmrf.in.ni.ni(200, 500, c(12, 15, 20, 25, 30), "C:/apps/GMRFilm/myTest.txt", toa=35)
