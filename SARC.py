#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from googlesearch import search 
import requests
# import html5lib
from bs4 import BeautifulSoup
from parameters import Parameters


def import_file(school, url):
    chunk_size = 2000
    filename = '/Users/georgiachanning/LA/SARC/' + school + ".pdf"
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(filename)
    return

def main():
    
    program_args = Parameters.parse_parameters()
    school_list_file = program_args["lookup_list"]
    
    school_sarc_file_url = {}
    could_not_download_from_url = []
    with open (school_list_file, "r") as f:
            school_list = f.read().split('\n')
                    
    for school in school_list:
        query = school + "SARC"
        print(school)
        for j in search(query, tld="co.in", num=10, stop=3, pause=2): 
            try:
                r = requests.get(j)
            except:
                continue
            soup = BeautifulSoup(r.content, 'html.parser')
            for link in soup.select("a[href$='.pdf']"):
                if "Spanish" in str(link):
                    continue
                if "Español" in str(link):
                    continue
                if "Espanol" in str(link):
                    continue
                if "Template" in str(link):
                    continue
                if "School Accountability Report Card" in str(link):
                    school_sarc_file_url[school] = link['href']
                elif "SARC" in str(link):
                    school_sarc_file_url[school] = link['href']
                elif "Report" in str(link):
                    school_sarc_file_url[school] = link['href']
                elif "2019" in str(link):
                    school_sarc_file_url[school] = link['href']
            if school in school_sarc_file_url:
                try:
                    print(school_sarc_file_url[school])
                    import_file(school, school_sarc_file_url[school])
                except:
                    could_not_download_from_url.append(school)
                break
    with open("url_dict.txt", "w") as f:
        for key, value in school_sarc_file_url.items():
            f.write('%s:%s\n' % (key, value))
        
    return
        
    
if __name__ == '__main__':
    main() 
