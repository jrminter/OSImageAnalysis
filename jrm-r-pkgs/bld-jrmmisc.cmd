cd %GIT_HOME%
cd "./jrm-r-pkgs"
R CMD build jrmmisc
R CMD check jrmmisc
pause
R CMD INSTALL "./jrmmisc_1.0.1.tar.gz"
pause
