import csv
import itertools
import hashlib
import pickle
import sys
import threading
import time
import statistics
import pandas as pd
import os, psutil
process = psutil.Process()

def yuval(legitMessage, ilegitMessage, h, m):
    dictTextHashes = {}
    totalIterations = 2**m
    actualIteration = 0

    while actualIteration < totalIterations:
        #processSize = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
        
        if (((actualIteration % (totalIterations / 2)) == 0) and actualIteration != 0): 
            for actualComboIlegit in itertools.product(["0", "1"], repeat=m):
                actualComboIlegit = bin(int(''.join(map(str, actualComboIlegit)), 2))[2:].ljust(30, '0')
                combinedText = ""
                for index, value in enumerate(actualComboIlegit):
                    combinedText = f'{combinedText} {ilegitMessage[index][int(value)]}'

                ilegitHash =  hashlib.md5(combinedText.encode('utf-8')).hexdigest()[:h]

                if ilegitHash in dictTextHashes: 
                    legitCombo = dictTextHashes[ilegitHash]
                    return [str(legitCombo), str(actualComboIlegit), str(ilegitHash)]
            
            dictTextHashes = {} #Delete dict

        actualComboLegit = bin(actualIteration)[2:].zfill(30)
        combinedText = ""
        for index, value in enumerate(actualComboLegit):
            combinedText = f'{combinedText} {legitMessage[index][int(value)]}'

        dictTextHashes[hashlib.md5(combinedText.encode('utf-8')).hexdigest()[:h]] = actualComboLegit
        actualIteration += 1
        
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

        df_print.to_csv("Resultados Yuval/HashAlternativo1 " + str(hashHex) + " " + str(round(statistics.mean(times),4)) + ".csv", index=False)

        print(hashHex)
        print(df_print)
        print("\n\n\n")

start_time = time.time()
mainYuval(6,11)
print(time.time() - start_time)
