#!/bin/bash

# Convert files from pdf to text using pdftotext

for FILE in *.pdf ; do 
    pdftotext "$FILE" -layout -enc UTF-8
done