Open this script, configure the regions and variables you have plots to dump into beamer:
`./dump_plots_to_beamer.py`

This makes a latex file `frames.tex`, which can be inserted into you own beamer template.

Alternatively, you can compile the predefined `slides.tex` into a PDF.
```
module load texlive
pdflatex slides
``` 
