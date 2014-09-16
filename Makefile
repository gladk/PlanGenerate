#!/usr/bin/make -f

FILETEX = plan
addSuffix = ''
MAKEPDF = xelatex
SHOWPDF = evince

all: clean dias createpdf showpdf
pdf: clean createpdf showpdf

createpdf:
	${MAKEPDF} $(FILETEX).tex
	#bibtex $(FILETEX).aux
	#${MAKEPDF} $(FILETEX).tex
	${MAKEPDF} $(FILETEX).tex
	
showpdf:
	${SHOWPDF} ./$(FILETEX).pdf &

clean:
	find ./ -type f -name "*.aux" | xargs rm -rf
	find ./ -type f -name "*.log" | xargs rm -rf
	find ./ -type f -name "*.bbl" | xargs rm -rf
	find ./ -type f -name "*.dvi" | xargs rm -rf
	find ./ -type f -name "*.blg" | xargs rm -rf
	find ./ -type f -name "*.out" | xargs rm -rf
	find ./ -type f -name "*.backup" | xargs rm -rf
	find ./ -type f -name "*.tex~" | xargs rm -rf
