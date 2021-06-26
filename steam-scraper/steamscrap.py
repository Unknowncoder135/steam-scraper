import json
import re
from sys import version
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup, SoupStrainer

url ='https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1'


def count_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return int(data['total_count'])
    # return int(mylenth)



def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

# print(get_data(url))
def parsing_data(data):
    my_list = []
    soup = BeautifulSoup(data,'html.parser')
    games = soup.find_all('a')
    for x in games:
        name = x.find('span',class_='title').text
        old_price  = x.find('div',class_='search_price').text.strip().split('₹')[1]
        try:
            discount_price= x.find('div',class_='search_price').text.strip().split('₹')[2]
        except:
            discount_price = 'no discount available'
        try:
            discount_percentage=x.find('div',class_='col search_discount responsive_secondrow').text.strip()
            # print(name,old_price,discount_price)
        except:
            discount_percentage = 'no discount available'
        my_game_data = {
            'game_name':name,
            'game_old_price':old_price,
            'disxount_price':discount_price,
            'discount_percentage':discount_percentage
        }
        my_list.append(my_game_data)
    return my_list


def panda_min(my_result):
    games = pd.concat([pd.DataFrame(g) for g in my_result])
    games.to_csv('main_result.csv',index=False)
    return 

my_result = []
for x in range(0,800,50):
    # print(x)
    dd =    get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&tags=19&infinite=1')
    my_result.append(parsing_data(dd))
    print(f'printing page {x}....')
    time.sleep(1.5)
panda_min(my_result)
print('misiion complated')








