cd %GIT_HOME%
cd "./jrm-r-pkgs"
R CMD build measureLines
R CMD check measureLines
pause
R CMD INSTALL "./measureLines_1.0.2.tar.gz"
pause
