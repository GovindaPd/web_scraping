"""
description --> scrape around 5,000 german school list of data [School name/Authority Name, Address, Email address, phone/Telephone] from 
https://km-bw.de/Schuladressdatenbank using requests library in csv format

from this url
https://lobw.kultus-bw.de/didsuche/DienststellenSucheWebService.asmx/SearchDienststellen
scrape data are [School name/Authority Name, Address, Email address, phone/Telephone]
"""
import time
import requests
import csv
from random import randint

error_urls = []

def scrape(start_urls):
    for i in reader:
        data = {'disch': "0" + str(i[0])}
        try:
            res = requests.post('https://lobw.kultus-bw.de/didsuche/DienststellenSucheWebService.asmx/GetDienststelle',\
                json=data)\.json()
            time.sleep(randint(0,5))
        except Ex:
            error_urls.append(i)
            print("program goes to sleep mode for 5 seconds for your bad handshake")
            time.sleep(5)

        li = res['d'].replace('null','None')
        s= eval(li)
        #The eval() function evaluates the specified (string) expression, if the expression is a legal Python statement, it will be executed.
        #like above eval(li) will  evaluate sting to a dictionary format cause above li string is valid dict expression in string format

        address = s['DISTR']+' '+ s['PLZSTR']+' '+ s['DIORT']
        address = address.replace('  ',' ')

        try:
            writerobj.writerow([s['NAME'],address,s['VERWEMAIL'],s['TELGANZ']])
        except Exception as error:
            print("error writing in file")
            print(s)
        
if name == '__main__':
    
    rf = open('nnn.csv', 'r')
    reader = csv.reader(rf)
    rf.close()
    
    wf = open('germanschool.csv', 'a', newline='')
    writerobj = csv.writer(wf)
    
    writerobj.writerow(['Name','Address','Email','Phone'])
    
    scrape(reader)
    print(f"{error_urls=}")
    
    wf.close()
