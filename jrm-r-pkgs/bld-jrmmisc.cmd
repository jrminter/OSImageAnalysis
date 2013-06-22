R CMD build jrmmisc
R CMD check jrmmisc
pause
R CMD INSTALL "./jrmmisc*.gz"
del jrmmisc*.gz
pause
