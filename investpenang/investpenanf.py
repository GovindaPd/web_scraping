from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import os

session = HTMLSession()
response = session.get('https://investpenang.gov.my/sme-llc-directory-manufacturing/')
bsobj = BeautifulSoup(response.text, 'html.parser')

for element in bsobj.findAll('div', {'class':'sme_div'}):

    company_name = element.select_one('div div h5').getText()
    support = element.select_one('div div h6').getText()
    address = element.select_one('.address-col li:nth-of-type(2)').getText()
    tel = element.select_one('ul:nth-of-type(2) li:nth-of-type(2)').getText()
    contact_person = element.select_one('ul:nth-of-type(3) li:nth-of-type(2)').getText()
    designation = element.select_one('ul:nth-of-type(4) li:nth-of-type(2)').getText()
    email = element.select_one('ul:nth-of-type(5) li:nth-of-type(2)').getText()
    website = element.select_one('ul:nth-of-type(6) li:nth-of-type(2)').getText()

    mydict['Company_name'] = company_name
    mydict['Support'] = support
    mydict['Address'] = address
    mydict['Tel'] = tel
    mydict['Contact_person'] = contact_person
    mydict['Designation'] = designation
    mydict['Email'] = email
    mydict['Website'] = website
    mylist.append(mydict)
    print(n)
    n += 1
    

with open('investpenang.json', 'w') as myfile:
    json.dump(mylist, myfile)

    
#old url --> https://investpenang.gov.my/sme-directory/
#new url --> https://investpenang.gov.my/sme-llc-directory-manufacturing/
"""
description --> sccrape over 450 SME/LLC Directory (Manufacturing) data from https://investpenang.gov.my
data that are included [Company Name, Support, Address, Telephone, Contact Person, Designation, Email, Website'
in json format.
"""
