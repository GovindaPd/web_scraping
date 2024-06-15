import requests
from bs4 import BeautifulSoup as bs
import json, csv
from random import randint
from requests import exceptions
import pandas as pd

"""
NOTE:
site to scrape is : "https://www.artsy.net/gene/painting"
and data is [image_url, price, artist]

use this in at the end of image url to get image in different sizes

"versions": [
             "square",
             "large_rectangle",
             "medium_rectangle",
             "tall",
             "small",
             "large",
             "larger",
             "normalized",
             "main",
             "medium"
]
"""

with open('scraping project/user_agents/scrapeops_io_complete_headers.csv', 'r') as file:
    ro = csv.DictReader(file)
    user_agent_list = list(ro)

def random_user_agent():
    return user_agent_list[randint(0, len(user_agent_list)-1)]


query = """query CollectionArtworksFilterQuery(
  $input: FilterArtworksInput
  $slug: String!
  $afterCursor: String
) {
  collection: marketingCollection(slug: $slug) {
    ...CollectionArtworksFilter_collection_2VV6jB
    id
  }
}

fragment ArtworkFilterArtworkGrid_filtered_artworks on FilterArtworksConnection {
  id
  pageInfo {
    hasNextPage
    endCursor
  }
  pageCursors {
    ...Pagination_pageCursors
  }
  edges {
    node {
      id
    }
  }
  ...ArtworkGrid_artworks
}

fragment ArtworkGrid_artworks on ArtworkConnectionInterface {
  __isArtworkConnectionInterface: __typename
  edges {
    __typename
    node {
      id
      slug
      href
      internalID
      image(includeAll: false) {
        aspectRatio
      }
      ...GridItem_artwork
      ...FlatGridItem_artwork
    }
    ... on Node {
      __isNode: __typename
      id
    }
  }
}

fragment Badge_artwork on Artwork {
  is_biddable: isBiddable
  href
  sale {
    is_preview: isPreview
    display_timely_at: displayTimelyAt
    id
  }
}

fragment CollectionArtworksFilter_collection_2VV6jB on MarketingCollection {
  slug
  query {
    artistIDs
    id
  }
  filtered_artworks: artworksConnection(input: $input) {
    id
    counts {
      total(format: "0,0")
    }
    ...ArtworkFilterArtworkGrid_filtered_artworks
  }
}

fragment DeprecatedSaveButton_artwork on Artwork {
  id
  internalID
  slug
  isSaved
  title
}

fragment Details_artwork on Artwork {
  internalID
  href
  title
  date
  isUnlisted
  sale_message: saleMessage
  cultural_maker: culturalMaker
  artist {
    targetSupply {
      isP1
    }
    id
  }
  marketPriceInsights {
    demandRank
  }
  artists(shallow: true) {
    id
    href
    name
  }
  collecting_institution: collectingInstitution
  partner(shallow: true) {
    name
    href
    id
  }
  sale {
    endAt
    cascadingEndTimeIntervalMinutes
    extendedBiddingIntervalMinutes
    startAt
    is_auction: isAuction
    is_closed: isClosed
    id
  }
  sale_artwork: saleArtwork {
    lotID
    lotLabel
    endAt
    extendedBiddingEndAt
    formattedEndDateTime
    counts {
      bidder_positions: bidderPositions
    }
    highest_bid: highestBid {
      display
    }
    opening_bid: openingBid {
      display
    }
    id
  }
  ...SaveButton_artwork
  ...SaveArtworkToListsButton_artwork
  ...HoverDetails_artwork
}

fragment FlatGridItem_artwork on Artwork {
  ...Metadata_artwork
  ...DeprecatedSaveButton_artwork
  sale {
    extendedBiddingPeriodMinutes
    extendedBiddingIntervalMinutes
    startAt
    id
  }
  saleArtwork {
    endAt
    extendedBiddingEndAt
    lotID
    id
  }
  internalID
  title
  image_title: imageTitle
  image(includeAll: false) {
    resized(width: 445, version: ["larger", "large"]) {
      src
      srcSet
      width
      height
    }
    blurhashDataURL
  }
  artistNames
  href
  isSaved
}

fragment GridItem_artwork on Artwork {
  internalID
  title
  imageTitle
  image(includeAll: false) {
    internalID
    placeholder
    url(version: ["larger", "large"])
    aspectRatio
    versions
    blurhashDataURL
  }
  artistNames
  href
  ...Metadata_artwork
  ...Badge_artwork
}

fragment HoverDetails_artwork on Artwork {
  internalID
  attributionClass {
    name
    id
  }
  mediumType {
    filterGene {
      name
      id
    }
  }
}

fragment Metadata_artwork on Artwork {
  ...Details_artwork
  internalID
  href
}

fragment Pagination_pageCursors on PageCursors {
  around {
    cursor
    page
    isCurrent
  }
  first {
    cursor
    page
    isCurrent
  }
  last {
    cursor
    page
    isCurrent
  }
  previous {
    cursor
    page
  }
}

fragment SaveArtworkToListsButton_artwork on Artwork {
  id
  internalID
  isSaved
  slug
  title
  date
  artistNames
  preview: image {
    url(version: "square")
  }
  isSavedToList
}

fragment SaveButton_artwork on Artwork {
  id
  internalID
  slug
  isSaved
  title
}

"""


