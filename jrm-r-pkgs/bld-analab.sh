#! /bin/bash
cd ~/git/jrm-r-pkgs
R CMD build analab
R CMD check analab
R CMD INSTALL ./analab*.tar.gz
rm analab*.gz
rm -rf analab.Rcheck

