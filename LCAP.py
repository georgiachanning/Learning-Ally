#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from googlesearch import search 
import requests
# import html5lib
from bs4 import BeautifulSoup
import os
from parameters import Parameters


def import_file(district, url): #this function downloads pdfs found on internet to local computer
    chunk_size = 2000 
    filename = '/Users/georgiachanning/LA/LCAP/' + district + ".pdf" # must be changed to local user
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(filename)
    return

def main():
    
    program_args = Parameters.parse_parameters()
    school_list_file = program_args["lookup_list"] # this is where the list of districts comes from
    
    school_lcap_file_url = {} # dictionary of URLs that link to LCAPs for each school
    could_not_download_from_url = [] # districts for which LCAPs not found
    with open (school_list_file, "r") as f: # reading list of schools
            school_list = f.read().split('\n')
                    
    for school in school_list: # finding LCAP for each school
        query = school + "LCAP" # what the google search is 
        print(school) 
        for j in search(query, tld="co.in", num=10, stop=3, pause=2):  # trying to find best match for LCAP query
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

