R CMD build jrmmisc
R CMD check jrmmisc
pause
R CMD INSTALL ./jrmmisc_*.gz
pause
RD /S /Q jrmmisc.Rcheck
del ./jrmmisc*.gz
pause
