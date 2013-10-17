#! /bin/bash
cd ~/git/jrm-r-pkgs
R CMD build measureLines
R CMD check measureLines
R CMD INSTALL ./measureLines_1.0.2.tar.gz
rm ./measureLines_1.0.2.tar.gz
rm -rf measureLines.Rcheck


