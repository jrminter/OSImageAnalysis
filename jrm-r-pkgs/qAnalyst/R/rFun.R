`rFun` <-
function(x) {
    if (length(na.omit(x))>0) {
        range1 = diff(range(x, na.rm = TRUE))
    }
    
    # NA if only missing values
    else {
        range1 = NA
    }

    return(range1)
}

