#' Compute the backscattered electron yield for an element
#' 
#' Use the method of Pouchou and Pichoir 1991 to compute the backscattered
#' electron yield for a given element
#'
#' @param z The atomic number of the element \code{z}
#'
#' @return the backscattered electron yield 
#'
#' @keywords keywords
#'
#' @export
#' 
#' @examples
#' # Compute for Cu
#' eta <- papEta(29)

papEta <- function(z){
  ret <- 1.75e-3 * z + 0.37 * (1.0 - exp(-0.015 * z^1.3))
  ret
}