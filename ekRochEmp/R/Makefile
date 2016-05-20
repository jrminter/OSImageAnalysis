BASE=ekRochEmp

all: $(BASE).pdf

$(BASE).tex: $(BASE).Rnw
		Rscript -e "library('knitr'); knit('$(BASE).Rnw')"
		
$(BASE).pdf: $(BASE).tex
	xelatex $(BASE)
	# bibtex $(BASE)
	xelatex $(BASE)
	xelatex $(BASE)
	
clean:
	rm -rf figure
	rm -rf *.a*
	rm -rf *.b*
	rm -rf *.synctex.gz
	rm -rf *.l*
	rm -rf *.t*
	rm -ff *.out
	
distclean: $(BASE).pdf clean
			