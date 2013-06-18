# misclassification.from.table.R
misclassification.from.table <- function(x){
  # from Patrick Breheny
  # http://r.789695.n4.nabble.com/misclassification-rate-td3787075.html
  misclass <- 1-sum(diag(x))/sum(x) 
  misclass 
}
