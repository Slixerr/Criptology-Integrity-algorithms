import statistics
import time
from zlib import crc32
import random
import pickle 
import pandas as pd

caracteres = 'abcdefghijklmnopqrstuvwxyz'
longitud = 5

def h(input): #Funcion de resumen
    input = bytes(input, encoding='utf-8')
    result = crc32(input)
    return result

def r(value, index): 
    binaryResult = bin(value)[2:].zfill(32)

    #TRANSFORMAR BITS EN CARACTERES LEGIBLES
    letra1 = caracteres[int(binaryResult[0:6], 2)       %   len(caracteres)]
    letra2 = caracteres[int(binaryResult[6:12], 2)      %   len(caracteres)]
    letra3 = caracteres[int(binaryResult[12:18], 2)     %   len(caracteres)]
    letra4 = caracteres[int(binaryResult[18:24], 2)     %   len(caracteres)]
    letra5 = caracteres[int(binaryResult[24:32], 2)     %   len(caracteres)]

    result = letra5 + letra4 + letra3 + letra2 + letra1

    indexCaracteres = index % 5
    result = result[(indexCaracteres):] + result[:indexCaracteres]
    return result

def generateRainbowTable(n, t):
    rainbowTable = {}
    while len(rainbowTable) < n:
        #Password al azar
        pi = ''.join(random.choice(caracteres) for _ in range(longitud)) 
        p = pi

        for j in range(1, t+1):
            p = r(h(p), j)
        
        rainbowTable[h(p)] = pi
        print(len(rainbowTable))

    with open('tablaArcoIris.pkl', 'wb') as f:
        pickle.dump(rainbowTable, f)

def searchColision(table, p0, t):
    p = p0
    for i in range(t):
        if p in table:                                               
            break
        p = h(r(p, i)) 
    
    if i == t - 1:
        return False
    
    else:
        pwd = table[p]
        i=0
        while (h(pwd) != p0 and i < 5*t):  
            pwd = r(h(pwd), i)
            i+=1
            
        if(h(pwd) == p0):
            return [table[p], pwd]

    return [table[p], None] 

realPasswords = ['qigvh', 'tipsh', 'buvmx', 'qvydt', 'pkvjb', 'fiulf', 'wunvo', 'cmycf', 'yaltu', 'jufbh', 'nuloa', 'kqbxr', 'hwnrv', 'odvfd', 'zrypq', 'nxidl', 'uckmh', 'tqrjk', 'figfk', 'ewhqd', 'boufa', 'yvxeq', 'jexrh', 'wkkme', 'ulliq', 'lzrmp', 'zebhi', 'jezia', 'pjscs', 'qgatm', 'hsmwd', 'zcwdo', 'dmzym', 'mnobj', 'jwtrh', 'hiewd', 'obzee', 'phhsk', 'eduin', 'eklin', 'ssdkq', 'ugsti', 'wupcl', 'vhbyu', 'quubj', 'guvgu', 'fvgzm', 'exzys', 'rovcn', 'xossw', 'bxydy', 'xodbb', 'tzkro', 'oukdc', 'jcwdj', 'aqjcq', 'zntny', 'rzdrl', 'owgbu', 'nbkao', 'ygncc', 'kjvnl', 'pddhc', 'ilxfp', 'vqtva', 'fhvjd', 'whpdu', 'ibrvo', 'efqid', 'vjaof', 'igpyh', 'hbyzp', 'qrwah', 'uzued', 'ghuli', 'axawj', 'xdmlq', 'tudjd', 'bkovu', 'waree', 'snrug', 'dxakb', 'fqztp', 'ozjgq', 'nbkym', 'gdrgu', 'glfkb', 'kldpy', 'ndvro', 'bbcpo', 'uxpne', 'crmcn', 'pzjdv', 'sdpjj', 'zgxru', 'ldtyi', 'ztbdt', 'sfyic', 'psebu', 'klhbm']

dfResult= pd.DataFrame()
dfEquals= pd.DataFrame()
columns = [20,50,100, 200]
rows = [60000, 70000, 80000, 90000, 100000]

for rws in rows:
    print(rws)
    for cols in columns:
        times = []
        equalPasswords = []
        colisions = 0
        passwordsGuessed = 0
        
        start_total_time = time.time()
        generateRainbowTable(rws, cols)
        with open('tablaArcoIris.pkl', 'rb') as f:
            tabla = pickle.load(f)
        
        for passw in realPasswords:
            p0 = h(passw)

            start_search_time = time.time()
            result = searchColision(tabla, p0, cols)
            total_search_time = time.time() - start_search_time

            times.append(total_search_time)

            if(result != False):
                colisions+=1
                if(result[1] != None): 
                    equalPasswords.append((passw, result[1], result[0]))
                    passwordsGuessed += 1

        total_time = time.time() - start_total_time
        new_row = {
                    "Filas": rws,
                    "Columnas": cols,
                    "% Colisiones": (colisions/(len(realPasswords)))*100,
                    "% Éxito": (passwordsGuessed / len(realPasswords))*100,
                    "Tiempo Medio Búsqueda": round(statistics.mean(times), 4),
                    "Tiempo total": round(total_time, 4),
                    "(Original / Equivalente / Colisión)": equalPasswords
                    }
        dfResult = pd.concat([dfResult, pd.DataFrame([new_row])], ignore_index=True)

dfResult.to_csv("ArcoIris  Resultado/ArcoIrisResult.csv", index=False)
















def r(value): #Dado el hex del hash....
    value = hex(value)[2:].zfill(8)

    #APLICAR OPERACIONES XOR
    grupo1 = bin(int(value[0:2],16) ^  int(value[2:4],16))[2:].zfill(8)  
    grupo2 = bin(int(value[2:4],16) ^  int(value[4:6],16))[2:].zfill(8) 
    grupo3 = bin(int(value[4:6],16) ^  int(value[6:8],16))[2:].zfill(8) 
    grupo4 = bin(int(value[6:8],16) ^  int(value[0:2],16))[2:].zfill(8) 

    binaryResult = grupo4 + grupo3 + grupo2 + grupo1


    #TRANSFORMAR BITS EN CARACTERES LEGIBLES
    letra1 = caracteres[int(binaryResult[0:6], 2)       %   len(caracteres)] 
    letra2 = caracteres[int(binaryResult[6:12], 2)      %   len(caracteres)]
    letra3 = caracteres[int(binaryResult[12:18], 2)     %   len(caracteres)]
    letra4 = caracteres[int(binaryResult[18:24], 2)     %   len(caracteres)]
    letra5 = caracteres[int(binaryResult[24:32], 2)     %   len(caracteres)]
    
    result = letra5 + letra4 + letra3 + letra2 + letra1
    return result

def r(value, index):
    value = str(hex(value)[2:].zfill(8))[-5:]
    result = ""
    for charHex in value:
        if charHex.isalpha():
            result = result + charHex
        else:
            result = result + hex((int(charHex, 16)*index) % 16)[2:]
    return result




 # indexCaracteres = index % 5
    # result = result[(indexCaracteres):] + result[:indexCaracteres]


