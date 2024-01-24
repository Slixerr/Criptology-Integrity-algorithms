import statistics
import time
from zlib import crc32
import random
import pickle 
import pandas as pd

longitud = 6
caracteres = '0123456789'


def h(input): #Funcion de resumen
    input = bytes(input, encoding='utf-8')
    result = crc32(input)
    return result


def r(value):
    result = str(value % 1000000) #Para que siempre devuelva 6 digitos
    return result


def generateRainbowTable(n, t):
    rainbowTable = {}
    while len(rainbowTable) < n:
        #Password al azar
        pi = ''.join(random.choice(caracteres) for _ in range(longitud)) 
        p = pi

        for j in range(1, t+1):
            p = r(h(p))
        
        rainbowTable[h(p)] = pi

    with open('tablaArcoIris.pkl', 'wb') as f:
        pickle.dump(rainbowTable, f)


def searchColision(table, p0, t):
    p = p0

    for i in range(t):
        if p in table:                                               
            break

        p = h(r(p)) 
    
    if i == t - 1:
        return False
    
    else:
        pwd = table[p]
        i=0
        while (h(pwd) != p0 and i < 5*t):  #en vez de un timeout usar tamaño de la tabla t, experimentacion extendida comparar 
            pwd = r(h(pwd))
            i+=1
            
        if(h(pwd) == p0):
            return [table[p], pwd]

    return [table[p], None] 


realPasswords = ['523824', '941167', '782749', '481939', '736342'] 

def mainArcoIris():
    dfResult= pd.DataFrame()
    columns = 200
    rows = 5000


    for i in range(10):
        print(i)
        times = []
        equalPasswords = []
        colisions = 0
        passwordsGuessed = 0

        generateRainbowTable(rows, columns)
        with open('tablaArcoIris.pkl', 'rb') as f:
            tabla = pickle.load(f)
        
        for passw in realPasswords:
                p0 = h(passw)

                start_time = time.time()
                result = searchColision(tabla, p0, columns)
                total_time = time.time() - start_time

                times.append(total_time)

                if(result != False):
                    colisions+=1
                    if(result[1] != None): 
                        equalPasswords.append((passw, result[1], result[0]))
                        passwordsGuessed += 1

        new_row = {
                    "Filas": rows,
                    "Columnas": rows,
                    "% Colisiones": (colisions/(len(realPasswords)))*100,
                    "% Éxito": (passwordsGuessed / len(realPasswords))*100,
                    "Tiempo Medio Búsqueda": statistics.mean(times),
                    "(Original / Equivalente / Colisión)": equalPasswords
                    }
        dfResult = pd.concat([dfResult, pd.DataFrame([new_row])], ignore_index=True)


    dfResult.to_csv("ArcoIris  Resultado/ArcoIrisResult Numerico.csv", index=False)



mainArcoIris()











