#! /bin/bash
cd ~/git/OSImageAnalysis/jrm-r-pkgs
R CMD BATCH ./doc_rLayerPap.R
cat doc_rLayerPap.Rout
R CMD build rLayerPAP
R CMD check rLayerPAP
R CMD INSTALL ./rLayerPAP_*.tar.gz
rm ./rLayerPAP_*.tar.gz
rm -rf rLayerPAP.Rcheck
rm -rf doc_rLayerPap.Rout


