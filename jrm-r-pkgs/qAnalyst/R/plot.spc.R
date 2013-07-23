`plot.spc` <-
function(x, cex = list(cexStrip=2, cexAxes=2, cexScales=2,cexPoints=1.5), ...) {

    spcObj=x

    # Warning if the chart S has some "hole", due to subgroups with an observation only
   
    if(spcObj$general$chartType=="s" && (length(spcObj$graphPars$points) != length(spcObj$graphPars$points[!is.na(spcObj$graphPars$points)]))) {
        warning("At least one subgroup with dimension lower than 2 in a variable chart for subgroups: chart may be discontinuos", call. = FALSE, immediate. = TRUE)
        warningForPlot = "spaces: subgroups with n=1"
    } else {
        warningForPlot = ""
    }
  
    #graphical settings
    hStrip=2
    cexStrip = cex$cexStrip
    cexAxes = cex$cexAxes
    cexScales = cex$cexScales
    cexPoints = cex$cexPoints
    texcexStrip=paste(spcObj$general$chartType,"chart of ", spcObj$general$xName)
    # options(warn=-1)

    #create the lattice object
    trellis.par.set('layout.heights', list (strip = hStrip))
    pointsForPlot <- spcObj$graphPars$points[!is.na(spcObj$graphPars$points)]
    
    pl = xyplot(spcObj$graphPars$points~spcObj$graphPars$i | texcexStrip, 
        ylim = spcObj$graphPars$ylim,
        ylab = list(spcObj$graphPars$ylab, cex = cexAxes),
        xlab = list(spcObj$graphPars$xlab, cex = cexAxes),
        strip = strip.custom (par.strip.text = list(cex = cexStrip, col = "blue")),
        scales = list(cex=cexScales, x = list(relation = "free")),
        main = list(warningForPlot, cex=1),
        

        panel = function(x, y, ...) {
            panel.lines(spcObj$graphPars$iForLimits, spcObj$graphPars$ucl3ForLimits, col = "grey", lwd = 6)
            panel.lines(spcObj$graphPars$iForLimits, spcObj$graphPars$lcl3ForLimits, col = "grey", lwd = 6)
            panel.lines(spcObj$graphPars$iForLimits, rep(spcObj$graphPars$center, each=2), col = "grey", lwd = 10)
            panel.lines(x, y, col = "blue", lwd = 3, ...)
            panel.xyplot(x, y, col = spcObj$graphPars$color, pch = 16, cex = cexPoints,...)
        }
    )


        
    #print the object via lattice
    print(pl)
    invisible(NULL)
}

