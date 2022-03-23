from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import numpy as np
import socket as sck
app = Flask(__name__)

port_sname={}

def dictReader(d):
    string="Service Name   |   Port Number<br>"
    for k in d.keys():
        string+=f"{d[k]}   |   {k}<br>"
    return string

def scanner(ip,portMin,portMax):
    s=sck.socket(sck.AF_INET,sck.SOCK_STREAM)
    for i in range(portMin,portMax+1,1):
        portValue = s.connect_ex((ip,i))
        con = None
        con = sqlite3.connect("TPSIT\Flask\provaVer2\db.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO PORTE (Ip,Port,Attivo) VALUES ('{ip}','{i}','{portValue}')")
        
        cur.execute("commit")
        if portValue!=0:
            cur.execute(f"SELECT ServiceName FROM snpn WHERE PortNumber='{i}'")
            sname = cur.fetchall()[0][0]
            port_sname[i]=sname
        con.close()

    s.close()
    
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ip = request.form['ip']
        portMin = int(request.form['portMin'])
        portMax = int(request.form['portMax'])
        ip_nmbrs=np.array(list(map(int, ip.split("."))))
        if (ip_nmbrs<=255).all() and (ip_nmbrs>=0).all():
            if portMin > 0 and portMin < portMax and portMax < 65535:
                scanner(ip,portMin,portMax)
                return redirect(url_for('port_scanner'))
                #error="Port scan concluded"
            else:
                error="wrong ports"
        else:
            error="wrong ip"
    return render_template('ip_form.html', error=error)

@app.route('/port_scan')
def port_scanner():
    return dictReader(port_sname)

if __name__== "__main__":
    app.run(debug=True)