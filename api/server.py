#!/usr/bin/python

from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask import request
from json2html import *


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'S3cret'
app.config['MYSQL_DB'] = 'onram'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/data', methods=['POST'])
def add_data():
    cur = mysql.connection.cursor()
    # To fix this make a bigger variable (?)
    hostname = request.json['hostname']
    ip = request.json['ip']
    ipmi = request.json['ipmi']
    cpu = request.json['cpu']
    ram = request.json['ram']
    ram_sticks = request.json['ram_sticks']
    threads = request.json['threads']
    nvme = request.json['nvme']
    ssd = request.json['ssd']
    hdd = request.json['hdd']
    start_time = request.json['start_time']
    # https://stackoverflow.com/questions/69887741/execute-takes-2-positional-arguments-but-3-were-given-for-db-execute-flask-p
    values = (hostname, ip, ipmi, cpu, threads, ram, ram_sticks, nvme, ssd, hdd, start_time)
    statement = "INSERT INTO test_suite (hostname, ip, ipmi, cpu, threads, ram, ram_sticks, nvme, ssd, hdd, start_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute( statement, values )
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data added successfully'})


@app.route('/data/<string:hostname>', methods=['DELETE'])
def delete_data_by_hostname(hostname):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM test_suite WHERE hostname = %s''', (hostname,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data deleted successfully'})


@app.route('/', methods=['GET'])
def get_root():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM test_suite''')
    data = cur.fetchall()
    cur.close()
    return json2html.convert(json = data)
    
@app.route('/data', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM test_suite''')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)
    
@app.route('/data/<string:hostname>', methods=['GET'])
def get_data_by_hostname(hostname):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM test_suite WHERE hostname = %s''', (hostname,))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)