#!/bin/tcsh
cd /Users/jrminter/git/OSImageAnalysis/ekRochEmp/R
R CMD Sweave ekRochEmp.Rnw
pdflatex ekRochEmp
bibtex ekRochEmp
pdflatex ekRochEmp
pdflatex ekRochEmp

rm *.aux
rm *.dvi
rm *.log
rm *.tex
rm *.bbl
rm *.blg
rm ekRochEmp-*.*
rm Rplots.pdf
rm .Rhistory

