# latex-autosplit
latex-autosplit helps to speed up latex beamer compilation by putting every frame in its own file

## Dependencies

- python
- pdflatex

## Features

- splitting latex files based on environments
- `\input{other-file}`
- detecting changes


## Example

The following script demonstrates the use of this script:
```
cd test-data/2
mkdir tmp/
python3 ../../latex-autosplit.py --tmp-dir tmp/ --compile main.tex
```
Directory `test-data/2/tmp/` will contain one pdf for each frame. Try executing it a second time. latex-autosplit will only compile frames that have not changed.

