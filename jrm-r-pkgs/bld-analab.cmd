R CMD build analab
R CMD check analab
R CMD INSTALL "./analab*.tar.gz"
del analab*.gz
RD /S /Q analab.Rcheck

pause
