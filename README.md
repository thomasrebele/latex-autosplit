# latex-autosplit
latex-autosplit helps to speed up latex / latex beamer compilation by putting every section / frame in its own file

## Dependencies

- python
- pdflatex

## Features

- splitting latex files based on sections or environments
- supports including other files with `\input{other-file}`
- recompile only changed parts


## Example

The following script demonstrates the use of this script:
```
cd test-data/2
mkdir tmp/
python3 ../../latex-autosplit.py --tmp-dir tmp/ --compile main.tex
```
Directory `test-data/2/tmp/` will contain one pdf for each frame. Try executing it a second time. latex-autosplit will only compile frames that have changed.

I recommend mergin the individual files with `pdfunite`

```
pdfunite tmp/pre*.pdf tmp/all.pdf
```

