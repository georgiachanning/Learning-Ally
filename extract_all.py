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
from os import path

# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
chunker = RegexpParser(NP)

def main():
    SARC_folder = '/Users/georgiachanning/LA/SARC/'
    terms_file_address = '/Users/georgiachanning/LA/terms_list.txt'
    school_dictionary = {}
    
    for file in os.listdir(SARC_folder):
        school_feature_dictionary = {}
        school_feature_dictionary["File Name"] = file
        text_filename = '/Users/georgiachanning/LA/SARC_text/' + file[:-4] + "_text.txt"
        table_filename = '/Users/georgiachanning/LA/SARC_tables/' + file[:-4] + "_tables.txt"
        out_file = '/Users/georgiachanning/LA/SARC_extract.csv'
        
        if path.exists(table_filename):
            print(table_filename)
            
            f = open(table_filename, "rb")
            document_lines = f.readlines()
            f.close()
            
            name_token = 'Charter'
            school_name_line = [x for x in range(len(document_lines)) if document_lines[x].find(b'Charter')!= -1]
            if not school_name_line:
                name_token = 'Elementary'
                school_name_line = [x for x in range(len(document_lines)) if document_lines[x].find(b'Elementary')!= -1]
            if not school_name_line:
                name_token = 'School'
                school_name_line = [x for x in range(len(document_lines)) if document_lines[x].find(b'School')!= -1]
            
            if school_name_line:
                school_name_line_chunked = chunker.parse(pos_tag(word_tokenize(str(document_lines[school_name_line[0]]))))
                continuous_chunk = []
                current_chunk = []
                for subtree in school_name_line_chunked:
                    if type(subtree) == Tree:
                        current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
                    elif current_chunk:
                        named_entity = " ".join(current_chunk)
                        if named_entity not in continuous_chunk:
                            continuous_chunk.append(named_entity)
                            current_chunk = []
                    else:
                        continue
                
                school_name_index = [x for x in range(len(continuous_chunk)) if continuous_chunk[x].find(name_token)!= -1]
                try:
                    table_school_name = continuous_chunk[school_name_index[0]]
                    school_name_array = re.split('\W+', table_school_name)
                    middle = [x for x in range(len(school_name_array)) if school_name_array[x]== name_token]
                    lower = [x for x in range(middle[0]) if school_name_array[x]== "NaN" or school_name_array[x].islower()]
                    if lower:
                        lower = lower[-1] + 1
                    else:
                        lower = 0
                    upper = [x for x in range(middle[0], len(school_name_array)) if "NaN" in school_name_array[x] or school_name_array[x].islower()]
                    if upper:
                        upper = upper[0]
                    else:
                        upper = len(school_name_array)
                    table_school_name = ' '.join(school_name_array[lower:upper])
                except IndexError:
                    table_school_name = file
            else:
                table_school_name = file
            
            socioeconomically_disadvantaged_line_number = [x for x in range(len(document_lines)) if document_lines[x].find(b'Socioeconomically Disadvantaged')!= -1]
            if not socioeconomically_disadvantaged_line_number:
                socioeconomically_disadvantaged_line_number = [x for x in range(len(document_lines)) if document_lines[x].find(b'Socioeconomically')!= -1]
            try:
                socioeconomically_disadvantaged_line = document_lines[socioeconomically_disadvantaged_line_number[0]]
                socioeconomically_disadvantaged = re.findall("\d+\.\d+", socioeconomically_disadvantaged_line.decode('utf-8')) 
                school_feature_dictionary["Socioeconomically Disadvantaged"] = socioeconomically_disadvantaged
            except IndexError:
                school_feature_dictionary["Socioeconomically Disadvantaged"] = "Unknown"
            
            # resource_specialist_line = f.find("Resource Specialist")
            resource_specialist_line = [x for x in range(len(document_lines)) if document_lines[x].find(b'Resource Specialist')!= -1]
            if not resource_specialist_line:
                school_feature_dictionary["Resource Specialist"] = "Unknown"
            else:
                percent_available = re.findall("\d+\.\d+|\.\d+", document_lines[resource_specialist_line[0]].decode('utf-8'))
                if not percent_available:
                    school_feature_dictionary["Resource Specialist"] = "Unknown"
                else: 
                    school_feature_dictionary["Resource Specialist"] = percent_available
                
                
            start_ELA_table = [x for x in range(len(document_lines)) if document_lines[x].find(b'Test Results in ELA')!= -1]
            if not start_ELA_table:
                start_ELA_table = [x for x in range(len(document_lines)) if document_lines[x].find(b'Test Results in English Language Arts')!= -1]
            if not start_ELA_table:
                start_ELA_table = [x for x in range(len(document_lines)) if document_lines[x].find(b'Test Results')!= -1]
            if not start_ELA_table:
                start_ELA_table = [x for x in range(len(document_lines)) if document_lines[x].find(b'CAASPP')!= -1]
            if not start_ELA_table:
                start_ELA_table = [x for x in range(len(document_lines)) if document_lines[x].find(b'ELA')!= -1]
            if not start_ELA_table:
                start_ELA_table = [x for x in range(len(document_lines)) if document_lines[x].find(b'English Language Arts')!= -1]
    
            try:
                all_students_line = [x for x in range(start_ELA_table[0], len(document_lines)) if document_lines[x].find(b'All Students')!= -1]
            except:
                pass
    
            try:
                disabilities_line = [x for x in range(start_ELA_table[0], len(document_lines)) if document_lines[x].find(b'Students with Disabilities')!=-1]
            except: 
                pass
            if not disabilities_line:
                try:
                    disabilities_line = [x for x in range(start_ELA_table[0], len(document_lines)) if document_lines[x].find(b'Students with')!= -1]
                except:
                    pass
            try:
                gen_ed_met_or_exceeded = re.findall("\d+\.\d+", document_lines[all_students_line[0]].decode('utf-8'))[-1]
                disabilities_met_or_exceeded = re.findall("\d+\.\d+", document_lines[disabilities_line[0]].decode('utf-8'))[-1]
            except IndexError:
                try:
                    gen_ed_met_or_exceeded = re.findall("\d+\.\d+", document_lines[all_students_line[1]].decode('utf-8'))[-1]
                    disabilities_met_or_exceeded = re.findall("\d+\.\d+", document_lines[disabilities_line[1]].decode('utf-8'))[-1]
                except IndexError:
                    gen_ed_met_or_exceeded = "Unknown"
                    disabilities_met_or_exceeded = "Unknown"
                
            
            school_feature_dictionary["Gen Ed"] = gen_ed_met_or_exceeded
            school_feature_dictionary["Disabilities"] = disabilities_met_or_exceeded
            print(school_feature_dictionary)
    
        with open (terms_file_address, "r") as f:
            terms = f.read().split('\n')
    
    
        feature_list = []
        # important_terms = {}
        try:
            f = open(text_filename, "r")
        except FileNotFoundError:
            try: 
                school_dictionary[table_school_name] = school_feature_dictionary
            except:
                school_dictionary[file] = school_feature_dictionary
            continue
        
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
                            text_school_name = (' ').join(words_in_line[index+1:])
                            break            
        except:
            text_school_name = file
        
        stripped_text = "".join(document_content.lower().strip())
        for term in terms:
            stripped_term = "".join(term.lower().strip())
            if stripped_term in stripped_text:
                feature_list.append(term)
        
        school_feature_dictionary["Other"] = feature_list
        
        if "".join("reading specialist".strip()) in stripped_text:
            school_feature_dictionary["Reading Specialist"] = "Yes"
        elif "".join("literacy specialist".strip()) in stripped_text:
            school_feature_dictionary["Reading Specialist"] = "Yes"
        elif "".join("literacy coach".strip()) in stripped_text:
            school_feature_dictionary["Reading Specialist"] = "Yes"
        elif "".join("reading coach".strip()) in stripped_text:
            school_feature_dictionary["Reading Specialist"] = "Yes"
        elif "".join("intervention teacher".strip()) in stripped_text:
            school_feature_dictionary["Reading Specialist"] = "Yes" 
        else: 
            school_feature_dictionary["Reading Specialist"] = "No"
        
        if "dyslexia" in stripped_text:
            school_feature_dictionary["Dyslexia mentioned"] = "Yes"
        else:
            school_feature_dictionary["Dyslexia mentioned"] = "No"
        
        if "".join("Orton-Gillingham".lower().strip()) in stripped_text:
            school_feature_dictionary["Orton-Gillingham"] = "Yes"
        elif "".join("Orton Gillingham".lower().strip()) in stripped_text:
            school_feature_dictionary["Orton-Gillingham"] = "Yes"
        else:
            school_feature_dictionary["Orton-Gillingham"] = "No"
        
        if "AVID" in document_content:
            school_feature_dictionary["AVID"] = "Yes"
        else:
            school_feature_dictionary["AVID"] = "No"
            
        try:
            if text_school_name is table_school_name:
                school_name = text_school_name
            elif text_school_name is file:
                school_name = table_school_name
            elif table_school_name is file:
                school_name = text_school_name
            else:
                school_name = text_school_name + "/" + table_school_name
        except NameError:
            school_name = text_school_name
            
        school_dictionary[school_name] = school_feature_dictionary
        print(school_name)
        
        
    header = sorted(set(i for b in map(dict.keys, school_dictionary.values()) for i in b))
    with open("all_output.csv", 'w', newline="") as f:
        write = csv.writer(f)
        write.writerow(['School', *header])
        for a, b in school_dictionary.items():
            write.writerow([a]+[b.get(i, '') for i in header])
    
    return

if __name__ == '__main__':
    main()

