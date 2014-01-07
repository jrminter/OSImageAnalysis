R CMD BATCH doc_rLayerPap.R
cat doc_rLayerPap.Rout
R CMD build rLayerPAP
pause
R CMD check rLayerPAP
R CMD INSTALL ./rLayerPAP*.gz
del rLayerPAP*.gz
RD /S /Q rLayerPAP.Rcheck
del doc_rLayerPap.Rout
pause
