from unicodedata import category
from itsdangerous import json
import requests




while(True):
    i = int(input("Inserire 1 (Frase Casuale) 2 (Frase per categoria) 3 (testo a caso) 0 (per chiudere): "))

    if i == 1:
        json = None
        r = requests.get('https://api.chucknorris.io/jokes/random')
        print("\n")
        json= r.json()
        frase = json['value']
        print(frase)
    elif i==2:
        json = None
        r = requests.get('https://api.chucknorris.io/jokes/categories')
        print("\n")
        lista = r.json()
        print("Lista categoria: \n")
        for k in lista:
            print(k)
        print("\n")
        category = input("Inserire categoria: ")
        r2 = requests.get(f'https://api.chucknorris.io/jokes/random?category={category}')
        json=r2.json()
        frase = json['value']
        print(frase)
    elif i==3:
        json=None
        query = input("Inserire parola a caso (Es train): ")
        r = requests.get(f'https://api.chucknorris.io/jokes/search?query={query}')
        json =r.json()
        for k in json['result']:
            print(k['value'])

    elif i== 0:
        break




