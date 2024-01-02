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

#
# ToDo
#
#   1. Change all cur.execute to use the variables "statement" and "values"
#  
#


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
    power_state = request.json['power_state']
    date_time = request.json['date_time']
    # https://stackoverflow.com/questions/69887741/execute-takes-2-positional-arguments-but-3-were-given-for-db-execute-flask-p
    values = (hostname, ip, ipmi, cpu, threads, ram, ram_sticks, nvme, ssd, hdd, power_state, date_time)
    statement = "INSERT INTO test_suite (hostname, ip, ipmi, cpu, threads, ram, ram_sticks, nvme, ssd, hdd, power_state, date_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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

# Power State
@app.route('/data/power_state/<string:hostname>', methods=['GET'])
def get_power_state_by_hostname(hostname):
    statement = 'SELECT power_state FROM test_suite WHERE hostname = %s'
    cur = mysql.connection.cursor()
    cur.execute( statement, (hostname,))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/data/power_state/<string:hostname>', methods=['PUT'])
def change_power_state_by_hostname(hostname):
    power_state = request.json['power_state']
    date_time = request.json['date_time']
    values = (power_state, date_time, hostname)
    statement = 'UPDATE test_suite SET power_state = %s, date_time = %s WHERE hostname = %s'
    cur = mysql.connection.cursor()
    cur.execute( statement, values)
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Power state changed successfully'})

# Auto cleaning / housekeeping
@app.route('/data/housekeeping', methods=['GET'])
def get_housekeeping():
    statement = 'SELECT * FROM test_suite WHERE date_time >= (curdate() - 5) AND power_state = "down"'
    cur = mysql.connection.cursor()
    cur.execute( statement, )
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

# Removing
@app.route('/data/housekeeping', methods=['DELETE'])
def delete_housekeeping():
    # statement = 'DELETE FROM test_suite WHERE date_time >= (curdate() - 7)'
    # cur = mysql.connection.cursor()
    # cur.execute( statement, )
    # data = cur.fetchall()
    # cur.close()
    # return jsonify(data)

    statement = 'DELETE FROM test_suite WHERE date_time = (curdate() - 5) AND power_state = "down"'
    cur = mysql.connection.cursor()
    cur.execute( statement, )
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Housekeeper deleted data successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)