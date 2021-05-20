# -*- coding: utf-8 -*-
"""
Created on Thu May 20 12:25:44 2021

@author: ltdan
"""

import requests 
from bs4 import BeautifulSoup
import re

URL = "https://supreme.justia.com/justice-ruth-bader-ginsburg-cases/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# The element that contains the page content
# So that it doesn't search nav etc
primary_content = soup.find("div", class_="primary-content")

# The total number of times that rgb mentions the indicated acts
num_opinions = 0

# Search for each link
for link in primary_content.find_all("a", attrs={'href': re.compile("^https://")}):
    
    #URL of link
    link_URL = link.get('href')
    link_page = requests.get(link_URL)
    
    #Search URL
    link_soup = BeautifulSoup(link_page.content, "html.parser")
    
    # The Case title from each link
    case_title = link_soup.find("h1", class_="heading-1")
    
    # Search For Key words / acts
    keywords = re.compile(r"Title VII of the Civil Rights Act|"
                                                      r"Age Discrimination in Employment Act|"
                                                      r"Americans with Disabilities Act|"
                                                      r"42 U.S.C. section 1981|"
                                                      r"Fair Labor Standards Act")
    
    # Find p elements that contain the keyords
    result = link_soup.body.find_all("p", 
                                    text = keywords)

    # If keywords were found, report that link and save to file
    # Remember to erase file if you run the code again
    if (len(result) > 0):
        
        with open("rgb-opinions.txt", "a") as f:
        
            num_opinions = num_opinions + 1

            print("\n", file = f)
            print("link: " + link.get("href"), file = f)
            print(case_title.text, file = f)
            print("Acts:", file = f)
            
            for p in result:
                print(keywords.findall(p.text), file = f)
                
            print(str(len(result)) + " matches", file = f)
            print("\n", file = f)
            

f = open("rgb-opinions.txt", "a")            
print("Total Opinions: " + str(num_opinions), file = f)
f.close()
    