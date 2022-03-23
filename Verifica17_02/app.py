import semaforo
from flask import Flask
import time
from flask import Flask, render_template, redirect, url_for, request, make_response
from re import U
import threading as thr
from datetime import datetime
import sqlite3
import random
import string
import sympy

app = Flask(__name__)

s = semaforo.semaforo()
STATO = "ATTIVO" #"SPENTO"

#USERNAME E PASSWORD : u: Ciao p:123  u:Homer p:Ciambella

#funzione validate per confrontare la password inserita nella pagina con quella nel database
def validate(username, password):
    completion = False
    conn = None
    try:
        conn = sqlite3.connect('datas.db')
    except:
        print("__")
    
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users") #prendo tutte le righe dal db nel caso non funzioni stampa CIAO
    except:
        print("CIAO")
    rows = cur.fetchall() #fetchall per prendere le righe
    
    for row in rows: #scorro la lista con username e password del db (in indice 0 nome user, indice 1 password)
        dbUser = row[0]
        dbPass = row[1]
        
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion
#uso una funzione check per confrontare le password
def check_password(hashed_password, user_password):
    return hashed_password == user_password

#Pagina di login con metodi get e post, due campi text e un bottone per fare il login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST': #se uguale a GET fa il return della pagina login
        username = request.form['username'] #prendo i campi text dall'html
        password = request.form['password']
        #controllo username e password e setto il cookie all'utente che mi servirà dopo
        if validate(username, password): 
            resp = make_response(redirect(url_for('test')))
            resp.set_cookie('username', username)
            print(request.cookies.get('username'))
            return resp
        else:
            #se le credenziali non sono valide stampa a video error
            error = "Invalid Credentials"
            return render_template('login.html', error=error)
        
    return render_template('login.html', error=error)


#Pagina dove si cambiamo i valori del semaforo
@app.route('/test',methods=['GET', 'POST'])
def test():
    #mi collego al db
    error = None
    con = None
    con= sqlite3.connect('datas.db')
    cur = con.cursor()
        
    #controllo se il metodo è post, nel form setto Post in modo da entrare in questa if
    if request.method == 'POST':
        STATO = "ATTIVO"
        #prendo i campi dei secondi
        secVerde = request.form['V']
        secGiallo = request.form['G']
        secRosso = request.form['R']
        
        

        #controllo se i tasti attiva e disattiva vengono premuti, se premuti faccio la query per salvare chi ha premuto il tasto
        #tramite cookie (request), lo STATO e la data e l'ora
        if request.form.get('Disattiva'):
                STATO = "DISATTIVO"
                now = datetime.now()
                data_str = now.strftime("%d/%m/%y %H:%M:%S")
                cur.execute(f"INSERT INTO operazioni (username,op,dataOra) VALUES ('{request.cookies.get('username')}','{STATO}','{data_str}')")
                cur.execute("commit")
                
        if request.form.get('Attiva'):

                STATO ="ATTIVO"
                now = datetime.now()
                data_str = now.strftime("%d/%m/%y %H:%M:%S")
                cur.execute(f"INSERT INTO operazioni (username,op,dataOra) VALUES ('{request.cookies.get('username')}','{STATO}','{data_str}')")
                cur.execute("commit")
        #Se lo stato è attivo faccio i controlli sui campi, in base a quelli vuoti decido quali valori assegnare alle luci, scelte casuali
        if STATO == "ATTIVO":
            if secVerde == "" and secRosso == "" and secGiallo == "":

            #Esempio di sequenza con semaforo attivo. I tempi devono essere
            #modificabili dalla pagina di configurazione!
                s.rosso(2)
                s.verde(3)
                s.giallo(1)
                
            else:
                if secVerde != "" and secRosso == "" and secGiallo == "":
                    s.rosso(1)
                    s.verde(int(secVerde))
                    s.giallo(1)
                if secVerde == "" and secRosso != "" and secGiallo == "":
                    s.rosso(int(secRosso))
                    s.verde(1)
                    s.giallo(1)
                if secVerde == "" and secRosso == "" and secGiallo != "":
                    s.rosso(1)
                    s.verde(1)
                    s.giallo(int(secGiallo))
                if secVerde != "" and secRosso != "" and secGiallo != "":
                    s.rosso(int(secRosso))
                    s.verde(int(secVerde))
                    s.giallo(int(secGiallo))
            #se il semaforo è disattivo fa partire la luce gialla e poi spegne tutto
        else:
            #Esempio di sequenza con semaforo spento. I tempi devono essere
            #modificabili dalla pagina di configurazione!
            s.giallo(1)
            s.luci_spente(1)
            

    #chiudo il DB
    con.close()  
    return render_template('test.html',error=error)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
    
   