variables = {
  "input": {
    "first": 100,
    "majorPeriods": [],
    "page": 4,
    "sizes": [],
    "sort": "-decayed_merch",
    "artistIDs": [],
    "artistSeriesIDs": [],
    "attributionClass": [],
    "partnerIDs": [],
    "additionalGeneIDs": [],
    "colors": [],
    "locationCities": [],
    "artistNationalities": [],
    "materialsTerms": [],
    "height": "*-*",
    "width": "*-*",
    "priceRange": "*-*"
  },
  "slug": "painting",
  "afterCursor": "")
}

#US/Eastern
#'Asia/Calcutta'
headers ={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
          'accept': '*/',
          'sec-ch-ua': 'Google Chrome;v="89", "Chromium";v="89", ";Not A Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': 'macOS',
          'sec-fetch-site': 'same-site',
          'sec-fetch-mod': 'cors',
          'sec-fetch-user': '?1',
          'accept-encoding': 'gzip',
          'accept-language': 'en-US',
          'X-Original-Session-Id': "feaeb840-fad7-11ee-b9bd-5175c84317c5",
          'X-Timezone': 'US/Eastern',
          'Origin': 'https://www.artsy.net',
          'referer': 'https://www.artsy.net/',
          'Sec-Fetch-Dest': 'empty',
          'authority': 'metaphysics-production.artsy.net',
          'method': 'POST',
          'path': '/v2',
          'scheme': 'https',
          'Content-Type': 'application/json'
          
          }
def change_require_header(headers):
    user_aget = random_user_agent()
    
    headers['user-agent'] = user_agent['user-agent']
    headers['sec-ch-ua'] = user_agent['sec-ch-ua']
    headers['sec-ch-ua-mobile'] = user_agent['sec-ch-ua-mobile']
    headers['sec-ch-ua-platform'] = user_agent['sec-ch-ua-platform']
    


#file writeing code
file = open("images_data5.csv", 'a', newline="", encoding='utf-8')
wo = csv.writer(file)

df = pd.read_csv("images_data3.csv", encoding='utf-8')

def crawl():
    
    for page in range(4,5):
        #variables['page'] = i
        json_data = {
            'id':'CollectionArtworksFilterQuery',
            'query':query,
            'variables':variables,
            }
        
        try:
            result = requests.post("https://metaphysics-production.artsy.net/v2",
            headers=headers, json=json_data, timeout=10)
        except exceptions as ex:
            print(ex)

        if result.status_code == 200:
            data = result.json()
            try:
                print(len(data['data']['collection']['filtered_artworks']['edges']))
            except:
                print(data)
                return None

            if data['data']['collection']['filtered_artworks']['edges'] != None:
                for i in data['data']['collection']['filtered_artworks']['edges']:
                    try:
                        url = i['node']['image']['url'] if i['node']['image']['url'] != None else ''
                        price = i['node']['sale_message'] if i['node']['sale_message'] != None else ''
                        artist = i['node']['artistNames'] if i['node']['artistNames'] != None else ''
                        message = i['node']['title'] if i['node']['title'] != None else ''
                        date = i['node']['date'] if i['node']['date'] != None else ''
                        if url not in df['url'].values:
                            x = wo.writerow((url, price,artist,message ,date))
                        else:
                            print("already present")
                    except:
                        print("error in writing")
                        continue
            else:
                print(result.text)
        else:
            print(f"status code error {result.status_code}")
        

if __name__=='__main__':
    try:
        crawl()
    except Exception as error:
        print(error)
    finally:
        file.close()


"""
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False)
    

PROXY = "88.157.149.250:8080" # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={PROXY}")

chrome = webdriver.Chrome(chrome_options=chrome_options)
chrome.get("http://google.com")


# //a[starts-with(@href, 'https://www.amazon.com/')]/@href
LINKS_XPATH = '//*[contains(@id,"result")]/div/div[3]/div[1]/a'
browser = webdriver.Chrome(executable_path="C:\\Users\Andrei\Downloads\chromedriver_win32\chromedriver.exe",
                           chrome_options=chrome_options)
"""
