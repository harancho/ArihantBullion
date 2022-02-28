import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request
import sqlite3 as lite
import os,os.path
from threading import Thread
import time

app = Flask(__name__)

gold_dalali = 1400
silver_dalali = 1400
gold_local_dalali = 1200
silver_kacchi_dalali = 1200
silver = 60000
gold = 50000

# con = lite.connect('site.db')
# with con:
# 	cur = con.cursor()
# 	cur.execute("CREATE TABLE IF NOT EXISTS dalalis(id INTEGER PRIMARY KEY, gold_dalali INTEGER , silver_dalali INTEGER, gold_local_dalali INTEGER, silver_kacchi_dalali INTEGER)")
# 	cur.execute("INSERT INTO dalalis (gold_dalali,silver_dalali,gold_local_dalali,silver_kacchi_dalali) VALUES (?,?,?,?) ",(gold_dalali,silver_dalali,gold_local_dalali,silver_kacchi_dalali))
# 	cur.execute("CREATE TABLE IF NOT EXISTS prices(id INTEGER PRIMARY KEY, gold_price INTEGER , silver_price INTEGER)")
# 	cur.execute("INSERT INTO prices (gold_price,silver_price) VALUES (?,?)",(gold,silver))

@app.route("/changeBadla", methods = ['GET','POST'])
def changeBadla():
  if request.method == "POST":
    gold_dalali_new = int(request.form['gold_badla'])
    gold_local_dalali_new = int(request.form['gold_local_badla'])
    silver_dalali_new = int(request.form['silver_badla'])
    silver_kacchi_dalali_new = int(request.form['silver_kacchi_badla'])

    con = lite.connect('site.db')
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM dalalis")
        # cur.execute("CREATE TABLE IF NOT EXISTS dalalis(id INTEGER PRIMARY KEY, gold_dalali INTEGER , silver_dalali INTEGER, gold_local_dalali INTEGER, silver_kacchi_dalali INTEGER)")
        cur.execute("INSERT INTO dalalis (gold_dalali,silver_dalali,gold_local_dalali,silver_kacchi_dalali) VALUES (?,?,?,?)",(gold_dalali_new,silver_dalali_new,gold_local_dalali_new,silver_kacchi_dalali_new))

    return jsonify(result = "Done")

  return "Done"

def get_prices():
    while True:
        page1 = requests.get("https://www.moneycontrol.com/commodity/silver-price.html#04mar2022")
        page2 = requests.get("https://www.moneycontrol.com/commodity/gold-price.html#05apr2022")

        Soup = BeautifulSoup(page1.content, 'html.parser')
        info = Soup.find_all(class_ = "gqtcont")
        silver = int(info[0].get_text().splitlines()[8][:5])
        print(silver)

        Soup = BeautifulSoup(page2.content, 'html.parser')
        info = Soup.find_all(class_="gqtcont")
        gold = int(info[0].get_text().splitlines()[8][:5])
        print(gold)

        con = lite.connect('site.db')
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM prices")
            cur.execute("INSERT INTO prices (gold_price,silver_price) VALUES (?,?)",(gold, silver))


        time.sleep(20)


@app.route("/")
def home():
    con = lite.connect('site.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM dalalis ORDER BY ROWID ASC LIMIT 1")
        row = cur.fetchall()
        print(row)
        gold_dalali_new = row[0][1]
        silver_dalali_new = row[0][2]
        gold_local_dalali_new = row[0][3]
        silver_kacchi_dalali_new = row[0][4]
        cur.execute("SELECT * FROM prices ORDER BY ROWID ASC LIMIT 1")
        row = cur.fetchall()
        print(row)
        gold_new = row[0][1]
        silver_new = row[0][2]
        
        return jsonify(gold_total = gold_new + gold_dalali_new, silver_total = silver_new + silver_dalali_new, gold_local_total = gold_new + gold_local_dalali_new, silver_kacchi_total = silver_new + silver_kacchi_dalali_new, gold = gold_new , silver = silver_new, gold_badla = gold_dalali_new, gold_local_badla = gold_local_dalali_new, silver_badla = silver_dalali_new, silver_kacchi_badla = silver_kacchi_dalali_new)

x = threading.Thread(target=get_prices)

# if __name__ == '__main__':
#     x.start()
#     app.run()

def run():
    x.start()
    app.run()


t = Thread(target=run)
t.start()