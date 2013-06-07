normal.bin <-
function(x, do.plot=FALSE, nBreaks=10)
{  
  # now compute the histogram
  h <- hist(x, breaks=nBreaks, plot=do.plot)
  # save what we want
  # midpoints
  h.x <- h$mids
  # counts
  h.cts <- h$counts
  # densities
  h.dens <-h$density
  # make a data frame
  data <- data.frame( x=h.x,
                      cts=h.cts,
                      dens=h.dens)
  # return a list
  mu <- mean(x)
  s <- sd(x)
  out <-list(data, mu, s)
  out
}
