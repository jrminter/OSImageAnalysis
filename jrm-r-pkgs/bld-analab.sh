#! /bin/bash
cd ~/git/jrm-r-pkgs
R CMD build analab
R CMD check analab
R CMD INSTALL ./analab_1.4.3.tar.gz

