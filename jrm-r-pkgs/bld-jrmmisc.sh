#! /bin/bash
cd ~/git/jrm-r-pkgs
R CMD build jrmmisc
R CMD check jrmmisc
R CMD INSTALL ./jrmmisc*.tar.gz
rm ./jrmmisc*.tar.gz
rm -rf jrmmisc.Rcheck


