import requests
from bs4 import BeautifulSoup as bs
import time, json
import random

url = "https://www.pepboys.com/stores"
df = None
mydata = {}

user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/123.0.6312.52 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.80 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko; compatible; BW/1.1; rb.gy/oupwis; a86a9293c9) Chrome/84.0.4147.105 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko; compatible; BW/1.1; rb.gy/oupwis; 337a6f333d) Chrome/84.0.4147.105 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    ]

with open('pepboy_city_store.json', 'r') as f:
    df = json.load(f)

def browse():
    headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    for state in df.keys():
        mydata[state] = []
        for city in df[state]:
            resp = requests.get(city, headers = {'User-Agent':headers}, verify=False)
            if resp.status_code == 200:
                scrape(resp.text, state, city)
            else:
                while resp.status_code != 200:
                    print(f"Errror with header = {headers}")
                    headers = random.choice(user_agent)
                    resp = requests.get(city, headers = headers, verify=False)
                    time.sleep(random.randint(3,6))
                scrape(resp.text, state, city)
            time.sleep(random.randint(1,10))


def scrape(resp, state, city):
    try:
        bobj = bs(resp, 'html.parser')
        data = bobj.select_one('div#mapDataArray').text
        jdata = json.loads(data)
        for row in jdata:
            mapl = "https://www.google.com/maps?cid="+ str(row['cid']) if 'cid' in row.keys() else "https://www.google.com/maps?q="+ row['addressLine1']
            x = [row['Name'], row['storeNumber'], row['Phone'], row['addressLine1']+", "+ row['town']+", "+ row['isoCodeShort']+ " "+ row['postalCode'], row['Lat'], row['Long'], mapl]
            print(x)
            mydata[state].append(x)
            
    except Exception as error:
        print(error)
        print(f"error in {state}, {city}")


try:
    browse()
except Exception as error:
    print(error)
finally:
    with open("pepboys_final_scraped.json", 'w') as f:
        json.dump(mydata, f)
    print("done scraping")
