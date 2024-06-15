from requests_html import HTMLSession
from bs4 import BeautifulSoup
#import pandas as pd
#import threading

agency ={}
no = 1
main = "https://www.realestate.com.au"
session = HTMLSession()

def getagents(link):
    global agency
    global no
    agencythings = {}
    url = main+link

    response = session.get(url)
    bsobj = BeautifulSoup(response.txt, 'html.parser')
    totalresults = int(bsobj.find('span', {'class':'sc-etwtAo jKboWG sc-fQejPQ JxEGc'}).getText())

    if totalresults%10 != 0:
        pages = (totalresults//10)+1
    else :
        pages = totalresults//10

    for single in bsobj.select('article.agency-card'):
        agencythings['agency_link'] = single.select('.agency-card__link')[0]['href']
        agencythings['agency_name'] = single.select('.agency-info__name')[0].text
        agencythings['agency_address'] = single.select('.agency-address')[0].text
        agency[no] = agencythings
        no += 1
        
    if pages >1:
        for page in range(2,pages):
            getmoreagents(link,page)


def getmoreagents(link):
    global agency
    global no
    agencythings = {}
    url = main+link+"?page="+str(page)
    response = session.get(url)
    bsobj = BeautifulSoup(response.txt, 'html.parser')
    for single in bsobj.select('article.agency-card'):
        agencythings['agency_link'] = single.select('.agency-card__link')[0]['href']
        agencythings['agency_name'] = single.select('.agency-info__name')[0].text
        agencythings['agency_address'] = single.select('.agency-address')[0].text
        agency[no] = agencythings
        no += 1
    return  None

if name == '__main__':
    getagents("https://www.realestate.com.au/find-agency/sydney-nsw/")

