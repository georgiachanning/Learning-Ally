#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from googlesearch import search 
import requests
# import html5lib
from bs4 import BeautifulSoup
import os

school_list_file = "/Users/georgiachanning/LA/districts_to_focus_on.txt"

def import_file(district, url):
    chunk_size = 2000
    filename = '/Users/georgiachanning/LA/LCAP/' + district + ".pdf"
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(filename)
    return

def main():
    school_lcap_file_url = {}
    could_not_download_from_url = []
    with open (school_list_file, "r") as f:
            school_list = f.read().split('\n')
                    
    for school in school_list:
        query = school + "LCAP"
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
                if "Annual Update" in str(link):
                    school_lcap_file_url[school] = link['href']
                elif "Local Control Accountability Plan" in str(link):
                    school_lcap_file_url[school] = link['href']
                elif "Final" in str(link):
                    school_lcap_file_url[school] = link['href']
                elif "2019" in str(link):
                    school_lcap_file_url[school] = link['href']
            if school in school_lcap_file_url:
                try:
                    print(school_lcap_file_url[school])
                    import_file(school, school_lcap_file_url[school])
                except:
                    could_not_download_from_url.append(school)
                break
    with open("url_dict.txt", "w") as f:
        for key, value in school_lcap_file_url.items():
            f.write('%s:%s\n' % (key, value))
        
    return
        
    
if __name__ == '__main__':
    main() 

