from flask import Flask, render_template, redirect, url_for, request
import threading as thr
import time
app = Flask(__name__)
import sqlite3
import random
import string
import socket

def portaAperte(ind):
    ip, portMin, portMax = ind.split(',')
    for port in range(int(portMin),int(portMax)+1):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip,port)) #se 0 porta aperta se result > 0 -> chiusa (cod 10035)
        print(result)
        print(f"{ip},{port}")
        if result > 0:
            result=1
        insert(ip,port,result)
        sock.close()

def insert(ind, porta, active ):
    conn=None
    conn = sqlite3.connect('C:\Michele\Scuola21-22\TPSIT\Flask\provaVer\simplewebapp\db.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO INDIRIZZI (Indirizzo,Porta,Attivo) VALUES ('{ind}','{porta}','{active}')")
    cur.execute("commit")
    conn.close()

@app.route(f'/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        if(request.form['IPp']!=''):  #gestico l'inserimento come una unica striga (ip,portMin,portMax)
            portaAperte(request.form['IPp'])
    elif request.method == 'GET':
        return render_template('index.html')
    msg="FINITO"
    return render_template("index.html",msg=msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')