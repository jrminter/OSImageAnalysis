R CMD build rLayerPAP
pause
R CMD INSTALL "./rLayerPAP*.gz"
del rLayerPAP*.gz
pause
