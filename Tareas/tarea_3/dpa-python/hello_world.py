# coding: utf-8
import random
import os
import json
import psycopg2
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def hello():
	try:
	    conn = psycopg2.connect("dbname='docker' user='docker' host='dpa_postgres' password='docker'")
	except:
	    print("I am unable to connect to the database.")

	try:
		cur = conn.cursor()
		cur.execute("""SELECT * from iris""")
		rows = cur.fetchall()
	except:
	    print("I can't SELECT from iris")

	return jsonify({ "row al azar": str(rows[random.randint(1,150)])})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port = "8090")