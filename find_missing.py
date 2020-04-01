#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from parameters import Parameters

def main():
    SARC_folder = '/Users/georgiachanning/LA/SARC/'
    list_of_cds_codes = []
    count = 0
    
    with open("/Users/georgiachanning/LA/all_elementary_cds_codes.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            code = line.rstrip()
            list_of_cds_codes.append(code)
        
    with open("/Users/georgiachanning/LA/missing_cds.txt", "a+") as f:
        for cds in list_of_cds_codes:
            would_be_file = SARC_folder + cds + ".pdf"
            if not path.exists(would_be_file):
                count += 1
                f.write(cds + '\n')
    return

if __name__ == '__main__':
    main()
    
