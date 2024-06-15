import requests_html
import json, csv
from random import randint

#scrape using  website

with open('scraping project/user_agents/scrapeops_io_complete_headers.csv', 'r') as file:
    ro = csv.DictReader(file)
    user_agent_list = list(ro)

def random_user_agent():
    return user_agent_list[randint(0, len(user_agent_list)-1)]

file = open("artsy.csv","a", newline="")
wo = csv.writer(file)

"""def scrape(i = 1, url=None):
    r =None
    if i<=3 and url is not None:
        try:
            r = requests_html.requests.get(url, headers=random_user_agent(), timeout=10)
            return r
        except requests.exceptions.TimeoutError:
            print("time out error")
            return scrape(i+1, url)
        except requests.exceptions as req_exp:
            print(f"Requestst exceptions {req_exp}")
            return scrape(i+1, url)
        except Exception as error:
            print(f"global exception {error}")
            return scrape(i+1, url)
    else:
        print("max try retch")
    return r
"""
s = requests_html.HTMLSession()
s.headers =random_user_agent()

try:
    for i in range(1,101,1):
        try:
            #,headers=random_user_agent()
            result = s.get(f"https://www.artsy.net/collection/painting?page={i}" ,timeout=10)
        except Exception as err:
            print(f"error in page {i}")
            continue
            
        if result.status_code ==200:
            rows = result.html.xpath("//div[@data-test='artworkGrid']//div[@data-test='artworkGridItem']")
            for r in rows[0:30]:
                x =(
                r.xpath("//div[@data-test='artworkGridItem']//img/@src")[0],
                r.xpath("//a/div/div[@color='black100']/text()")[0],
                r.xpath("//a/div/div/div/span/text()")[0]
                )
                try:
                    _ = wo.writerow(x)
                    print(x)
                except:
                    print("error in writing")
            print(f"{i} page scraped")

        else:
            print(f"there is an error in {i} page")

except:
    print("error")
finally:
    file.close()
    



