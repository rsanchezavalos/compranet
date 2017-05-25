import os
import json
from flask import Flask, jsonify
from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route("/")
def hello():
	conn = psycopg2.connect("dbname='docker' user='docker' host='dpa_postgres' password='docker'")
	cur = conn.cursor()
	cur.execute("""SELECT * from iris""")
	desc = cur.description
	columns = [column[0] for column in desc]
	results = []
	for row in cur.fetchall():
		results.append(dict(zip(columns, row)))
	return jsonify({'results': str(results)})

if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 5000))
    app.run(host="0.0.0.0", port = port)



