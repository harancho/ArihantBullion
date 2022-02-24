from itertools import count
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request
import sqlite3 as lite
import os,os.path

app = Flask(__name__)

count = 0
gold_dalali = 1400
silver_dalali = 1400
gold_local_dalali = 1200
silver_kacchi_dalali = 1200

con = lite.connect('site.db')
with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS dalalis(id INTEGER PRIMARY KEY, gold_dalali INTEGER , silver_dalali INTEGER, gold_local_dalali INTEGER, silver_kacchi_dalali INTEGER)")
	cur.execute("INSERT INTO dalalis (gold_dalali,silver_dalali,gold_local_dalali,silver_kacchi_dalali) VALUES (?,?,?,?)",(gold_dalali,silver_dalali,gold_local_dalali,silver_kacchi_dalali))


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
        cur.execute("DROP TABLE IF EXISTS dalalis")
        cur.execute("CREATE TABLE IF NOT EXISTS dalalis(id INTEGER PRIMARY KEY, gold_dalali INTEGER , silver_dalali INTEGER, gold_local_dalali INTEGER, silver_kacchi_dalali INTEGER)")
        cur.execute("INSERT INTO dalalis (gold_dalali,silver_dalali,gold_local_dalali,silver_kacchi_dalali) VALUES (?,?,?,?)",(gold_dalali_new,silver_dalali_new,gold_local_dalali_new,silver_kacchi_dalali_new))

    return jsonify(result = "Done")

  return jsonify(result="Done")

@app.route("/")
def home():
  # gold_dalali = int(request.form['gold_dalali'])
  # gold_local_dalali = int(request.form['gold_local_dalali'])
  # silver_dalali = int(request.form['silver_dalali'])
  # silver_kacchi_dalali = int(request.form['silver_kacchi_dalali'])
  global count
  count+=1
  print(count)
  print("Request received")
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
    cur.execute("SELECT * FROM dalalis ORDER BY ROWID ASC LIMIT 1")
    row = cur.fetchall()
    print(row)
    gold_dalali_new = row[0][1]
    silver_dalali_new = row[0][2]
    gold_local_dalali_new = row[0][3]
    silver_kacchi_dalali_new = row[0][4]

  return jsonify(gold_total = gold + gold_dalali_new, silver_total = silver + silver_dalali_new, gold_local_total = gold + gold_local_dalali_new, silver_kacchi_total = silver + silver_kacchi_dalali_new, gold = gold , silver = silver, gold_badla = gold_dalali_new, gold_local_badla = gold_local_dalali_new, silver_badla = silver_dalali_new, silver_kacchi_badla = silver_kacchi_dalali_new)

if __name__ == '__main__':
    app.run(debug=True)

# def run():
#     app.run(host='0.0.0.0', port=5000)


# t = Thread(target=run)
# t.start()