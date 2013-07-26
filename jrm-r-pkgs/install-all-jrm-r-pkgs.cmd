REM 
REM __install-all-jrm-r-pkgs.cmd
REM 
REM J. R. Minter Version of 2013-07-24
REM 
REM Build and install the current version of all jrm R packages
REM NOTE the environment variable %GITHOME% needs window style pathname
REM 

cd %GITHOME%
cd "edp/R"
R CMD build Peaks
R CMD INSTALL ./Peaks_*.tar.gz
R CMD build edp
R CMD INSTALL ./edp_*.tar.gz
DEL /Q *.gz

cd %GITHOME%
cd "OSImageAnalysis/jrm-r-pkgs"
R CMD build analab
R CMD INSTALL analab_*.tar.gz
R CMD build jrmmisc
R CMD INSTALL jrmmisc_*.tar.gz
R CMD build measureLines
R CMD INSTALL measureLines_*.tar.gz
R CMD build qAnalyst
R CMD INSTALL qAnalyst_*.tar.gz
R CMD build tikzDevice
R CMD INSTALL tikzDevice_*.tar.gz

DEL /Q *.gz

pause
