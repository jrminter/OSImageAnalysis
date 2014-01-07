R CMD build measureLines
R CMD check measureLines
pause
R CMD INSTALL ./measureLin*.tar.gz
RD /S /Q measureLines.Rcheck
del meas*gz
pause
