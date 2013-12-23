#' Pre-clean for GMRFilm
#'
#' @param wrkDir Working directory for GMRFilm simulation \code{wrkDir}
#'
#' @return none
#'
#' @keywords keywords
#'
#' @export

preClean <- function(wrkDir='C:/Temp/'){
  setwd(wrkDir)
  # get rid of old output files
  files <- list.files(pattern="^[F]")
  file.remove(files)
  files <- list.files(pattern="standard.dat")
  file.remove(files)
}