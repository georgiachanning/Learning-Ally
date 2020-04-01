# Learning-Ally README

This repository contains the files associated with the text extraction and evaluation of LCAPs and SARCs for the identification of California pilot schools for the UCSF Dyslexia Center. The structure and paths reflect those on my local machine, so will have to be updated before the code can be redeployed. Code is commented, but as a brief overview:

extract.py evaluates tables data from the SARC tables. 
extract_terms.py finds keywords from PDFs read into plain test (LCAP or SARC). 
extract_all.py extracts both table and text data from SARCS. 
find_missing.py identifies the CDS codes of schools not yet processed. 
tables.py converts PDF to table/text. 
LCAP.py web-scrapes for LCAPs. 
SARC.py web-scrapes for SARCs. 

Other miscellaneous files not housed within a folder contain information relevant to one or more of the above .py files. Most output is within a subfolder-- with the exception of all_output.csv, which is a single file output from extract_all.py. 
