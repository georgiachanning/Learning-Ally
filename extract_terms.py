#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import RegexpParser
from nltk import Tree
import csv
import itertools
import sys
from parameters import Parameters


# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
chunker = RegexpParser(NP)

SARC_folder = '/Users/georgiachanning/LA/SARC_text/'
terms_file_address = '/Users/georgiachanning/LA/terms_list.txt'
school_dictionary = {}

with open (terms_file_address, "r") as f:
    terms = f.read().split('\n')


for file in os.listdir(SARC_folder):
    feature_list = []
    important_terms = {}
    filename = '/Users/georgiachanning/LA/SARC_text/' + file
    f = open(filename, "r")
    document_read = f.read()
    document_content = document_read.replace('\n', ' ')
    document_lines = document_read.split('\n')
    f.close()
    
    try:
        for x in range(0,5):
            if "for" in document_lines[x]:
                words_in_line = document_lines[x].split()
                for index in range(len(words_in_line)):
                    if words_in_line[index] == "for":
                        school_name = (' ').join(words_in_line[index+1:])
                        break            
    except:
        school_name = filename
        
    for term in terms:
        if term.lower() in document_content.lower():
            feature_list.append(term)
    
    important_terms["Other"] = feature_list
    
    if "reading specialist" in document_content.lower():
        important_terms["Reading Specialist"] = "Yes"
    elif "literacy specialist" in document_content.lower():
        important_terms["Reading Specialist"] = "Yes"
    else: 
        important_terms["Reading Specialist"] = "No"
    
    if "dyslexia" in document_content.lower():
        important_terms["Dyslexia mentioned"] = "Yes"
    else:
        important_terms["Dyslexia mentioned"] = "No"
    
    if "Orton-Gillingham" in document_content:
        important_terms["Orton-Gillingham"] = "Yes"
    else:
        important_terms["Orton-Gillingham"] = "No"
    
    if "AVID" in document_content:
        important_terms["AVID"] = "Yes"
    else:
        important_terms["AVID"] = "No"
        
    school_dictionary[school_name] = important_terms
    print(school_name)
    
    
header = sorted(set(i for b in map(dict.keys, school_dictionary.values()) for i in b))
with open("text_output.csv", 'w', newline="") as f:
    # w = csv.DictWriter(f, fields )
    write = csv.writer(f)
    write.writerow(['School', *header])
    for a, b in school_dictionary.items():
        write.writerow([a]+[b.get(i, '') for i in header])
                
                
                
            