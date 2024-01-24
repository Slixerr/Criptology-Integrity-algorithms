import csv
import itertools
import hashlib
import time
import statistics
import pandas as pd
import os, psutil
process = psutil.Process()

def yuval(legitMessage, ilegitMessage, h, m):
    dictTextHashesLegit = {}
    dictTextHashesIlegit = {}

    for actualCombo in itertools.product(["0", "1"], repeat=m):
        actualCombo = bin(int(''.join(map(str, actualCombo)), 2))[2:].ljust(30, '0')
        combinedText = ""
        for index, value in enumerate(actualCombo):
            combinedText = f'{combinedText} {legitMessage[index][int(value)]}'

        dictTextHashesLegit[hashlib.md5(combinedText.encode('utf-8')).hexdigest()[:h]] = actualCombo
        
    for actualCombo in itertools.product(["0", "1"], repeat=m):
        actualCombo = bin(int(''.join(map(str, actualCombo)), 2))[2:].ljust(30, '0')
        combinedText = ""
        for index, value in enumerate(actualCombo):
            combinedText = f'{combinedText} {ilegitMessage[index][int(value)]}'

        dictTextHashesIlegit[hashlib.md5(combinedText.encode('utf-8')).hexdigest()[:h]] = actualCombo   
    
    print(round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2, 4))

    for key in dictTextHashesLegit:
        if key in dictTextHashesIlegit:
            print("para h" +  str(h))
            
            return [str(dictTextHashesLegit[key]), str(dictTextHashesIlegit[key]), str(key)]

    return None


def messageLoad(file):
    with open(file, encoding='UTF-8') as f:
        reader = csv.reader(f)
        message = list(tuple(line) for line in reader)[1:]
    return message


def mainYuval(minHash, maxHash):
    legitMessage = messageLoad("Mensajes/mensajeLicito.csv")
    
    for hashHex in range(minHash,maxHash):
        times = []
        messageHexBits = hashHex*2
        colisions = 0
        df_print = pd.DataFrame()

        while colisions < 15:
            ilegitMessage = messageLoad('Mensajes/mensajeIlicito ' + str(colisions) + '.csv')
            start_time = time.time()
            result = yuval(legitMessage, ilegitMessage, hashHex, messageHexBits)
            total_time = time.time() - start_time
            if result != None:    
                times.append(total_time) 
                colisions += 1

                new_row = {
                    "Bits Mensaje": messageHexBits,
                    "Comb Binaria Lícita": result[0],
                    "Comb Binaria Ilícita": result[1],
                    "Hash": result[2],
                    "Tiempo (s)": round(total_time, 4)
                    }

                df_print = pd.concat([df_print, pd.DataFrame([new_row])], ignore_index=True)
                messageHexBits = hashHex*2

            else:
                messageHexBits += 1

        df_print.to_csv("Resultados Yuval/HashAlternativo2 " + str(hashHex) + " " + str(round(statistics.mean(times),4)) + ".csv", index=False)

        print(hashHex)
        print(df_print)
        print("\n\n\n")

        



 
legitMessage = messageLoad("Mensajes/mensajeLicito.csv")
ilegitMessage = messageLoad('Mensajes/mensajeIlicito 7.csv')

yuval(legitMessage, ilegitMessage, 13, 26)
print("\n")















