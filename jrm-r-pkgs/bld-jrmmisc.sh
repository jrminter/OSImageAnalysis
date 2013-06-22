#! /bin/bash
cd ~/git/jrm-r-pkgs
R CMD build jrmmisc
R CMD check jrmmisc
R CMD INSTALL ./jrmmisc_1.0.1.tar.gz
rm ./jrmmisc_1.0.1.tar.gz
rm -rf jrmmisc.Rcheck


