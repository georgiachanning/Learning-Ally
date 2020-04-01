#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tabula
import PyPDF2
import os
from parameters import Parameters

def main():
    program_args = Parameters.parse_parameters()
    SARC_folder = program_args["sarc_folder"]
    
    for file in os.listdir(SARC_folder):
        future_filename = '/Users/georgiachanning/LA/SARC_tables_csv/' + file[:len(file)-4] + "_tables.csv"
        # edit_name = file[:len(file)-4] + "_tables.txt"
        filename = '/Users/georgiachanning/LA/SARC/' + file
        # if edit_name in os.listdir('/Users/georgiachanning/LA/SARC_tables'):
            # print("passed")
            # continue
        tables = tabula.read_pdf(filename, multiple_tables=True, pages='all')
        print(filename)
        reader = PyPDF2.PdfFileReader(filename)
        if reader.isEncrypted:
            encrypted_files_list = open('encrypted_list.txt',"a+")
            encrypted_files_list.write(filename + '\n')
            encrypted_files_list.close()
            continue
        print(future_filename)
        f = open(future_filename,"w+")
        f.write(str(tables))
        f.close()
    return

if __name__ == "__main__":
    main()