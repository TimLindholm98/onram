
from flask import Flask, jsonify
from flask_mysqldb import MySQL
from json2html import *


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'
mysql = MySQL(app)


@app.route('/data', methods=['POST'])
def add_data():
    cur = mysql.connection.cursor()
    
    hostname = request.json['hostname']
    ip = request.json['ip']
    ipmi = request.json['ipmi']
    ram = request.json['ram']
    threads = request.json['threads']
    nvme = request.json['nvme']
    ssd = request.json['ssd']
    hdd = request.json['hdd']
    
    cur.execute('''INSERT INTO test_suite (hostname, ip, ipmi, ram, threads, nvme, ssd, hdd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', hostname, ip, ipmi, ram, threads, nvme, ssd, hdd
)
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data added successfully'})


@app.route('/data/<string:hostname>', methods=['DELETE'])
def delete_data(hostname):
    cur = mysql.connection.cursor()
    
    cur.execute('''DELETE FROM test_suite WHERE hostname = %s''', (hostname,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data deleted successfully'})


@app.route('/data', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM test_suite''')
    data = cur.fetchall()
    cur.close()
    return json2html.convert(json = data)

if __name__ == '__main__':
    app.run(debug=True)