from cmath import inf
import time
import requests
from bs4 import BeautifulSoup

def send_messageS():
    page1 = requests.get("https://www.moneycontrol.com/commodity/silver-price.html#04mar2022")
    page2 = requests.get("https://www.moneycontrol.com/commodity/gold-price.html#05apr2022")

    Soup = BeautifulSoup(page1.content, 'html.parser')
    info = Soup.find_all(class_ = "gqtcont")
    # for items in info:
    #     print(items)
    silver = info[0].get_text().splitlines()[8][:5]
    print(int(silver))

    Soup = BeautifulSoup(page2.content, 'html.parser')
    info = Soup.find_all(class_="gqtcont")
    gold = info[0].get_text().splitlines()[8][:5]
    print(int(gold))

while True:
    send_messageS()
    time.sleep(5)