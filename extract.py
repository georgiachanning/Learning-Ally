#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import RegexpParser
from nltk import Tree
import csv
from parameters import Parameters



# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
chunker = RegexpParser(NP)

SARC_folder = '/Users/georgiachanning/LA/SARC_tables'
school_dictionary = {}

for file in os.listdir(SARC_folder):
    try:
        filename = '/Users/georgiachanning/LA/SARC_tables/' + file
        out_file = '/Users/georgiachanning/LA/SARC_extract.csv'
        
        school_feature_dictionary = {}
        school_feature_dictionary["File Name"] = filename
        
        f = open(filename, "rb")
        document_lines = f.readlines()
        f.close()
        # school_name_line = f.find(b'Elementary')
        
        name_token = 'Charter'
        school_name_line = [x for x in range(len(document_lines)) if document_lines[x].find(b'Charter')!= -1]
        if not school_name_line:
            name_token = 'Elementary'
            school_name_line = [x for x in range(len(document_lines)) if document_lines[x].find(b'Elementary')!= -1]
        if not school_name_line:
            name_token = 'School'
            school_name_line = [x for x in range(len(document_lines)) if document_lines[x].find(b'School')!= -1]
        
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
            school_name = continuous_chunk[school_name_index[0]]
            school_name_array = re.split('\W+', school_name)
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
            school_name = ' '.join(school_name_array[lower:upper])
        except IndexError:
            school_name = filename
        
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
            
            
        print(school_feature_dictionary)
    
            
        # start_ELA_table = f.find("English Language Arts")
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

        all_students_line = [x for x in range(start_ELA_table[0], len(document_lines)) if document_lines[x].find(b'All Students')!= -1]

        disabilities_line = [x for x in range(start_ELA_table[0], len(document_lines)) if document_lines[x].find(b'Students with Disabilities')!=-1]
        if not disabilities_line:
            disabilities_line = [x for x in range(start_ELA_table[0], len(document_lines)) if document_lines[x].find(b'Students with')!= -1]
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
        school_dictionary[school_name] = school_feature_dictionary
    except:
        pass
    
#fields = ["School","Disabilities", "File Name", "Gen Ed", "Resource Specialist", "Socioeconomically Disadvantaged"]
header = sorted(set(i for b in map(dict.keys, school_dictionary.values()) for i in b))
with open("table_output.csv", 'w', newline="") as f:
    # w = csv.DictWriter(f, fields )
    write = csv.writer(f)
    write.writerow(['School', *header])
    for a, b in school_dictionary.items():
        write.writerow([a]+[b.get(i, '') for i in header])
    
    
    
    
    
    
        
    

