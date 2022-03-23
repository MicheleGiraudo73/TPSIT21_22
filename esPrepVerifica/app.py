from flask import Flask, render_template, redirect, url_for, request, make_response
from re import U
import threading as thr
from datetime import datetime
import sqlite3
import random
import string
import sympy

app = Flask(__name__)





def validate(username, password):
    completion = False
    conn = None
    try:
        conn = sqlite3.connect('data.db')
    except:
        print("__")
    
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM USERS")
    except:
        print("CIAO")
    rows = cur.fetchall()
    
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password



@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST': #se uguale a GET fa il return della pagina login
        username = request.form['username']
        password = request.form['password']
        
        if validate(username, password): 
            resp = make_response(redirect(url_for('calcolo')))
            resp.set_cookie('username', username)
            print(request.cookies.get('username'))
            return resp
        else:
            error = "Invalid Credentials"
            return render_template('login.html', error=error)
        
    return render_template('login.html', error=error)



@app.route(f'/calcolo', methods=['GET', 'POST'])

def calcolo():
    error = None
    con = None
    con = sqlite3.connect('C:\Michele\Scuola21-22\TPSIT\Flask\esPrepVer2\data.db')
    cur = con.cursor()

    if request.method == 'POST':
        now = datetime.now()
        data_str = now.strftime("%d/%m/%y %H:%M:%S")


        funzione = request.form['funzione']
        basso = request.form['basso']
        alto = request.form['alto']

        if basso == '' and alto == "":
            x = sympy.Symbol('x')
            y = funzione
            soluz = sympy.integrate(y,x)
            print(soluz)
            cur.execute(f"INSERT INTO registro (utente,integrale,soluzione,data) VALUES ('{request.cookies.get('username')}','{y}','{soluz}','{data_str}')")
            cur.execute("commit")
            error = f"{y} = {soluz}"
            
        else:
            x = sympy.Symbol('x')
            y = funzione
            soluz = sympy.integrate(y,(x,basso,alto))
            print(soluz)
            cur.execute(f"INSERT INTO registro (utente,integrale,soluzione,data) VALUES ('{request.cookies.get('username')}','{y}','{soluz}','{data_str}')")
            cur.execute("commit")
            error = f"{y} = {soluz}"
            
    con.close()
    return render_template("calcolo.html",error=error)




if __name__== "__main__":
    app.run(debug=True) 
    
   


