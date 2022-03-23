import string
import csv


lista = ""

lista = string.ascii_letters+string.digits


psw_list = []
for let1 in lista:
        for let2 in lista:
            for let3 in lista:
                stri=let1+let2+let3
                psw_list.append(stri)

with open('C:\Michele\Scuola21-22\TPSIT\Flask\Giraudo\psw.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(psw_list)



    

