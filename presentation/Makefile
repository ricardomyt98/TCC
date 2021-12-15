MAIN=main
OUTPUT=$(MAIN)_$(USER).pdf

main: $(MAIN).tex
	@pdflatex $(MAIN)
	# @bibtex   $(MAIN)
	@pdflatex $(MAIN)
	@pdflatex $(MAIN)
	@mv $(MAIN).pdf $(OUTPUT)

clean:
	@find . -xdev -iname \*~    -print -delete
	@find . -xdev -iname \*.aux -print -delete
	-rm -f texput.log
	-rm -f $(MAIN).log $(MAIN).lot $(MAIN).lof
	-rm -f $(MAIN).toc $(MAIN).bbl $(MAIN).blg
	-rm -f $(MAIN).acr $(MAIN).smb

purge: clean
	@rm -f $(OUTPUT)
