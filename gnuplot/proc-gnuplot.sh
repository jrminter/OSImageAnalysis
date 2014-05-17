#!/bin/bash
# proc-gnuplot.sh
ps2pdf $1.ps temp.pdf
pdfcrop --margins 4 temp.pdf $1.pdf
rm -rf temp.pdf
