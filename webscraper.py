#!/usr/bin/env python

# Author: Amy Nguyen
# Python Web Scraper
# This program scrapes a weblink and returns the HTML code for the weblink as a text file. 
# It also returns a CSV file of the unique URIs located on the webpage. 

from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse

# scrape() pulls the html code from a URL and puts it into a beautiful soup object called soup. 
def scrape(url_to_scrape): 

    request_page = urlopen(url_to_scrape)
    page_html = request_page.read()
    request_page.close()

    soup = BeautifulSoup(page_html, 'html.parser')
    
    print("The url was successfully scraped.")
    return soup
    

# Using the soup object from scrape(), export_HTML() writes out a formatted version of the HTML code into a text file.
def export_HTML(soup):
    
    success = False
    
    try: 
        soup_tree = soup.prettify()
        file = open("html_code.txt", 'w', encoding='utf-8')

        file.write(soup_tree)
        file.close()
        print("A text file of the html code was successfully created.")
        
        success = True

    except ValueError:
        print("HTML Tree File was not successfully created." + ValueError)
        success = False
    
    return success

# Using the soup object returned by scrape() the extract_uniqueURIs method pulls out all of the absolute and relative weblinks from the HTML code into a list.
# From there it checks for duplicates by converting the list of URIs into a set of URIs.
# Lastly, the set of URIs is sorted for readibility reason and then returned as uri_sorted
def extract_uniqueURIs(soup): 
    
    # Pulling URIs from given URL and putting them in a list
    uri_list = []
    base = 'https://www.census.gov'
    
    for url in soup.find_all('a'):
        data = str(url.get('href'))

        if "http" in data:
            uri_list.append(data)
        elif "None" not in data and "#" not in data:
            uri_list.append(urllib.parse.urljoin(base, data))

    
    # Removing duplicates by converting the URI list into a set
    uri_set = list(set(uri_list))

    # Sort duplicate free uri_set
    uri_sorted = sorted(uri_set)

    print("A list of the unique URIs was successfully created.")
    return uri_sorted

# The export_CSV() method takes the set of URL links and writes it out into a CSV file. 
def export_CSV(uri_set):
    
    success = False
    
    try:
        file = open("unique_URIs.csv", 'w')
        
        clean_URISet = str(uri_set)[1:-1]
        clean_URISet = clean_URISet.replace("'","")
    
        file.write(clean_URISet)
        
        print("A CSV file of the unique URIs was successfully created.")
        success = True

    except ValueError:
        print("CSV of unique URIs was not created." + ValueError)

        success = False
    
    return success
    

def main():
   
    soup = scrape("https://www.census.gov/programs-surveys/popest.html")
    
    export_HTML(soup)

    extracted_URIs = extract_uniqueURIs(soup)
    export_CSV(extracted_URIs)

if __name__ == "__main__":
    main()
